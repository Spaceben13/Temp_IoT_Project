#!/usr/bin/env python3
"""
Script for å opprette Mosquitto passordfil.
Bruker bcrypt for å hashe passord på samme måte som mosquitto_passwd.
"""
import bcrypt
import sys
import os

def create_password_file(username, password, output_file):
    """Oppretter en Mosquitto passordfil med hashet passord."""
    # Hash passordet med bcrypt (samme som mosquitto_passwd bruker)
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Skriv til fil i formatet: username:hashed_password
    with open(output_file, 'w') as f:
        f.write(f"{username}:{hashed.decode('utf-8')}\n")
    
    print(f"Passordfil opprettet: {output_file}")
    print(f"Brukernavn: {username}")
    print(f"Passord: {password}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Bruk: python create_password_file.py <brukernavn> <passord> [output_fil]")
        print("Eksempel: python create_password_file.py sensor1 mittpassord mosquitto.conf/password.txt")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "mosquitto.conf/password.txt"
    
    # Sjekk om output directory eksisterer
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    create_password_file(username, password, output_file)

