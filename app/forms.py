from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Order, UserProfile, Category
from django import forms
from django.contrib.auth.forms import UserCreationForm


class AddProductForm(forms.Form):
    name = forms.CharField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    description = forms.CharField(widget=forms.Textarea())
    price = forms.FloatField()
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


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

class CustomOrderForm(ModelForm):
    description = forms.CharField(max_length=512, widget=forms.Textarea, help_text="Describe your custom order (size, color, materials, etc.)")
    class Meta:
        model = Order
        fields = ('description',)

