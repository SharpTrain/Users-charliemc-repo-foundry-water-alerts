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

        body = (
            f"[{prop_short}] {phase_name} hit daily water limit: "
            f"{spike['gallons_today']:,.0f} gal used "
            f"({spike['gallons_over']:,.0f} over {spike['daily_limit']:,} gal limit). "
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
