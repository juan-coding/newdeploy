from django import forms
from .models import Upload


# upload file system
class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['description', 'file']