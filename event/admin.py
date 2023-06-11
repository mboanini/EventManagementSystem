from django.contrib import admin

# Register your models here.
from .models import Event
from .models import EventCategory
from .models import Registration

admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(Registration)
