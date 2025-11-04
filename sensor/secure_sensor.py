#!/usr/bin/env python3
# sensor/secure_sensor.py
# Sensor that connects using username/password (for mosquitto_secure.conf).

import paho.mqtt.client as mqtt
import time
import random
import json
import argparse
import os

parser = argparse.ArgumentParser(description="Secure simulated temperature sensor.")
parser.add_argument("--broker", default="localhost", help="MQTT broker host")
parser.add_argument("--topic", default="sensors/temperature1", help="MQTT topic")
parser.add_argument("--interval", type=float, default=3.0, help="Publish interval (s)")
parser.add_argument("--username", default=os.environ.get("MQTT_USER","sensor1"))
parser.add_argument("--password", default=os.environ.get("MQTT_PASS","sensorpass"))
args = parser.parse_args()

client = mqtt.Client(client_id="sensor_secure_1")
client.username_pw_set(args.username, args.password)
client.connect(args.broker, 1883, 60)

try:
    while True:
        temperature = round(random.uniform(18.0, 25.0), 2)
        payload = {
            "device_id": "sensor_secure_1",
            "timestamp": int(time.time()),
            "temperature": temperature
        }
        client.publish(args.topic, json.dumps(payload))
        print(f"[SENSOR-SECURE] Published to {args.topic}: {payload}")
        time.sleep(args.interval)
except KeyboardInterrupt:
    print("Exiting sensor.")
    client.disconnect()
