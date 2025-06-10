from django.shortcuts import render, redirect
from mainapp.decorators import role_required
from core.mqtt_client import publish_message
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
import uuid
import random
import string
from datetime import datetime
from .models import Event, Ticket, EmployeeProfile, Device, UserProfile, Connection
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    return render(request, 'main/index.html')

@role_required('admin')
def admin(request):
    today = timezone.now().date()
    events = Event.objects.filter(host=request.user).order_by('date')
    context = {
        'upcoming_events': events.filter(date__gte=today),
        'past_events': events.filter(date__lt=today)
    }
    return render(request, 'main/admin.html', context)

@login_required
@role_required('attendee')
def attendee(request):
    return attendee_dashboard(request)

# Dashboard for attendees to view their tickets??
def ticket_dashboard(request):
    msg = latest_message.get("easyconnect/ticket", "No ticket data")
    return render(request, "mainapp/dashboard.html", {"ticket_info": msg})

# Generate a random 6 digit alphanumeric code for events and tickets
def gen_code_6():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Generate a random 2 digit code for events ids
def gen_code_2():
    return ''.join(random.choices(string.digits, k=2))
    
# Attendee dashboard
@login_required
@role_required('attendee')
def attendee_dashboard(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('event_date')
    now = timezone.now()
    
    # Get connections
    connections = Connection.objects.filter(user1=request.user).select_related('user2')
    connected_users = []
    
    for conn in connections:
        profile, _ = UserProfile.objects.get_or_create(
            user=conn.user2, 
            defaults={'role': 'attendee'}
        )
        connected_users.append({
            'user': conn.user2,
            'profile': profile,
            'event_id': conn.event_id
        })
    
    context = {
        'upcoming_events': tickets.filter(event_date__gte=now),
        'past_events': tickets.filter(event_date__lt=now),
        'connections': connected_users
    }
    return render(request, "main/attendee.html", context)

# Attendee profile
@login_required
@role_required('attendee')
def attendee_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user, defaults={'role': 'attendee'})
    if request.method == 'POST':
        request.user.full_name = request.POST.get('full_name', request.user.full_name)
        request.user.save()

        profile.bio = request.POST.get('bio', profile.bio)
        profile.linkedin = request.POST.get('linkedin', profile.linkedin)
        profile.website = request.POST.get('website', profile.website)
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('attendee')

    context = {'profile': profile}
    return render(request, 'main/profile.html', context)

# Event creation
@login_required
@role_required('admin')
def create_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        date = request.POST.get('date')
        time_val = request.POST.get('time')
        location = request.POST.get('location')

        Event.objects.create(
            name=name,
            description=description,
            date=date,
            time=time_val,
            location=location,
            host=request.user,
            attendee_GA_code=gen_code_6(),
            attendee_VIP_code=gen_code_6(),
            employee_code=gen_code_6(),
            event_id="E_" + gen_code_2(),
            attendee_count=0
        )
        messages.success(request, 'Event created successfully')
        return redirect('admin')
    return render(request, 'main/create_event.html')

def get_events_json(request):
    events = Event.objects.all().values("id", "name", "location", "date", "time")
    return JsonResponse(list(events), safe=False)

# Attendee joins an event using a code
@login_required
@csrf_exempt
def join_event(request):
    if request.method == 'POST':
        event_code = request.POST.get('event_code')
        
        try:
            # First try to find event by GA code
            event = Event.objects.get(attendee_GA_code=event_code)
            _ticket_type = 'GA'
        except Event.DoesNotExist:
            try:
                # If GA code fails, try VIP code
                event = Event.objects.get(attendee_VIP_code=event_code)
                _ticket_type = 'VIP'
            except Event.DoesNotExist:
                messages.error(request, 'Invalid event code')
                return redirect('attendee')
        
        # Get the event time and date
        event_dt = timezone.make_aware(datetime.combine(event.date, event.time))

        # Generate a ticket for the user if it doesn't exist
        ticket, created = Ticket.objects.get_or_create(
            user=request.user,
            ticket_id = "T_" + gen_code_6(),
            event_name = event.name,
            event_date = event_dt,
            ticket_type = _ticket_type,
            event_id=event.event_id
        )

        # Only update count and show success if ticket was created
        if created:
            event.attendee_count += 1
            event.save()
            messages.success(request, 'Event joined successfully')
        else:
            messages.info(request, 'You are already registered for this event')

        return redirect('attendee')
    return redirect('attendee')

