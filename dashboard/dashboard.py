#!/usr/bin/env python3
# dashboard/dashboard.py
# Simple subscriber that prints incoming sensor messages.

import paho.mqtt.client as mqtt
import json
import argparse

parser = argparse.ArgumentParser(description="Dashboard/Subscriber for sensor topics.")
parser.add_argument("--broker", default="localhost", help="MQTT broker host")
parser.add_argument("--topic", default="sensors/#", help="Topic filter")
args = parser.parse_args()

def on_connect(client, userdata, flags, rc):
    print("Connected to broker, subscribing to:", args.topic)
    client.subscribe(args.topic)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
    except Exception:
        data = msg.payload.decode()
    print(f"[DASHBOARD] {msg.topic} -> {data}")

client = mqtt.Client(client_id="dashboard_1")
client.on_connect = on_connect
client.on_message = on_message

client.connect(args.broker, 1883, 60)
client.loop_forever()
