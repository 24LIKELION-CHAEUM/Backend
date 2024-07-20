from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('senior', 'Senior'),
        ('protector', 'Protector'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.user.username

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