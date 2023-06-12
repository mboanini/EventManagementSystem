from django import forms
from .models import Event, EventCategory
from django.contrib.auth.forms import UserCreationForm, User


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'category',
                  'creator', 'ticket_price', 'max_seats', 'available_seats', 'program', 'image']


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = EventCategory
        fields = ['name']
