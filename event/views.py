from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Registration, EventCategory
from django.contrib.auth.decorators import login_required
from .forms import EventForm, SignUpForm, CategoryForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages


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
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('event:event_list')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@login_required
def modify_event(request, title):
    event = get_object_or_404(Event, title=title)

    if request.user != event.creator:
        messages.error(request, "You are not authorized to modify this event.")
        return redirect('event:my_events')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
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
        messages.error(request, "You are not authorized to remove this event.")
        return redirect('event:my_events')

    if request.method == 'POST':
        event.delete()
        return redirect('event:my_events')

    return render(request, 'remove_event.html', {'event': event})


@login_required
def participant_list(request, title):
    event = get_object_or_404(Event, title=title)

    if request.user != event.creator:
        messages.error(request, "You are not authorized to remove this event.")
        return redirect('event:my_events')

    registrations = event.registrations.all()

    return render(request, 'participant_list.html', {'event': event, 'registrations': registrations})


def event_search(request):
    query = request.GET.get('query')

    events = Event.objects.all()

    if query:
        events = events.filter(title__icontains=query) | events.filter(category__name__icontains=query)

    return render(request, 'event_search.html', {'events': events, 'query': query})


def my_events(request):
    events = Event.objects.filter(creator=request.user)

    context = {
        'events': events
    }

    return render(request, 'my_events.html', context)


@login_required()
def my_profile(request):
    user = request.user
    created_events = Event.objects.filter(creator=user)
    registered_events = Event.objects.filter(registrations__participant=user)

    return render(request, 'profile.html', {'created_events': created_events,
                                            'registered_events': registered_events})


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event:create_event')
    else:
        form = CategoryForm()

    return render(request, "create_category.html", {'form': form})
