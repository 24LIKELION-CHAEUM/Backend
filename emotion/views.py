from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Emotion
from .forms import EmotionForm, ProtectorCommentForm
from datetime import datetime, timedelta
from accounts.models import UserProfile, Relationship

@login_required
def emotion_page(request):
    today = datetime.today().date()
    start_date = today - timedelta(days=today.weekday())
    dates = [start_date + timedelta(days=i) for i in range(7)]

    selected_date = request.GET.get('date', str(today))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.user_type == 'senior':
        emotions = Emotion.objects.filter(user=request.user, date=selected_date)
        template = 'emotion/senior/emotion_page.html'
    else:
        related_user_ids = Relationship.objects.filter(protector=user_profile, pending=False).values_list('senior__user_id', flat=True)
        seniors = User.objects.filter(id__in=related_user_ids)
        emotions = Emotion.objects.filter(user__in=seniors, date=selected_date)
        template = 'emotion/protector/emotion_page.html'

    return render(request, template, {
        'dates': dates,
        'selected_date': selected_date,
        'emotions': emotions,
    })

@login_required
def emotion_create(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type != 'senior':
        return redirect('emotion_page')

    today = datetime.today().date()
    if Emotion.objects.filter(user=request.user, date=today).exists():
        return redirect('emotion_page')

    if request.method == 'POST':
        form = EmotionForm(request.POST)
        if form.is_valid():
            emotion = form.save(commit=False)
            emotion.user = request.user
            emotion.date = today
            emotion.save()
            return redirect('emotion_page')
    else:
        form = EmotionForm()

    return render(request, 'emotion/senior/emotion_create.html', {'form': form})

@login_required
def senior_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    relationships = Relationship.objects.filter(protector=user_profile, pending=False).select_related('senior')

    seniors = []
    for rel in relationships:
        senior_profile = rel.senior
        senior_profile.relationship = rel.relationship_type
        senior_profile.today_emotion = Emotion.objects.filter(user=senior_profile.user, date=datetime.today().date()).first()
        if senior_profile.today_emotion:
            senior_profile.has_comment = bool(senior_profile.today_emotion.protector_comment)
        else:
            senior_profile.has_comment = False
        seniors.append(senior_profile)

    return render(request, 'emotion/protector/senior_page.html', {
        'seniors': seniors,
    })

@login_required
def add_comment(request, emotion_id):
    emotion = get_object_or_404(Emotion, id=emotion_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.user_type == 'protector' and Relationship.objects.filter(protector=user_profile, senior=emotion.user.userprofile, pending=False).exists():
        if request.method == 'POST':
            form = ProtectorCommentForm(request.POST, instance=emotion)
            if form.is_valid():
                form.save()
                return redirect('emotion_page')
        else:
            form = ProtectorCommentForm(instance=emotion)
        
        return render(request, 'emotion/protector/add_comment.html', {'form': form, 'emotion': emotion})
    else:
        return redirect('emotion_page')
