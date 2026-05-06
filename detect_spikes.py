"""
detect_spikes.py
Compares current usage against baselines and flags spikes.
"""

import logging

logger = logging.getLogger(__name__)


def check_daily_spike(yesterday_usage, baselines, config):
    """
    Compare yesterday's totals to 30-day average.
    Returns list of spike dicts for phases that exceeded threshold.
    """
    threshold = config["thresholds"]["spike_daily_pct"]
    spikes = []

    for phase_id, data in yesterday_usage.items():
        if data.get("error") or data.get("gallons") is None:
            continue

        baseline = baselines.get(phase_id, {})
        avg = baseline.get("avg_daily_gallons", 0)

        if avg == 0:
            logger.warning(f"No baseline for {data['name']}, skipping spike check")
            continue

        ratio = data["gallons"] / avg
        pct_over = (ratio - 1) * 100

        if ratio >= threshold:
            spikes.append({
                "phase_id": phase_id,
                "phase_name": data["name"],
                "type": "daily",
                "gallons": data["gallons"],
                "avg_gallons": avg,
                "ratio": ratio,
                "pct_over": pct_over,
                "unit_count": data["unit_count"],
                "per_unit_gallons": data["gallons"] / data["unit_count"],
                "date": data.get("date"),
            })
            logger.warning(
                f"DAILY SPIKE: {data['name']} used {data['gallons']:.0f} gal "
                f"({pct_over:.1f}% over avg of {avg:.0f} gal)"
            )

    return spikes


def check_hourly_spike(recent_hourly, baselines, config):
    """
    Check the most recent hour against hourly average.
    Returns list of spike dicts.
    """
    threshold = config["thresholds"]["spike_hourly_pct"]
    persistent_min = config["thresholds"]["persistent_hours"]
    spikes = []

    for phase_id, data in recent_hourly.items():
        if data.get("error") or not data.get("readings"):
            continue

        baseline = baselines.get(phase_id, {})
        avg_hourly = baseline.get("avg_hourly_gallons", 0)

        if avg_hourly == 0:
            continue

        readings = data["readings"]
        # Check most recent hour
        latest = readings[-1] if readings else None
        if not latest:
            continue

        current_val = latest.get("total") or latest.get("gallons") or latest.get("value") or 0
        ratio = current_val / avg_hourly if avg_hourly > 0 else 0
        pct_over = (ratio - 1) * 100

        # Count consecutive above-threshold hours
        consecutive = 0
        for r in reversed(readings):
            val = r.get("total") or r.get("gallons") or r.get("value") or 0
            if val / avg_hourly >= threshold:
                consecutive += 1
            else:
                break

        is_spike = ratio >= threshold
        is_persistent = consecutive >= persistent_min

        if is_spike:
            spikes.append({
                "phase_id": phase_id,
                "phase_name": data["name"],
                "type": "hourly" if not is_persistent else "persistent",
                "current_gallons_per_hour": current_val,
                "avg_gallons_per_hour": avg_hourly,
                "ratio": ratio,
                "pct_over": pct_over,
                "consecutive_hours": consecutive,
                "persistent": is_persistent,
            })
            logger.warning(
                f"{'PERSISTENT ' if is_persistent else ''}HOURLY SPIKE: "
                f"{data['name']} {current_val:.0f} gph vs avg {avg_hourly:.0f} gph "
                f"({pct_over:.1f}% over)"
            )

    return spikes
