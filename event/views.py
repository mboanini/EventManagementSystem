from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventCategory, Registration
from django.contrib.auth.decorators import login_required
from .forms import EventForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django import forms


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event:event_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event:event_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, title):
    event = Event.objects.get(title=title)
    return render(request, 'event_detail.html', {'event': event})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event:event_list')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@login_required
def modify_event(request, title):
    event = get_object_or_404(Event, title=title)

    if request.user != event.creator:
        return redirect('event:unauthorized_page')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event:event_detail', title=event.title)
    else:
        form = EventForm(instance=event)

        return render(request, 'modify_event.html', {'form': form, 'event': event})


@login_required
def remove_event(request, title):
    event = get_object_or_404(Event, title=title)

    if request.user != event.creator:
        return redirect('event:unauthorized_page')

    if request.method == 'POST':
        event.delete()
        return redirect('event:event_list')

    return render(request, 'remove_event.html', {'event': event})


@login_required
def participant_list(request, title):
    event = get_object_or_404(Event, title=title)

    if request.user != event.creator:
        return redirect('event: unauthorized_page')

    registrations = event.registrations.all()

    return render(request, 'participant_list.html', {'event': event, 'registrations': registrations,
                                                     'unauthorized_page': unauthorized_page})


def unauthorized_page(request):
    return render(request, 'unauthorized_page.html')


def buy_ticket(request, title):
    event = get_object_or_404(Event, title=title)

    is_registered = Registration.objects.filter(event=event, participant=request.user).exists()

    if request.method == 'POST':
        if is_registered:
            return redirect('event:already_registered')
        else:
            if event.available_seats > 0:
                registration = Registration(event=event, participant=request.user)
                registration.save()

                event.available_seats -= 1
                event.save()

                return redirect('event:event_detail', title=event.title)
            else:
                return redirect('event:sold_out')

    return render(request, 'event_registration.html', {'event': event, 'is_registered': is_registered,
                                                       'sold_out': sold_out})


def already_registered(request):
    return render(request, 'already_registered.html')


def sold_out(request):
    return render(request, 'sold_out.html')


def event_search(request):
    query = request.GET.get('query')

    events = Event.objects.all()

    if query:
        events = events.filter(title__icontains=query) | events.filter(category__name__icontains=query)

    return render(request, 'event_search.html', {'events': events, 'query': query})
