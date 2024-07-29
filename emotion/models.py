from django.db import models
from django.contrib.auth.models import User

class Emotion(models.Model):
    EMOTION_CHOICES = [
        ('happy', '행복'),
        ('neutral', '평범'),
        ('sad', '슬픔'),
        ('angry', '분노'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotions')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField()
    emotion = models.CharField(max_length=10, choices=EMOTION_CHOICES)
    description = models.TextField(blank=True)
    protector_comment = models.TextField(blank=True)  # 보호자의 한마디 필드 추가

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.emotion}"
