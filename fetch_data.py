"""
fetch_data.py
Pulls usage data from the BlueBot Flow API v2.

API base: https://prod.bluebot.com/flow/v2
Auth:     bluebot-api-key: <VALUE_AFTER_DOT>
Params:   range_start / range_end as Unix timestamps (seconds)
Meter serial is passed as a path segment, not a query param.
"""

import requests
import yaml
from datetime import datetime, timedelta
import pytz
import logging

logger = logging.getLogger(__name__)


def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def get_headers(config):
    return {
        "bluebot-api-key": config["bluebot"]["api_key"],
        "Content-Type": "application/json",
    }


def _to_unix(dt):
    """Convert a timezone-aware datetime to a Unix timestamp (seconds)."""
    return int(dt.timestamp())


def get_yesterday_usage(config):
    """
    Fetch yesterday's total daily usage per phase.
    Uses /total/daily-tz/{meter_serial} so day boundaries respect the
    meter's local timezone.
    Returns: dict of { phase_id: { 'name', 'gallons', 'unit_count', 'date' } }
    """
    tz = pytz.timezone(config["property"]["timezone"])
    now = datetime.now(tz)
    yesterday = now - timedelta(days=1)
    start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)

    results = {}
    base_url = config["bluebot"]["base_url"]

    for phase in config["bluebot"]["phases"]:
        meter = phase["id"]
        try:
            url = f"{base_url}/total/daily-tz/{meter}"
            params = {
                "range_start": _to_unix(start),
                "range_end": _to_unix(end),
            }
            resp = requests.get(url, headers=get_headers(config), params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            # BlueBot returns a list of { timestamp, value/gallons } records
            readings = data if isinstance(data, list) else (data.get("data") or data.get("readings") or [])
            gallons = sum(r.get("total") or r.get("gallons") or r.get("value") or 0 for r in readings)

            results[phase["id"]] = {
                "name": phase["name"],
                "gallons": gallons,
                "unit_count": phase["unit_count"],
                "date": yesterday.strftime("%Y-%m-%d"),
            }
            logger.info(f"Fetched yesterday: Phase {phase['name']} = {gallons:.0f} gal")
        except Exception as e:
            logger.error(f"Failed to fetch yesterday for phase {phase['name']}: {e}")
            results[phase["id"]] = {
                "name": phase["name"],
                "gallons": None,
                "unit_count": phase["unit_count"],
                "date": yesterday.strftime("%Y-%m-%d"),
                "error": str(e),
            }

    return results


def get_recent_hourly(config, hours=4):
    """
    Fetch the last N hours of hourly usage for spike detection.
    Uses /total/hourly/{meter_serial}.
    Returns: dict of { phase_id: { 'name', 'readings': [...] } }
    """
    tz = pytz.timezone(config["property"]["timezone"])
    now = datetime.now(tz)
    start = now - timedelta(hours=hours)

    results = {}
    base_url = config["bluebot"]["base_url"]

    for phase in config["bluebot"]["phases"]:
        meter = phase["id"]
        try:
            url = f"{base_url}/total/hourly/{meter}"
            params = {
                "range_start": _to_unix(start),
                "range_end": _to_unix(now),
            }
            resp = requests.get(url, headers=get_headers(config), params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            readings = data if isinstance(data, list) else (data.get("data") or data.get("readings") or [])
            results[phase["id"]] = {
                "name": phase["name"],
                "readings": readings,
            }
            logger.info(f"Fetched hourly: Phase {phase['name']} = {len(readings)} records")
        except Exception as e:
            logger.error(f"Failed to fetch hourly for phase {phase['name']}: {e}")
            results[phase["id"]] = {"name": phase["name"], "readings": [], "error": str(e)}

    return results


def get_30day_baseline(config):
    """
    Fetch 30 days of daily totals to compute a rolling average per phase.
    Uses /total/daily/{meter_serial}.
    Returns: dict of { phase_id: { 'avg_daily_gallons', 'avg_hourly_gallons' } }
    """
    tz = pytz.timezone(config["property"]["timezone"])
    now = datetime.now(tz)
    start = now - timedelta(days=30)

    baselines = {}
    base_url = config["bluebot"]["base_url"]

    for phase in config["bluebot"]["phases"]:
        meter = phase["id"]
        try:
            url = f"{base_url}/total/daily/{meter}"
            params = {
                "range_start": _to_unix(start),
                "range_end": _to_unix(now),
            }
            resp = requests.get(url, headers=get_headers(config), params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            readings = data if isinstance(data, list) else (data.get("data") or data.get("readings") or [])
            if readings:
                values = [r.get("total") or r.get("gallons") or r.get("value") or 0 for r in readings]
                avg_daily = sum(values) / len(values)
            else:
                avg_daily = 0

            baselines[phase["id"]] = {
                "name": phase["name"],
                "avg_daily_gallons": avg_daily,
                "avg_hourly_gallons": avg_daily / 24,
            }
            logger.info(f"Baseline: Phase {phase['name']} avg daily = {avg_daily:.0f} gal")
        except Exception as e:
            logger.error(f"Failed to fetch baseline for phase {phase['name']}: {e}")
            baselines[phase["id"]] = {
                "name": phase["name"],
                "avg_daily_gallons": 0,
                "avg_hourly_gallons": 0,
                "error": str(e),
            }

    return baselines
