# Smart Temperature Sensor — IKT214 Project

Simulation + security assessment of an IoT temperature monitoring system.

## Overview
- MQTT broker (Eclipse Mosquitto)
- Sensor simulator (publishes JSON temperature readings)
- Dashboard (subscriber prints readings)
- Attacker script (demonstrates security vulnerabilities)
- Two versions: **Insecure** (no authentication) and **Secure** (with authentication)

## Quick Comparison: Insecure vs Secure

| Feature | Insecure Version | Secure Version |
|---------|-----------------|----------------|
| Authentication | ❌ None (anyone can connect) | ✅ Username/password required |
| Attacker Script | ✅ Works (can inject fake data) | ❌ Blocked (connection refused) |
| Use Case | Demonstrates vulnerabilities | Demonstrates security |

**Key Demonstration:**
- **Insecure**: Run `python attacker/attacker.py` → Attack succeeds
- **Secure**: Run `python attacker/attacker.py` → Attack fails (blocked)

## Quick Start Guide

### Complete Test Scenario: Insecure → Secure

**Test 1: Insecure Version (Vulnerable)**
1. Start insecure broker: `docker-compose -f docker-compose.insecure.yml up -d`
2. Run sensor: `python sensor/sensor.py`
3. Run dashboard: `python dashboard/dashboard.py --username "" --password ""`
4. Run attacker: `python attacker/attacker.py` → **SUCCESS** (attack works!)

**Test 2: Secure Version (Protected)**
1. Stop insecure: `docker-compose -f docker-compose.insecure.yml down`
2. Start secure broker: `docker-compose -f docker-compose.secure.yml up -d`
3. Run secure sensor: `python sensor/secure_sensor.py` (use: user/123456)
4. Run dashboard: `python dashboard/dashboard.py` (use: user/123456)
5. Run attacker: `python attacker/attacker.py` → **BLOCKED** (attack fails!)

## Prerequisites

- Docker and Docker Compose
- Python 3.6+
- Required Python packages: `paho-mqtt`, `bcrypt`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Standard Login Credentials (Secure Version)

- **Username**: `user`
- **Password**: `123456`

## How to Run the Program

### Option 1: Insecure Version (No Authentication)

This version demonstrates security vulnerabilities by allowing anyone to connect without authentication.

#### Step 1: Start the MQTT Broker
```bash
docker-compose -f docker-compose.insecure.yml up -d
```

#### Step 2: Run the Sensor
In a terminal, run:
```bash
python sensor/sensor.py
```

The sensor will start publishing temperature data every 3 seconds.

#### Step 3: Run the Dashboard
In another terminal, run:
```bash
python dashboard/dashboard.py --username "" --password ""
```

You should see temperature readings appearing in the dashboard.

#### Step 4: Demonstrate Attack (Shows Vulnerability)
In a third terminal, run the attacker script to inject fake data:
```bash
python attacker/attacker.py
```

**What happens:**
- The attacker script successfully connects (no authentication required)
- It publishes fake temperature data:
  - Low temperature (15.0°C) to hide overheating
  - High temperature spike (90.0°C) to create false alarms
- You will see these fake readings appear in your dashboard
- This demonstrates the **data injection/forgery vulnerability**

**Expected output:**
```
[ATTACK] Sent fake low: {'device_id': 'sensor_demo_1', 'timestamp': ..., 'temperature': 15.0}
[ATTACK] Sent fake spike: {'device_id': 'sensor_demo_1', 'timestamp': ..., 'temperature': 90.0}
```

**In the dashboard**, you will see both real sensor data and fake attacker data mixed together, showing how an attacker can manipulate the system.

#### Stop the Broker
```bash
docker-compose -f docker-compose.insecure.yml down
```

---

### Option 2: Secure Version (With Authentication)

This version requires username/password authentication to connect.

#### Step 1: Start the MQTT Broker
```bash
docker-compose -f docker-compose.secure.yml up -d
```

#### Step 2: Run the Sensor
In a terminal, run:
```bash
python sensor/secure_sensor.py
```

When prompted:
- **Username**: `user`
- **Password**: `123456`

Or provide credentials directly:
```bash
python sensor/secure_sensor.py --username user --password 123456
```

#### Step 3: Run the Dashboard
In another terminal, run:
```bash
python dashboard/dashboard.py
```

When prompted:
- Type `j` (or `y`/`yes`) to use authentication
- **Username**: `user`
- **Password**: `123456`

Or provide credentials directly:
```bash
python dashboard/dashboard.py --username user --password 123456
```

#### Step 4: Test Security (Attacker Blocked)
In a third terminal, try to run the attacker script:
```bash
python attacker/attacker.py
```

