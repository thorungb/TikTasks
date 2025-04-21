from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TodoItem

class UserRegisterForm(UserCreationForm):
    """
    Form for user registration.
    """
    email = forms.EmailField()
    
    class Meta:
        """Meta class for UserRegisterForm."""
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TodoItemForm(forms.ModelForm):
    """
    Form for creating and updating TodoItem instances.
    """
    class Meta:
        """Meta class for TodoItemForm."""
        model = TodoItem
        fields = ['title', 'description', 'status', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
