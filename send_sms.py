"""
send_sms.py
Sends spike alert SMS via Twilio.
Only fires on spike events (not daily digest).
"""

import logging
from twilio.rest import Client

logger = logging.getLogger(__name__)


def send_spike_sms(spikes, phase_phone_list, config):
    """
    Send spike alert SMS to affected-phase residents who opted in.
    phase_phone_list: dict of { phase_id: ['+1XXXXXXXXXX', ...] }
    """
    if not spikes:
        return

    client = Client(
        config["sms"]["account_sid"],
        config["sms"]["auth_token"],
    )
    from_number = config["sms"]["from_number"]
    prop_short = "Foundry WP"

    affected_phases = set(s["phase_id"] for s in spikes)

    for spike in spikes:
        phase_id = spike["phase_id"]
        phase_name = spike["phase_name"]

        if spike["type"] == "daily":
            body = (
                f"[{prop_short}] Water spike in {phase_name}: "
                f"+{spike['pct_over']:.0f}% above normal yesterday. "
                f"Check for leaks. Reply STOP to opt out."
            )
        else:
            tag = "PERSISTENT " if spike.get("persistent") else ""
            body = (
                f"[{prop_short}] {tag}Water spike in {phase_name}: "
                f"{spike['current_gallons_per_hour']:.0f} gal/hr "
                f"(+{spike['pct_over']:.0f}% above avg). "
                f"Check for leaks. Reply STOP to opt out."
            )

        phones = phase_phone_list.get(phase_id, [])
        for phone in phones:
            try:
                msg = client.messages.create(
                    body=body,
                    from_=from_number,
                    to=phone,
                )
                logger.info(f"SMS sent to {phone}: SID {msg.sid}")
            except Exception as e:
                logger.error(f"SMS failed to {phone}: {e}")
