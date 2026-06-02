"""
detect_spikes.py
Determines which 250-gallon threshold bands have been newly crossed today.

Each phase fires an alert at its daily_gallon_limit, then again at every
additional increment_gallons above that (default 250 gal).

  Phase 1 (1,750 limit): alerts at 1750, 2000, 2250, 2500 ...
  Phase 2 (2,650 limit): alerts at 2650, 2900, 3150, 3400 ...
"""

import logging

logger = logging.getLogger(__name__)

_DEFAULT_INCREMENT = 250


def get_crossed_thresholds(gallons, base_limit, increment=_DEFAULT_INCREMENT):
    """Return sorted list of every gallon threshold crossed (base_limit, +increment, +2×, ...)."""
    if gallons < base_limit:
        return []
    count = int((gallons - base_limit) / increment) + 1
    return [base_limit + i * increment for i in range(count)]


def check_new_threshold_crossings(today_usage, config, alerted_thresholds):
    """
    For each phase, return spike dicts for thresholds crossed but not yet alerted today.

    today_usage:       output of fetch_data.get_today_totals()
    config:            loaded config.yaml dict
    alerted_thresholds: { phase_id: [gallon levels already alerted today] }

    Returns list of spike dicts, one per phase that has new crossings.
    """
    increment = config.get("thresholds", {}).get("increment_gallons", _DEFAULT_INCREMENT)
    results = []

    for phase in config["bluebot"]["phases"]:
        phase_id = phase["id"]
        base_limit = phase.get("daily_gallon_limit")
        if not base_limit:
            logger.warning(f"No daily_gallon_limit configured for {phase.get('name')}, skipping")
            continue

        data = today_usage.get(phase_id, {})
        if data.get("error") or data.get("gallons") is None:
            continue

        gallons = data["gallons"]
        crossed = get_crossed_thresholds(gallons, base_limit, increment)
        already = set(alerted_thresholds.get(phase_id, []))
        new = [t for t in crossed if t not in already]

        if new:
            results.append({
                "phase_id": phase_id,
                "phase_name": data["name"],
                "gallons_today": gallons,
                "daily_limit": base_limit,
                "gallons_over": gallons - base_limit,
                "unit_count": data["unit_count"],
                "per_unit_gallons": gallons / data["unit_count"] if data["unit_count"] else 0,
                "threshold_hit": max(new),
                "new_thresholds": sorted(new),
                "increment": increment,
            })
            logger.warning(
                f"NEW THRESHOLD(S) crossed — {data['name']}: "
                f"{gallons:.0f} gal today, new bands: {sorted(new)}"
            )

    return results
