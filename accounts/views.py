from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from .forms import UserTypeForm, CustomUserCreationForm, UserProfileForm, MealTimeForm, MedicineForm
from .models import UserProfile, MealTime, Medicine
import json
from datetime import datetime

def home(request):
    return render(request, 'accounts/home.html')

def signup_step1(request):
    if request.method == 'POST':
        form = UserTypeForm(request.POST)
        if form.is_valid():
            request.session['user_type'] = form.cleaned_data['user_type']
            return redirect('signup_step2')
    else:
        form = UserTypeForm()
    return render(request, 'accounts/signup_step1.html', {'form': form})

def signup_step2(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['password'] = form.cleaned_data['password']
            return redirect('signup_step3')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup_step2.html', {'form': form})

def signup_step3(request):
    if 'user_type' not in request.session or 'username' not in request.session or 'password' not in request.session:
        return redirect('signup_step1')

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            request.session['name'] = form.cleaned_data['name']
            request.session['birth_date'] = str(form.cleaned_data['birth_date'])  # serialize date
            if request.session['user_type'] == 'senior':
                return redirect('signup_step4_senior')
            else:
                return redirect('signup_complete')
    else:
        form = UserProfileForm()
    return render(request, 'accounts/signup_step3.html', {'form': form})

def signup_step4_senior(request):
    if 'user_type' not in request.session or request.session.get('user_type') != 'senior':
        return redirect('signup_step1')

    meal_times = request.session.get('meal_times', [])
    meal_time_flags = {
        'breakfast': any(mt['meal_type'] == 'breakfast' for mt in meal_times),
        'lunch': any(mt['meal_type'] == 'lunch' for mt in meal_times),
        'dinner': any(mt['meal_type'] == 'dinner' for mt in meal_times),
    }
    all_meal_times_set = all(meal_time_flags.values())
    return render(request, 'accounts/senior/signup_step4_senior.html', {
        'meal_time_flags': meal_time_flags,
        'all_meal_times_set': all_meal_times_set,
    })

def meal_time(request):
    if 'user_type' not in request.session or request.session.get('user_type') != 'senior':
        return redirect('home')

    if request.method == 'POST':
        form = MealTimeForm(request.POST)
        if form.is_valid():
            meal_type = form.cleaned_data['meal_type']
            time = form.cleaned_data['time'].strftime('%H:%M:%S')  # Convert to string
            meal_times = request.session.get('meal_times', [])
            meal_times = [mt for mt in meal_times if mt['meal_type'] != meal_type]  # 기존 항목 제거
            meal_times.append({'meal_type': meal_type, 'time': time})
            request.session['meal_times'] = meal_times
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        form = MealTimeForm()

    meal_times = request.session.get('meal_times', [])
    meal_time_flags = {
        'breakfast': any(mt['meal_type'] == 'breakfast' for mt in meal_times),
        'lunch': any(mt['meal_type'] == 'lunch' for mt in meal_times),
        'dinner': any(mt['meal_type'] == 'dinner' for mt in meal_times),
    }
    return render(request, 'accounts/senior/meal_time.html', {'form': form, 'meal_time_flags': meal_time_flags})

def get_meal_time_flags(request):
    meal_times = request.session.get('meal_times', [])
    meal_time_flags = {
        'breakfast': any(mt['meal_type'] == 'breakfast' for mt in meal_times),
        'lunch': any(mt['meal_type'] == 'lunch' for mt in meal_times),
        'dinner': any(mt['meal_type'] == 'dinner' for mt in meal_times),
    }
    return JsonResponse(meal_time_flags)

def medicine_register(request):
    return render(request, 'accounts/senior/medicine_register.html')

def save_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine_data = {
                'name': form.cleaned_data['name'],
                'time': form.cleaned_data['time'].strftime('%H:%M:%S'),  # Convert to string
                'days': form.cleaned_data['days']
            }
            medicines = request.session.get('medicines', [])
            medicines.append(medicine_data)
            request.session['medicines'] = medicines
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False})

def signup_complete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            with transaction.atomic():
                # 새로운 사용자 생성
                user = User.objects.create_user(
                    username=data['username'],
                    password=data['password']
                )

                # 사용자 프로필 생성
                UserProfile.objects.create(
                    user=user,
                    user_type=request.session.get('user_type', 'senior'),
                    name=data['name'],
                    birth_date=data['birth_date']
                )

                # 기존 세션에서 식사 시간과 투약 정보 가져오기
                meal_times = request.session.get('meal_times', [])
                medicines = request.session.get('medicines', [])

                # 새 사용자에게 식사 시간과 투약 정보를 복사
                for meal_time in meal_times:
                    MealTime.objects.create(
                        user=user,
                        meal_type=meal_time['meal_type'],
                        time=datetime.strptime(meal_time['time'], '%H:%M:%S').time()  # Convert back to time object
                    )

                for medicine in medicines:
                    Medicine.objects.create(
                        user=user,
                        name=medicine['name'],
                        time=datetime.strptime(medicine['time'], '%H:%M:%S').time(),  # Convert back to time object
                        days=medicine['days']
                    )

            auth_login(request, user)
            clear_signup_session(request)  # 회원가입 완료 후 세션 정보 정리
            return JsonResponse({'success': True})
        except IntegrityError:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

# 회원가입 완료 후에는 세션에 저장된 정보를 정리함
def clear_signup_session(request):
    request.session.pop('username', None)
    request.session.pop('password', None)
    request.session.pop('name', None)
    request.session.pop('birth_date', None)
    request.session.pop('user_type', None)
    request.session.pop('meal_times', None)
    request.session.pop('medicines', None)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('home')
    return render(request, 'accounts/logout.html')
