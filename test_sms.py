"""
test_sms.py
Sends a test SMS to all recipients in residents_sms.csv.
Run with: python test_sms.py
"""

import csv
import yaml
from twilio.rest import Client

# Load config
with open("config.yaml") as f:
    config = yaml.safe_load(f)

client = Client(config["sms"]["account_sid"], config["sms"]["auth_token"])
from_number = config["sms"]["from_number"]

# Load recipients
with open("residents_sms.csv") as f:
    readers = list(csv.DictReader(f))

print(f"Sending test SMS to {len(readers)} recipients...\n")

for row in readers:
    name = row["name"]
    phone = row["phone"].strip()
    try:
        msg = client.messages.create(
            body="[Foundry WP] TEST — BlueBot water spike alert system is active. No action needed. Reply STOP to opt out.",
            from_=from_number,
            to=phone,
        )
        print(f"✓ Sent to {name} ({phone}) — SID: {msg.sid}")
    except Exception as e:
        print(f"✗ Failed to {name} ({phone}): {e}")

print("\nDone.")
