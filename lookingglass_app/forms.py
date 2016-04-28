from lookingglass_app.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('flickrid',)

class UploadFileForm(forms.Form):
   title = forms.CharField(max_length=50)
   file = forms.FileField()
