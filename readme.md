# EasyConnect Software Repository Overview 
```

├── README.MD                     # Project overview and instructions
├── authapp                       # Handles authentication logic
│   ├── auth_backend.py           # Custom auth backend (e.g., role-based access)
│   ├── models.py                 # User models
│   └── views.py                  # Signup/login views
├── core                          # Django config and MQTT interface
│   ├── mqtt_client.py            # MQTT client logic (device communication)
│   ├── settings.py               # Project settings
│   └── hivemq-cert.pem           # Certificate for secure MQTT
├── db.sqlite3                    # Local development database
├── mainapp                       # Core app for events, tickets, profiles
│   ├── models.py                 # Events, devices, tickets, etc.
│   ├── views.py                  # Dashboard/event views
│   └── utils.py                  # Helper functions
├── manage.py                     # Django CLI entry point
├── requirements.txt              # Python dependencies
├── static                        # Frontend assets (CSS/JS)
│   ├── css
│   └── js
├── templates                     # HTML templates for frontend
│   ├── auth                      # Login/signup templates
│   └── main                      # Dashboards, event views, etc.
└── test_mqtt_publish.py          # MQTT publishing test script
```

### Software Objectives 
* Facilitates user registration with role-specific dashboards (Attendee, Host, Employee)
* Enables event creation, ticket generation, and device assignment
* Supports profile exchange via BLE and access control via NFC
* Communicates in real time with ESP32-C6 wristbands via MQTT
* Displays user interactions and insights through a responsive web interface

### Modules Overview
#### authapp/ 
Handles account creation, login, and user roles (host, employee, attendee)

#### mainapp/ 
Responsible for primary features: 
* Profiles (public info, social links, dashboards)
* Events (creation, joining, tracking)
* Tickets (generation, scanning, verification)
* Device assignment via MQTT
* Profile swapping logic from BLE handshakes

#### core/
Includes: 
* mqtt_client.py for MQTT interactions
* Project-wide configuration in settings.py
* SSL certificate for secure MQTT with HiveMQ (hivemq-cert.pem)

### Software + Hardware Integration 
* When a ticket QR code is scanned by an employee, this software:
    1. Verifies the ticket
    2. Publishes to a specific device topic over MQTT
    3. Updates BLE advertising on the device with ticket info

* During a BLE handshake, the device sends a POST to the link:
> https://www.EasyConnect.com/api/profile-exchange
{
  "device_ticket_id": "T1",
  "detected_ticket_id": "T2"
}

→ The software:

  Matches ticket IDs to users
  Updates both users’ dashboards with each other’s profiles
* When a phone reads an NFC chip on a wristband:
  Redirects to a secure page showing that ticket’s ID, name, and tier
  Enables access control visuals on-site (LED color tiers optional)

### Local Development SetUp
##### 1. Clone the Repository 
```
git clone https://github.com/YourUsername/EasyConnect-Software.git
cd EasyConnect-Software
```
##### 2. Create Environment & Install Requirements
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
``` 
##### 3. Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```
##### 4. Start the Server 
```python 
manage.py runserver
```

### MQTT Broker Configuration
You must have a HiveMQ broker set up as described in the hardware README for this web application to work.

In mqtt_client.py or .env, configure:
```python
MQTT_SERVER=your_cluster_url
MQTT_PORT=8883
MQTT_USERNAME=your_mqtt_username
MQTT_PASSWORD=your_mqtt_password
```

### MQTT Activities (Software to Devices) 
#### Subscriptions (Software)
* event/+/available_devices/+ → Listen for available devices
* device/+/status → Confirm actions or receive logs
#### Publications (Software)
* device/{device_id}/control → Assign ticket or configure device
* event/{event_id}/broadcast → Reboot or broadcast event-wide commands

### Role Based User Logical Flow 
#### Attendee
1. Signs up → updates public profile
2. Joins event using code → ticket is generated
3. Scans other attendees → views exchanged profiles on dashboard

#### Host

1. Registers as host
2. Creates event → receives attendee/employee join codes
3. Monitors:
    * Number of attendees
    * Profile exchanges (graph)
    * Top connector

#### Employee

1. Signs up as employee
2. Joins event
3. Scans QR codes to assign devices
4. Taps wristbands for access control info via NFC

### Testing Tools
Run the MQTT publish script:
``` 
python test_mqtt_publish.py
```

Use the HiveMQ Web Client to monitor live topics:
* device/#
* event/#
