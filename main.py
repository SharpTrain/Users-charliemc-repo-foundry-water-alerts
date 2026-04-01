"""
main.py
Entry point. Run with:
  python main.py --mode daily    # Morning digest (run once at 5-6 AM)
  python main.py --mode spike    # Spike check (run every 15 min)
  python main.py --mode test     # Send test email/SMS to board only
"""

import argparse
import logging
import sys
from datetime import datetime
import pytz

from fetch_data import load_config, get_yesterday_usage, get_recent_hourly, get_30day_baseline
from detect_spikes import check_daily_spike, check_hourly_spike
from send_email import send_daily_digest, send_spike_alert
from send_sms import send_spike_sms
from load_recipients import load_email_list, load_sms_list

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("alerts.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def is_quiet_hours(config):
    tz = pytz.timezone(config["property"]["timezone"])
    hour = datetime.now(tz).hour
    start = config["thresholds"]["quiet_hours_start"]
    end = config["thresholds"]["quiet_hours_end"]
    if start > end:
        return hour >= start or hour < end
    return start <= hour < end


def run_daily(config):
    logger.info("=== Running DAILY digest ===")
    baselines = get_30day_baseline(config)
    yesterday = get_yesterday_usage(config)

    all_emails, emails_by_phase = load_email_list()
    send_daily_digest(yesterday, baselines, all_emails, config)
    logger.info("Daily digest sent.")


def run_spike_check(config):
    logger.info("=== Running SPIKE check ===")

    if is_quiet_hours(config):
        logger.info("Quiet hours — skipping spike check.")
        return

    baselines = get_30day_baseline(config)
    recent = get_recent_hourly(config, hours=4)

    spikes = check_hourly_spike(recent, baselines, config)

    if spikes:
        logger.warning(f"Spikes detected: {[s['phase_name'] for s in spikes]}")
        _, emails_by_phase = load_email_list()
        _, phones_by_phase = load_sms_list()

        send_spike_alert(spikes, emails_by_phase, config)
        send_spike_sms(spikes, phones_by_phase, config)
    else:
        logger.info("No spikes detected.")


def run_test(config):
    """Send a fake spike alert to board only — use this to verify credentials."""
    logger.info("=== Running TEST mode ===")
    fake_spikes = [
        {
            "phase_id": config["bluebot"]["phases"][0]["id"],
            "phase_name": config["bluebot"]["phases"][0]["name"],
            "type": "hourly",
            "current_gallons_per_hour": 850,
            "avg_gallons_per_hour": 500,
            "ratio": 1.70,
            "pct_over": 70.0,
            "consecutive_hours": 1,
            "persistent": False,
        }
    ]

    board_emails = config["email"]["always_notify"]
    send_spike_alert(fake_spikes, {}, config)
    logger.info(f"Test spike alert sent to: {board_emails}")

    # Optionally test SMS (comment out if not ready)
    # board_phones = ["+1XXXXXXXXXX"]  # add your number here
    # send_spike_sms(fake_spikes, {fake_spikes[0]['phase_id']: board_phones}, config)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["daily", "spike", "test"],
        required=True,
        help="daily = morning digest, spike = real-time check, test = send test alert",
    )
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.mode == "daily":
        run_daily(config)
    elif args.mode == "spike":
        run_spike_check(config)
    elif args.mode == "test":
        run_test(config)


if __name__ == "__main__":
    main()
