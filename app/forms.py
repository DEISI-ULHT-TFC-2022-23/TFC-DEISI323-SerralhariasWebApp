from django.forms import ModelForm
from .models import User, Product, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm


class addProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class UserEditForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'vat_number', 'address', 'billing_address')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)