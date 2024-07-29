from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, MealTime, Medicine, Relationship

class UserTypeForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('senior', '시니어'),
        ('protector', '보호자'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)
    
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Username',
            'password': 'Password',
        }
        help_texts = {
            'username': None,  # 도움말 텍스트 제거
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None  # 추가로 여기서도 제거

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "비밀번호가 일치하지 않습니다.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'birth_date', 'profile_image']  # 프로필 사진 필드 추가
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

class MealTimeForm(forms.ModelForm):
    class Meta:
        model = MealTime
        fields = ['meal_type', 'time']
        widgets = {
            'meal_type': forms.Select(choices=MealTime.MEAL_TYPE_CHOICES),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def save(self, user, commit=True):
        meal_time = super().save(commit=False)
        meal_time.user = user
        if commit:
            meal_time.save()
        return meal_time

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'time', 'days']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'days': forms.TextInput()  # 사용자 정의 입력 방식 적용 가능
        }

    def save(self, user, commit=True):
        medicine = super().save(commit=False)
        medicine.user = user
        if commit:
            medicine.save()
        return medicine
