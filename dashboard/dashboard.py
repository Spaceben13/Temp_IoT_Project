#!/usr/bin/env python3
# dashboard/dashboard.py
# Simple subscriber that prints incoming sensor messages.

import paho.mqtt.client as mqtt
import json
import argparse
import getpass

parser = argparse.ArgumentParser(description="Dashboard/Subscriber for sensor topics.")
parser.add_argument("--broker", default="localhost", help="MQTT broker host")
parser.add_argument("--topic", default="sensors/#", help="Topic filter")
parser.add_argument("--username", default=None, nargs='?', const="", help="MQTT username (tom for usikker versjon, spør interaktivt hvis ikke oppgitt)")
parser.add_argument("--password", default=None, nargs='?', const="", help="MQTT password (tom for usikker versjon, spør interaktivt hvis ikke oppgitt)")
args = parser.parse_args()

# Håndter tomme strenger fra kommandolinjen
if args.username == "" or args.password == "":
    args.username = None
    args.password = None
# Hvis brukernavn/passord ikke er oppgitt og ikke eksplisitt tomt, spør interaktivt
elif args.username is None and args.password is None:
    use_auth = input("Bruke autentisering? (j/n): ").strip().lower()
    if use_auth == 'j' or use_auth == 'ja' or use_auth == 'y' or use_auth == 'yes':
        args.username = input("Brukernavn: ").strip() or "sensor1"
        args.password = getpass.getpass("Passord: ") or "sensorpass"
    else:
        args.username = None
        args.password = None

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

# Set up authentication (kun hvis brukernavn og passord er oppgitt)
if args.username and args.password:
    client.username_pw_set(args.username, args.password)
    print(f"Using authentication: username={args.username}")
else:
    print("No authentication (usikker versjon)")

client.connect(args.broker, 1883, 60)
client.loop_forever()
