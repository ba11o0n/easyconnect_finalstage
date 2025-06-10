from core.mqtt_client import publish_message
import time

if __name__ == "__main__":
    # You must run this after Django is started and MQTT has connected
    time.sleep(2)  # Wait for connection
    test_topic = "easyconnect/device123/control"
    test_payload = '{"ticket_id": "T1234"}'
    publish_message(test_topic, test_payload)
    print("Message published to", test_topic)