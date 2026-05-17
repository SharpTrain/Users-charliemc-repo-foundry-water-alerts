"""
validate_config.py
Asserts all required config fields are present and non-empty before any alert
job runs. Exit 1 on any failure so GitHub Actions fails fast with a clear message.
"""

import sys
import yaml


def validate(path="config.yaml"):
    errors = []

    try:
        with open(path) as f:
            c = yaml.safe_load(f)
    except Exception as e:
        print(f"FAIL: cannot load {path}: {e}")
        sys.exit(1)

    # Required top-level sections
    for section in ("property", "bluebot", "email", "sms", "thresholds"):
        if section not in c:
            errors.append(f"Missing top-level section: {section}")

    # BlueBot phases — each must have daily_gallon_limit
    phases = c.get("bluebot", {}).get("phases", [])
    if not phases:
        errors.append("bluebot.phases is empty or missing")
    for p in phases:
        name = p.get("name", p.get("id", "unknown"))
        if not p.get("daily_gallon_limit"):
            errors.append(f"Phase '{name}' is missing daily_gallon_limit")
        if not p.get("unit_count"):
            errors.append(f"Phase '{name}' is missing unit_count")

    # Credentials — must be non-empty (GitHub Actions may inject blank if secret unset)
    if not c.get("bluebot", {}).get("api_key", "").strip():
        errors.append("bluebot.api_key is blank (BLUEBOT_API_KEY secret may be unset)")
    if not c.get("email", {}).get("app_password", "").strip():
        errors.append("email.app_password is blank (GMAIL_APP_PASSWORD secret may be unset)")
    if not c.get("sms", {}).get("account_sid", "").strip():
        errors.append("sms.account_sid is blank (TWILIO_ACCOUNT_SID secret may be unset)")

    # always_notify must have at least one address
    always = c.get("email", {}).get("always_notify", [])
    if not always:
        errors.append("email.always_notify is empty — no board recipients configured")

    if errors:
        print("Config validation FAILED:")
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)

    print(f"Config OK — {len(phases)} phase(s), limits: " +
          ", ".join(f"{p['name']}={p['daily_gallon_limit']:,} gal" for p in phases))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()
    validate(args.config)
