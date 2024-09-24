from django import forms
from .models import VideoModel

class VideoForm(forms.Form):
    title = forms.CharField(required=True, max_length=100)
    file = forms.FileField(required=True)

    def save(self, commit=True):
        video = VideoModel(title = self.cleaned_data['title'],
                           video = self.cleaned_data['video'])
        video.save()
        return video