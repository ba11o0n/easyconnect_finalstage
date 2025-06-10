import paho.mqtt.publish as publish
import ssl
import json

def assign_ticket_to_device(device_id, ticket_id):
    topic = f"device/{clientId}/#"
    payload = {
        "command": "assignment",
        "ticket_id": ticket_id
    }

    publish.single(
        topic,
        json.dumps(payload),
        hostname="your-cluster.hivemq.cloud",
        port=8883,
        auth={"username": "your_username", "password": "your_password"},
        tls={"cert_reqs": ssl.CERT_REQUIRED}
    )
