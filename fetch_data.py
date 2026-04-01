"""
fetch_data.py
Pulls usage data from the BlueBot API.
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
        "Authorization": f"Bearer {config['bluebot']['api_key']}",
        "Content-Type": "application/json",
    }


def get_yesterday_usage(config):
    """
    Fetch yesterday's total usage per phase.
    Returns: dict of { phase_id: { 'name': ..., 'gallons': ..., 'unit_count': ... } }
    """
    tz = pytz.timezone(config["property"]["timezone"])
    now = datetime.now(tz)
    yesterday = now - timedelta(days=1)
    start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)

    results = {}
    base_url = config["bluebot"]["base_url"]

    for phase in config["bluebot"]["phases"]:
        try:
            url = f"{base_url}/usage/historical"
            params = {
                "device_id": phase["id"],
                "start": start.isoformat(),
                "end": end.isoformat(),
                "interval": "day",
            }
            resp = requests.get(url, headers=get_headers(config), params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            # Adapt this key based on actual BlueBot response shape
            gallons = data.get("total_gallons") or data.get("usage") or 0

            results[phase["id"]] = {
                "name": phase["name"],
                "gallons": gallons,
                "unit_count": phase["unit_count"],
                "date": yesterday.strftime("%Y-%m-%d"),
            }
            logger.info(f"Fetched yesterday: Phase {phase['name']} = {gallons} gal")
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
    Fetch the last N hours of usage for spike detection.
    Returns: dict of { phase_id: [ { 'timestamp': ..., 'gallons': ... }, ... ] }
    """
    tz = pytz.timezone(config["property"]["timezone"])
    now = datetime.now(tz)
    start = now - timedelta(hours=hours)

    results = {}
    base_url = config["bluebot"]["base_url"]

    for phase in config["bluebot"]["phases"]:
        try:
            url = f"{base_url}/usage/historical"
            params = {
                "device_id": phase["id"],
                "start": start.isoformat(),
                "end": now.isoformat(),
                "interval": "hour",
            }
            resp = requests.get(url, headers=get_headers(config), params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            # Adapt based on actual BlueBot response — usually a list of { timestamp, value }
            readings = data.get("readings") or data.get("data") or []
            results[phase["id"]] = {
                "name": phase["name"],
                "readings": readings,
            }
        except Exception as e:
            logger.error(f"Failed to fetch hourly for phase {phase['name']}: {e}")
            results[phase["id"]] = {"name": phase["name"], "readings": [], "error": str(e)}

    return results


def get_30day_baseline(config):
    """
    Fetch 30 days of daily totals to compute a rolling average per phase.
    Returns: dict of { phase_id: { 'avg_daily_gallons': float, 'avg_hourly_gallons': float } }
    """
    tz = pytz.timezone(config["property"]["timezone"])
    now = datetime.now(tz)
    start = now - timedelta(days=30)

    baselines = {}
    base_url = config["bluebot"]["base_url"]

    for phase in config["bluebot"]["phases"]:
        try:
            url = f"{base_url}/usage/historical"
            params = {
                "device_id": phase["id"],
                "start": start.isoformat(),
                "end": now.isoformat(),
                "interval": "day",
            }
            resp = requests.get(url, headers=get_headers(config), params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            readings = data.get("readings") or data.get("data") or []
            if readings:
                values = [r.get("gallons") or r.get("value") or 0 for r in readings]
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
