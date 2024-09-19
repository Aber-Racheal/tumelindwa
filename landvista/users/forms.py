from django import forms
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_superuser = forms.BooleanField(required=False, initial=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_superuser']
    def clean_first_name(self):
        first_name = self.cleaned_data.get('username')
        if User.objects.filter(first_name=first_name).exists():
            raise forms.ValidationError("Username already exists.")
        return first_name
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email