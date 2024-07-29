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
    profile_image = models.ImageField(upload_to='accounts/profile_images/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username

    @property
    def protectors(self):
        if self.user_type == 'senior':
            return [rel.protector for rel in self.protector_relationships.filter(pending=False)]
        return None

    @property
    def seniors(self):
        if self.user_type == 'protector':
            return [rel.senior for rel in self.senior_relationships.filter(pending=False)]
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
    days = models.CharField(max_length=50)  # 요일 저장 형식 ('mon,tue,wed' 등)

    def __str__(self):
        return f"{self.user.username} - {self.name} - {self.time} - {self.days}"

class Relationship(models.Model):
    RELATIONSHIP_CHOICES = [
        ('자녀', '자녀'),
        ('친구', '친구'),
        ('배우자', '배우자'),
        ('간병인', '간병인'),
        ('기타', '기타'),
    ]

    senior = models.ForeignKey(UserProfile, related_name='protector_relationships', on_delete=models.CASCADE)
    protector = models.ForeignKey(UserProfile, related_name='senior_relationships', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=10, choices=RELATIONSHIP_CHOICES)
    pending = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.senior.user.username} - {self.protector.user.username} - {self.relationship_type}"
