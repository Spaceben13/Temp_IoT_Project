#!/usr/bin/env python3
"""tools/collect_messages.py
Subscribe to a topic and collect N messages, then exit.
"""
import paho.mqtt.client as mqtt
import argparse
import json

parser = argparse.ArgumentParser(description="Collect N MQTT messages and exit")
parser.add_argument("--broker", default="localhost")
parser.add_argument("--topic", default="sensors/#")
parser.add_argument("--count", type=int, default=6)
args = parser.parse_args()

collected = []

def on_connect(client, userdata, flags, rc):
    print(f"Connected, subscribing to {args.topic}")
    client.subscribe(args.topic)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except Exception:
        payload = msg.payload.decode(errors='replace')
    entry = {"topic": msg.topic, "payload": payload}
    collected.append(entry)
    print(f"[COLLECTED] {entry}")
    if len(collected) >= args.count:
        client.disconnect()

client = mqtt.Client(client_id="collector_1")
client.on_connect = on_connect
client.on_message = on_message

client.connect(args.broker, 1883, 60)
client.loop_forever()

print("Done. Collected messages:")
for m in collected:
    print(m)
