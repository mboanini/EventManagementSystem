from django.urls import path
from . import views

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
    path('ticket/<str:title>', views.buy_ticket, name='buy_ticket'),
    path('already-registered/', views.already_registered, name='already_registered'),
    path('sold-out/', views.sold_out, name='sold_out'),
    path('unauthorized_page/', views.unauthorized_page, name='unauthorized_page'),
    path('search/', views.event_search, name='event_search'),
]
