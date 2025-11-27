# Praktisk Implementasjon - Sjekkliste ✅

## ✅ Alle praktiske krav er fullført!

### 1. IoT System - Implementert ✅
- [x] MQTT Broker (Eclipse Mosquitto) - Docker container
- [x] Temperature Sensor Simulator - Publiserer JSON data
- [x] Dashboard/Subscriber - Mottar og viser data
- [x] Attacker Script - Demonstrerer sårbarheter (data injection)

### 2. Sikker vs Usikker Versjon - Implementert ✅
- [x] **Usikker versjon**: 
  - Ingen autentisering
  - Tillater anonyme tilkoblinger
  - Demonstrerer sårbarheter
  - Attacker kan injisere falske data
  
- [x] **Sikker versjon**:
  - Username/password autentisering
  - Passordfil med hashede passord (PBKDF2)
  - Interaktiv passordinput
  - Fungerer korrekt

### 3. Bytte mellom Versjoner - Implementert ✅
- [x] PowerShell scripts (Windows)
- [x] Bash scripts (Linux/Mac)
- [x] Docker Compose konfigurasjoner
- [x] Enkel bytte mellom sikker/usikker

### 4. Testing - Fullført ✅
- [x] Usikker versjon testet og fungerer
- [x] Sikker versjon testet og fungerer
- [x] Attacker script demonstrerer sårbarheter
- [x] Dataflyt verifisert (sensor → broker → dashboard)

### 5. Konfigurasjon og Verktøy - Implementert ✅
- [x] Passordfil-generering (mosquitto_passwd)
- [x] Python script for passordfil-opprettelse
- [x] Docker Compose konfigurasjoner
- [x] README med instruksjoner

### 6. Funksjonalitet - Implementert ✅
- [x] Sensor publiserer temperaturdata
- [x] Dashboard mottar og viser data
- [x] Autentisering fungerer (sikker versjon)
- [x] Ingen autentisering (usikker versjon)
- [x] Attacker kan injisere falske data (usikker versjon)
- [x] Attacker blokkert (sikker versjon)

---

## 📊 Status: 100% Praktisk Implementasjon Fullført

**Alt det praktiske er ferdig!** 

Rapporten (dokumentasjon) kan nå skrives basert på:
- Den implementerte koden
- Testing-resultatene
- Sammenligningen mellom sikker/usikker versjon
- Demonstrasjonen av sårbarheter

---

## 📝 For Rapport (Dokumentasjon)

Dette skal dokumenteres i rapporten:
- Threat Modeling (basert på implementasjonen)
- Cryptography Evaluation (PBKDF2, manglende TLS)
- Protocol Analysis (MQTT sikkerhet)
- Security Recommendations (basert på funnene)

**Alt dette er dokumentasjon - ikke praktisk implementasjon!**

