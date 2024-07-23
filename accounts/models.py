from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('senior', 'Senior'),
        ('protector', 'Protector'),
    ]

    RELATIONSHIP_CHOICES = [
        ('자녀', '자녀'),
        ('친구', '친구'),
        ('배우자', '배우자'),
        ('간병인', '간병인'),
        ('기타', '기타'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    senior_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='protector_userprofiles')
    relationship = models.CharField(max_length=10, choices=RELATIONSHIP_CHOICES, blank=True, null=True)
    profile_image = models.ImageField(upload_to='accounts/profile_images/', null=True, blank=True)  # 프로필 사진 필드 추가
    pending_protector_requests = models.ManyToManyField(User, related_name='pending_requests', blank=True)
    
    def __str__(self):
        return self.user.username

    @property
    def protectors(self):
        if self.user_type == 'senior':
            return self.user.protector_userprofiles.all()
        return None

    @property
    def seniors(self):
        if self.user_type == 'protector':
            return UserProfile.objects.filter(senior_user=self.user)
        return None

class MealTime(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', '아침'),
        ('lunch', '점심'),
        ('dinner', '저녁'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)
    time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} - {self.time}"
    
class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    time = models.TimeField()
    days = models.CharField(max_length=50)  # 'mon,tue,wed' 형식으로 저장

    def __str__(self):
        return f"{self.user.username} - {self.name} - {self.time} - {self.days}"
