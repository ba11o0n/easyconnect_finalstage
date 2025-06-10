import paho.mqtt.client as mqtt
import ssl
import json
from mainapp.models import Device
import os
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USERNAME")
MQTT_PASS = os.getenv("MQTT_PASSWORD")

mqtt_client = None

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected successfully")
        client.subscribe("event/#")
        client.subscribe("device/#")
    else:
        print(f"[MQTT] Connection failed with code {rc}")

# Callback for when a message is received from the broker
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[MQTT] {topic} -> {payload}")

    try:
        from mainapp.views import handle_profile_swap
        
        if "available_devices" in topic:
            data = json.loads(payload)
            _device_id = data.get("device_id")
            _event_id = data.get("event_id")
            _is_available = data.get("is_available")

            Device.objects.update_or_create(
                device_id=_device_id,
                event_id = _event_id,
                available = _is_available
            )

        elif "profile_swap" in topic:
            data = json.loads(payload)
            event_id = data.get("event_id")
            ticket_id1 = data.get("ticket_id")
            ticket_id2 = data.get("ticket_id_to_swap")
            
            handle_profile_swap(event_id, ticket_id1, ticket_id2)

        elif "status" in topic:
            print(f"[MQTT] Status from device: {payload}")

    except Exception as e:
        print(f"[MQTT ERROR] {e}")

    except Exception as e:
        print("[MQTT ERROR]", e)

# Publish message to a MQTT topic
def publish_message(topic, message):
    global mqtt_client
    
    try:
        if mqtt_client and mqtt_client.is_connected():
            result = mqtt_client.publish(topic, str(message))
            result.wait_for_publish(timeout=5)
            print(f"[MQTT] Published to {topic}: {message}")
            return True
        else:
            print("[MQTT ERROR] Client not connected")
            return False
            
    except Exception as e:
        print(f"[MQTT ERROR] Failed to publish to {topic}: {e}")
        return False

# Start the MQTT client and connect to the broker
def start_mqtt():
    global mqtt_client
    
    try:
        mqtt_client = mqtt.Client()
        mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
        mqtt_client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        
        mqtt_client.connect(MQTT_SERVER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        
        print("[MQTT] Starting MQTT client...")
        return True
        
    except Exception as e:
        print(f"[MQTT ERROR] Failed to start: {e}")
        return False
