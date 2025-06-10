from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-panel/', views.admin, name='admin'),
    path('attendee-panel/', views.attendee, name='attendee'),
    path('employee-panel/', views.employee, name='employee'),

    path('dashboard/', views.attendee_dashboard, name='attendee_dashboard'),
    path('profile/', views.attendee_profile, name='attendee_profile'),
    path('create-event/', views.create_event, name='create_event'),
    path('api/events/', views.get_events_json, name='get_events_json'),
    path('scan-ticket/', views.scan_ticket, name='scan_ticket'),
    path('employee/scan/', views.scanner_view, name='scanner_view'),
    path('join-employee-event/', views.join_event_employee, name='join_event_employee'),
    path('join-event/', views.join_event, name='join_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]
