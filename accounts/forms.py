# users/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth.hashers import make_password

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


from django import forms
from .models import User

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User  # Your custom user model
        fields = ['username', 'password', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
                'required': 'required'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter password',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
                'required': 'required'
            }),
            'role': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
        }
    def save(self, commit=True):
        user = super().save(commit=False)  # Create the user instance without saving to DB
        user.password = make_password(self.cleaned_data['password'])  # Hash the password

        # Handle role assignment
        if self.cleaned_data['role'] == 'Admin':
            user.is_staff = True
            user.is_superuser = True
        else:  # Make sure to handle other roles if needed
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()  # Save the user instance to the database
        return user


