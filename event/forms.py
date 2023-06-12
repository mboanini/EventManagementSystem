from django import forms
from .models import Event, EventCategory
from django.contrib.auth.forms import UserCreationForm, User


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'category',
                  'creator', 'max_seats', 'available_seats', 'program', 'image']


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['name']
