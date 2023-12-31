from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'event'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('events/<str:title>/', views.event_detail, name='event_detail'),
    path('createEvent/', views.create_event, name='create_event'),
    path('modifyEvent/<str:title>', views.modify_event, name='modify_event'),
    path('removeEvent/<str:title>', views.remove_event, name='remove_event'),
    path('event/<str:title>/participants', views.participant_list, name='participant_list'),
    path('search/', views.event_search, name='event_search'),
    path('myEvents/', views.my_events, name='my_events'),
    path('myProfile/', views.my_profile, name='my_profile'),
    path('newCategory/', views.create_category, name='category'),
    path('buy_ticket/<str:title>/', views.buy_ticket, name='buy_ticket'),
    path('cancel_booking/<str:title>/', views.cancel_booking, name='cancel_booking'),
    path('event_registration/<str:title>/', views.event_registration, name='event_registration'),
    path('already_registered/<str:title>/', views.already_registered, name='already_registered'),
    path('payment/', views.payment, name='payment'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
