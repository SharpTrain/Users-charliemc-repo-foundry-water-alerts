"""
detect_spikes.py
Compares today's running total against each phase's fixed daily gallon limit.
"""

import logging

logger = logging.getLogger(__name__)


def check_daily_total_threshold(today_usage, config):
    """
    Compare today's running total against each phase's daily_gallon_limit.
    Returns list of spike dicts for phases that have exceeded their limit.
    """
    limits = {p["id"]: p.get("daily_gallon_limit") for p in config["bluebot"]["phases"]}
    spikes = []

    for phase_id, data in today_usage.items():
        if data.get("error") or data.get("gallons") is None:
            continue

        limit = limits.get(phase_id)
        if not limit:
            logger.warning(f"No daily_gallon_limit configured for {data['name']}, skipping")
            continue

        gallons = data["gallons"]
        if gallons >= limit:
            spikes.append({
                "phase_id": phase_id,
                "phase_name": data["name"],
                "type": "daily_total",
                "gallons_today": gallons,
                "daily_limit": limit,
                "gallons_over": gallons - limit,
                "unit_count": data["unit_count"],
                "per_unit_gallons": gallons / data["unit_count"] if data["unit_count"] else 0,
            })
            logger.warning(
                f"DAILY LIMIT EXCEEDED: {data['name']} used {gallons:.0f} gal today "
                f"(limit: {limit:,} gal, over by {gallons - limit:.0f} gal)"
            )

    return spikes