@login_required
@role_required('employee')
def employee(request):
    profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
    events = profile.joined_events.all().order_by('date')
    today = timezone.now().date()
    context = {
        'upcoming_events': events.filter(date__gte=today),
        'past_events': events.filter(date__lt=today)
    }
    return render(request, 'main/employee.html', context)

# 
@csrf_exempt
def join_event_employee(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            event_code = data.get('event_code')
        else:
            event_code = request.POST.get('event_code')
        try:
            event = Event.objects.get(employee_code=event_code)
            profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
            profile.joined_events.add(event)
            if request.content_type == 'application/json':
                return JsonResponse({'success': True, 'event_id': event.id})
            messages.success(request, 'Event joined successfully')
            return redirect('employee')
        except Event.DoesNotExist:
            if request.content_type == 'application/json':
                return JsonResponse({'success': False, 'error': 'Invalid event code'})
            messages.error(request, 'Invalid event code')
            return redirect('employee')

# QR code scanning for tickets
@csrf_exempt
def scan_ticket(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            _ticket_id = data.get('ticket_id')
            
            # Get ticket and verify it exists
            ticket = Ticket.objects.get(ticket_id=_ticket_id)
            
            # Find available device for the same event_id
            device = Device.objects.filter(event_id=ticket.event_id, available=True).first()
            
            if not device:
                return JsonResponse({'success': False, 'error': 'No available devices'})
            
            # Assign device to ticket
            device.assigned_ticket = _ticket_id
            device.available = False
            device.save()
            
            # Send MQTT message to device to assign ticket
            topic = f"device/{device.device_id}/assignment"
            success = publish_message(topic, _ticket_id)
            
            if success:
                return JsonResponse({'success': True, 'device_id': device.device_id})
            else:
                device.assigned_ticket = None
                device.available = True
                device.save()
                return JsonResponse({'success': False, 'error': 'Failed to contact device'})
                
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid ticket'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def scanner_view(request):
    return render(request, 'main/scanner.html')


@login_required
@role_required('admin')
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id, host=request.user)
    event_dt = timezone.make_aware(datetime.combine(event.date, event.time))
    attendee_count = Ticket.objects.filter(event_name=event.name, event_date=event_dt).count()
    interactions_count = Connection.objects.filter(event_id=event_id).count()
    context = {
        'event': event,
        'attendee_count': attendee_count,
        'interactions_count': interactions_count,
    }
    return render(request, 'main/event_detail.html', context)


@login_required
@role_required('attendee')
def ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id, user=request.user)
    event = Event.objects.filter(
        name=ticket.event_name,
        date=ticket.event_date.date(),
        time=ticket.event_date.time()
    ).first()
    context = {
        'ticket': ticket,
        'event': event
    }
    return render(request, 'main/ticket_detail.html', context)

# Profile swap
def handle_profile_swap(event_id, ticket_id1, ticket_id2):
    try:
        # Get tickets and users
        ticket1 = Ticket.objects.get(ticket_id=ticket_id1, event_id=event_id)
        ticket2 = Ticket.objects.get(ticket_id=ticket_id2, event_id=event_id)
        
        user1 = ticket1.user
        user2 = ticket2.user
        
        # Create connections
        Connection.objects.get_or_create(
            user1=user1, user2=user2, event_id=event_id
        )
        Connection.objects.get_or_create(
            user1=user2, user2=user1, event_id=event_id
        )

        # Send MQTT message to device to buzz motor
        topic1 = f"event/{event_id}/profile_swap/{ticket_id1}"
        topic2 = f"event/{event_id}/profile_swap/{ticket_id2}"
        publish_message(topic1, "profile swap")
        publish_message(topic2, "profile swap")

        
    except Ticket.DoesNotExist:
        print("[PROFILE SWAP ERROR] Invalid ticket IDs")
    except Exception as e:
        print(f"[PROFILE SWAP ERROR] {e}")