**What happens:**
- The attacker script tries to connect without authentication
- Connection is **rejected**: `Client attacker_sim disconnected, not authorised`
- The attacker **cannot** publish fake data
- This demonstrates that authentication **prevents** the attack

**Expected output in broker logs:**
```
Sending CONNACK to attacker_sim (0, 5)
Client attacker_sim disconnected, not authorised.
```

**In contrast to insecure version:** The secure version successfully blocks unauthorized access attempts.

#### Stop the Broker
```bash
docker-compose -f docker-compose.secure.yml down
```

---

## Web Dashboard

You can also use a web-based dashboard in your browser.

### Step 1: Start the Broker
Choose either insecure or secure version:
```bash
# Insecure version
docker-compose -f docker-compose.insecure.yml up -d

# OR secure version
docker-compose -f docker-compose.secure.yml up -d
```

### Step 2: Start HTTP Server
In the project root directory, run:
```bash
# Python 3
python -m http.server 8000

# OR if you have Node.js
npx http-server -p 8000
```

### Step 3: Open in Browser
Navigate to:
```
http://localhost:8000/dashboard/web_dashboard.html
```

### Step 4: Connect
- **For insecure version**: Leave Username and Password empty
  - Broker (WebSocket): `ws://localhost:9001`
  - Topic: `sensors/#`
  - Click "Connect"

- **For secure version**: Fill in credentials
  - Broker (WebSocket): `ws://localhost:9001`
  - Username: `user`
  - Password: `123456`
  - Topic: `sensors/#`
  - Click "Connect"

### Step 5: Start Sensor
Run the sensor (insecure or secure version) to see data appear in the web dashboard.

---

## Changing Username and Password

To change the default credentials:

### Step 1: Create New Password File
```bash
docker run --rm -v ${PWD}/mosquitto.conf:/mosquitto/config eclipse-mosquitto:2.0 mosquitto_passwd -b -c /mosquitto/config/password.txt <username> <password>
```

Example:
```bash
docker run --rm -v ${PWD}/mosquitto.conf:/mosquitto/config eclipse-mosquitto:2.0 mosquitto_passwd -b -c /mosquitto/config/password.txt myuser mypassword
```

### Step 2: Restart Broker
```bash
docker-compose -f docker-compose.secure.yml restart
```

### Step 3: Use New Credentials
When running the sensor or dashboard, use the new credentials:
```bash
python sensor/secure_sensor.py --username myuser --password mypassword
python dashboard/dashboard.py --username myuser --password mypassword
```

---

## Using Environment Variables

You can also set credentials using environment variables:

**Windows PowerShell:**
```powershell
$env:MQTT_USER="myuser"
$env:MQTT_PASS="mypassword"
python sensor/secure_sensor.py
```

**Linux/Mac:**
```bash
export MQTT_USER=myuser
export MQTT_PASS=mypassword
python sensor/secure_sensor.py
```

---

## Project Structure

```
smart-temperature-iot/
├── sensor/
│   ├── sensor.py              # Insecure sensor (no auth)
│   └── secure_sensor.py        # Secure sensor (with auth)
├── dashboard/
│   ├── dashboard.py            # Command-line dashboard
│   └── web_dashboard.html      # Web-based dashboard
├── attacker/
│   └── attacker.py             # Attack demonstration script
├── mosquitto.conf/
│   ├── mosquitto.conf          # Insecure broker config
│   ├── mosquitto_secure.conf   # Secure broker config
│   └── password.txt            # Password file (secure version)
├── docker-compose.yml          # Default (insecure)
├── docker-compose.insecure.yml # Insecure version
├── docker-compose.secure.yml   # Secure version
└── requirements.txt            # Python dependencies
```

---

## Troubleshooting

### Broker won't start
- Check if port 1883 or 9001 is already in use
- Ensure Docker is running
- Check logs: `docker logs mqtt-broker`

### Connection refused
- Make sure the broker is running: `docker ps`
- Verify you're using the correct version (secure/insecure)
- Check firewall settings

### Authentication fails
- Verify username and password are correct
- Ensure you're using the secure version: `docker-compose -f docker-compose.secure.yml up -d`
- Check password file exists: `mosquitto.conf/password.txt`

### Web dashboard not connecting
- Ensure WebSocket port 9001 is accessible
- Check broker logs for WebSocket errors
- Verify you're using the correct credentials for secure version

---

## Stopping Everything

To stop all services:
```bash
docker-compose down
# or specifically
docker-compose -f docker-compose.insecure.yml down
docker-compose -f docker-compose.secure.yml down
```
