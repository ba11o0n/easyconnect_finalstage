from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Extended Profile for any user role (attendee, admin, vendor)
class UserProfile(models.Model):
    
    ROLE_CHOICES = [
        ('attendee', 'Attendee'),
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# Event model created by host/admin
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='hosted_events')
    attendee_GA_code = models.CharField(max_length=10, unique=True)
    attendee_VIP_code = models.CharField(max_length=10, default="VIP123")
    employee_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    attendee_count = models.PositiveIntegerField(default=0)
    event_id = models.CharField(max_length=10, default="E_00")

    def __str__(self):
        return f"{self.name} on {self.date}"
    
# Ticket for attendees
class Ticket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=100, unique=True)
    event_id = models.CharField(max_length=10, default="E_00")
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    ticket_type = models.CharField(max_length=50, choices=[
        ('GA', 'General Admission'),
        ('VIP', 'VIP'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket_id} ({self.event_name})"
    
# Device 
class Device(models.Model):
    device_id = models.CharField(max_length=100)
    event_id = models.CharField(max_length=10, default="E_00")
    assigned_ticket = models.CharField(max_length=100, blank=True, null=True)
    available = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "Available" if self.available else f"Assigned to {self.assigned_ticket}"
        return f"Device {self.device_id} - {status}"
    

# Employee account 
class EmployeeProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    joined_events = models.ManyToManyField(Event, related_name="employees")
    phone_number = models.CharField(max_length=20, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Employee: {self.user.username}"
    
# Connection between two users at an event
class Connection(models.Model):
    user1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='connections_as_user1')
    user2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='connections_as_user2')
    event_id = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user1', 'user2', 'event_id']
    
    def __str__(self):
        return f"{self.user1.username} ↔ {self.user2.username} at {self.event_id}"
