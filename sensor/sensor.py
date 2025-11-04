#!/usr/bin/env python3
# sensor/sensor.py
# Simple sensor simulator that publishes JSON temperature readings to MQTT.

import paho.mqtt.client as mqtt
import time
import random
import json
import argparse

parser = argparse.ArgumentParser(description="Simulated temperature sensor (demo).")
parser.add_argument("--broker", default="localhost", help="MQTT broker host")
parser.add_argument("--topic", default="sensors/temperature1", help="MQTT topic")
parser.add_argument("--interval", type=float, default=3.0, help="Publish interval (s)")
args = parser.parse_args()

client = mqtt.Client(client_id="sensor_demo_1")
client.connect(args.broker, 1883, 60)

try:
    while True:
        temperature = round(random.uniform(18.0, 25.0), 2)
        payload = {
            "device_id": "sensor_demo_1",
            "timestamp": int(time.time()),
            "temperature": temperature
        }
        client.publish(args.topic, json.dumps(payload))
        print(f"[SENSOR] Published to {args.topic}: {payload}")
        time.sleep(args.interval)
except KeyboardInterrupt:
    print("Exiting sensor.")
    client.disconnect()
