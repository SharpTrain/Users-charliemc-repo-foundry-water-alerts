"""
load_recipients.py
Loads resident email and SMS lists from CSV files.

CSV format for emails (residents_email.csv):
  name,email,phase_id
  Jane Smith,jane@email.com,PHASE_1_ID
  John Doe,john@email.com,PHASE_1_ID

CSV format for SMS (residents_sms.csv):
  name,phone,phase_id
  Jane Smith,+13035550100,PHASE_1_ID
  John Doe,+13035550101,PHASE_1_ID
"""

import csv
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


def load_email_list(csv_path="residents_email.csv"):
    """
    Returns:
      all_emails: flat list of all email addresses
      by_phase:   dict { phase_id: [email, ...] }
    """
    all_emails = []
    by_phase = defaultdict(list)

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row["email"].strip()
            phase = row["phase_id"].strip()
            all_emails.append(email)
            by_phase[phase].append(email)

    logger.info(f"Loaded {len(all_emails)} email recipients from {csv_path}")
    return all_emails, dict(by_phase)


def load_sms_list(csv_path="residents_sms.csv"):
    """
    Returns:
      all_phones: flat list of all phone numbers
      by_phase:   dict { phase_id: [phone, ...] }
    """
    all_phones = []
    by_phase = defaultdict(list)

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            phone = row["phone"].strip()
            phase = row["phase_id"].strip()
            all_phones.append(phone)
            by_phase[phase].append(phone)

    logger.info(f"Loaded {len(all_phones)} SMS recipients from {csv_path}")
    return all_phones, dict(by_phase)
