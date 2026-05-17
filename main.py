"""
main.py
Entry point. Run with:
  python main.py --mode daily    # Morning digest (run once at 5-6 AM)
  python main.py --mode spike    # Daily total check (run every 15 min)
  python main.py --mode test     # Send test email/SMS to board only
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
import pytz

from fetch_data import load_config, get_yesterday_usage, get_today_totals, get_30day_baseline
from detect_spikes import check_daily_total_threshold
from send_email import send_daily_digest, send_spike_alert, send_today_digest
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

STATE_FILE = "alert_state.json"
FOLLOWUP_INTERVAL_HOURS = 2.5


def _load_alert_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"alerted_on": {}}


def _save_alert_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save alert state: {e}")


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
    logger.info("=== Running DAILY TOTAL check ===")

    if is_quiet_hours(config):
        logger.info("Quiet hours — skipping check.")
        return

    tz = pytz.timezone(config["property"]["timezone"])
    now = datetime.now(tz)
    now_utc = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    state = _load_alert_state()
    alerted_on = state.get("alerted_on", {})
    last_alert_time = state.get("last_alert_time", {})

    today_usage = get_today_totals(config)
    all_triggers = check_daily_total_threshold(today_usage, config)

    new_spikes = []
    followup_spikes = []

    for s in all_triggers:
        pid = s["phase_id"]
        if alerted_on.get(pid) != today:
            new_spikes.append(s)
        else:
            last_t_str = last_alert_time.get(pid)
            if last_t_str:
                last_t = datetime.fromisoformat(last_t_str)
                elapsed_hours = (now_utc - last_t).total_seconds() / 3600
                if elapsed_hours >= FOLLOWUP_INTERVAL_HOURS:
                    followup_spikes.append(s)
                    logger.info(
                        f"{s['phase_name']}: {elapsed_hours:.1f}h since last alert — queuing follow-up"
                    )

    if new_spikes:
        logger.warning(f"Daily limit exceeded (initial alert): {[s['phase_name'] for s in new_spikes]}")
        _, emails_by_phase = load_email_list()
        _, phones_by_phase = load_sms_list()
        send_spike_alert(new_spikes, emails_by_phase, config)
        send_spike_sms(new_spikes, phones_by_phase, config)
        for s in new_spikes:
            alerted_on[s["phase_id"]] = today
            last_alert_time[s["phase_id"]] = now_utc.isoformat()

    if followup_spikes:
        logger.warning(f"Still over limit (follow-up): {[s['phase_name'] for s in followup_spikes]}")
        _, emails_by_phase = load_email_list()
        _, phones_by_phase = load_sms_list()
        send_spike_alert(followup_spikes, emails_by_phase, config, is_followup=True)
        send_spike_sms(followup_spikes, phones_by_phase, config, is_followup=True)
        for s in followup_spikes:
            last_alert_time[s["phase_id"]] = now_utc.isoformat()

    if not new_spikes and not followup_spikes:
        if all_triggers:
            logger.info(
                f"Over limit but follow-up not due yet: {[s['phase_name'] for s in all_triggers]}"
            )
        else:
            logger.info("No daily limits exceeded.")

    state["alerted_on"] = alerted_on
    state["last_alert_time"] = last_alert_time
    _save_alert_state(state)


def run_today(config):
    """Send an evening digest of today's running totals to all board members."""
    logger.info("=== Running TODAY summary ===")
    today_usage = get_today_totals(config)
    all_emails, _ = load_email_list()
    send_today_digest(today_usage, all_emails, config)
    logger.info("Today's summary sent.")


def run_test(config):
    """Send a test daily-limit alert to board only — use this to verify credentials."""
    logger.info("=== Running TEST mode ===")
    phase = config["bluebot"]["phases"][0]
    limit = phase.get("daily_gallon_limit", 2000)
    fake_spikes = [
        {
            "phase_id": phase["id"],
            "phase_name": phase["name"],
            "type": "daily_total",
            "gallons_today": int(limit * 1.15),
            "daily_limit": limit,
            "gallons_over": int(limit * 0.15),
            "unit_count": phase["unit_count"],
            "per_unit_gallons": int(limit * 1.15) / phase["unit_count"],
        }
    ]

    send_spike_alert(fake_spikes, {}, config)
    logger.info(f"Test spike alert sent to: {config['email']['always_notify']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["daily", "spike", "today", "test"],
        required=True,
        help="daily = morning digest, spike = 15-min check, today = evening summary, test = send test alert",
    )
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.mode == "daily":
        run_daily(config)
    elif args.mode == "spike":
        run_spike_check(config)
    elif args.mode == "today":
        run_today(config)
    elif args.mode == "test":
        run_test(config)


if __name__ == "__main__":
    main()
