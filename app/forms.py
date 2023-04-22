from django.forms import ModelForm
from .models import MyUser, addProduct
from django import forms
from django.contrib.auth.forms import UserCreationForm


class addProductForm(ModelForm):
    class Meta:
        model = addProduct
        fields = '__all__'

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)