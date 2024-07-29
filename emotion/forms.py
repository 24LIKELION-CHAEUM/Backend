from django import forms
from .models import Emotion

class EmotionForm(forms.ModelForm):
    class Meta:
        model = Emotion
        fields = ['emotion', 'time', 'description']
        widgets = {
            'time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

class ProtectorCommentForm(forms.ModelForm):
    class Meta:
        model = Emotion
        fields = ['protector_comment']
        widgets = {
            'protector_comment': forms.Textarea(attrs={'rows': 3}),
        }
