from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username= forms.CharField(required=True, 
                                min_length= 4, max_length= 50, 
                                widget= forms.TextInput(attrs={
                                    'type': 'username',
                                    'class': 'form-control',
                                    'id': 'floatingInput'
                                    }))
                                    
    email= forms.EmailField(required=True, 
                                widget=forms.PasswordInput(attrs={
                                    'type': 'email',
                                    'class': 'form-control',
                                    'id': 'floatingInput'
                                    }))

    password= forms.CharField(required=True, 
                                widget=forms.PasswordInput(attrs={
                                    'type': 'password',
                                    'class': 'form-control',
                                    'id': 'floatingPassword'
                                    }))


    password2= forms.CharField(required=True, 
                            widget=forms.PasswordInput(attrs={
                                    'type': 'password',
                                    'class': 'form-control',
                                    'id': 'floatingPassword'
                                    }))

    def clean_username(self):
        username= self.cleaned_data.get('username').lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already being used')
        return username

    def clean_email(self):
        email= self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already being used')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'Password not matching')

    """
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            email= self.cleaned_data['email'],
            password= self.cleaned_data['password']
        )
        return user
    """
