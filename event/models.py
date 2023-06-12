import datetime
from PIL import Image

from django.db import models
from django.contrib.auth.models import User


def event_image_upload_path(instance, filename):
    return f'{filename}'


class Event(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(default=datetime.time)
    location = models.CharField(max_length=100)
    program = models.TextField(default='Not Available')
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    image = models.ImageField(upload_to=event_image_upload_path, null=True, blank=True)
    category = models.ManyToManyField('EventCategory')
    # participants = models.ManyToManyField(User, related_name="events_participants")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    max_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class EventCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"

    def __str__(self):
        return self.name


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.participant.username} - {self.event.title}"
