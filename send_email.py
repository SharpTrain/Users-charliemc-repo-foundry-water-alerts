"""
send_email.py
Sends daily digest and spike alert emails via Gmail SMTP.
"""

import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)


def _build_daily_digest_html(phase_data, baselines, config):
    tz = pytz.timezone(config["property"]["timezone"])
    date_str = datetime.now(tz).strftime("%A, %B %d, %Y")
    prop_name = config["property"]["name"]

    # Build limit lookup from config
    limits = {p["id"]: p.get("daily_gallon_limit") for p in config["bluebot"]["phases"]}

    rows = ""
    for phase_id, data in phase_data.items():
        if data.get("error"):
            rows += f"<tr><td>{data['name']}</td><td colspan='4'>Data unavailable</td></tr>"
            continue
        gallons = data.get("gallons", 0) or 0
        per_unit = gallons / data["unit_count"] if data["unit_count"] else 0
        avg = baselines.get(phase_id, {}).get("avg_daily_gallons", 0)
        avg_str = f"{avg:,.0f} gal" if avg > 0 else "—"
        limit = limits.get(phase_id)
        if limit:
            over = gallons - limit
            if over > 0:
                limit_cell = f"<td style='color:#d9534f'><b>{gallons:,.0f} / {limit:,} gal (+{over:,.0f} OVER)</b></td>"
            else:
                limit_cell = f"<td style='color:#5cb85c'>{gallons:,.0f} / {limit:,} gal ({abs(over):,.0f} under)</td>"
        else:
            limit_cell = f"<td>{gallons:,.0f} gal</td>"
        rows += (
            f"<tr>"
            f"<td><b>{data['name']}</b></td>"
            f"{limit_cell}"
            f"<td>{avg_str}</td>"
            f"<td>{per_unit:.1f} gal/unit</td>"
            f"</tr>"
        )

    return f"""
<html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
<h2 style="color:#2c7be5">{prop_name}</h2>
<h3>Water Usage Report — {date_str}</h3>
<table border="1" cellpadding="8" cellspacing="0" width="100%"
  style="border-collapse:collapse;font-size:14px">
  <thead style="background:#2c7be5;color:white">
    <tr>
      <th>Phase</th><th>Yesterday vs Daily Limit</th><th>30-Day Avg</th><th>Per Unit Avg</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
<p style="color:#666;font-size:12px;margin-top:24px">
  Water-saving tip: A running toilet wastes up to 200 gallons/day.
  Report leaks to management immediately.<br><br>
  You are receiving this as a resident of {prop_name}.
  To unsubscribe, reply with UNSUBSCRIBE.
</p>
</body></html>
"""


def _build_spike_alert_html(spikes, config):
    prop_name = config["property"]["name"]
    tz = pytz.timezone(config["property"]["timezone"])
    now_str = datetime.now(tz).strftime("%A, %B %d %Y at %I:%M %p")

    # Red for the initial limit crossing, orange for subsequent 250-gal bands.
    initial = any(s.get("threshold_hit", s["daily_limit"]) == s["daily_limit"] for s in spikes)
    header_color = "#d9534f" if initial else "#e8820c"
    increment = spikes[0].get("increment", 250) if spikes else 250

    items = ""
    for s in spikes:
        threshold_hit = s.get("threshold_hit", s["daily_limit"])
        is_first = threshold_hit == s["daily_limit"]
        bands_over = (threshold_hit - s["daily_limit"]) // increment
        band_note = "Daily limit reached" if is_first else f"+{bands_over * increment:,} gal above limit"

        items += f"""
<tr>
  <td><b>{s['phase_name']}</b></td>
  <td>{s['gallons_today']:,.0f} gal used today</td>
  <td style="color:#d9534f"><b>+{s['gallons_over']:,.0f} gal</b> over {s['daily_limit']:,} gal limit</td>
  <td>{s['per_unit_gallons']:.1f} gal/unit</td>
  <td style="color:#888;font-size:12px">{band_note}</td>
</tr>"""

    return f"""
<html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
<div style="background:{header_color};color:white;padding:16px;border-radius:4px">
  <h2 style="margin:0">Water Usage Alert</h2>
  <p style="margin:4px 0 0 0">{prop_name} — {now_str}</p>
</div>
<p>Today's water usage has exceeded the daily limit. Alerts fire at the limit and at
every additional {increment:,} gallons above it. Please inspect for leaks,
running toilets, or open faucets.</p>
<table border="1" cellpadding="8" cellspacing="0" width="100%"
  style="border-collapse:collapse;font-size:14px;margin-top:16px">
  <thead style="background:{header_color};color:white">
    <tr><th>Phase</th><th>Usage Today</th><th>vs Daily Limit</th><th>Per Unit</th><th>Status</th></tr>
  </thead>
  <tbody>{items}</tbody>
</table>
<h3>What to check:</h3>
<ul>
  <li>Running or phantom-flushing toilets</li>
  <li>Dripping faucets or showerheads</li>
  <li>Laundry or dishwasher left running</li>
  <li>Irrigation systems (if applicable)</li>
</ul>
<p>If you notice a leak, contact property management immediately.</p>
<p style="color:#666;font-size:12px">
  To unsubscribe from alerts, reply with UNSUBSCRIBE.
</p>
</body></html>
"""


def _build_today_summary_html(phase_data, config):
    tz = pytz.timezone(config["property"]["timezone"])
    date_str = datetime.now(tz).strftime("%A, %B %d, %Y at %I:%M %p")
    prop_name = config["property"]["name"]
    limits = {p["id"]: p.get("daily_gallon_limit") for p in config["bluebot"]["phases"]}

    rows = ""
    for phase_id, data in phase_data.items():
        if data.get("error"):
            rows += f"<tr><td>{data['name']}</td><td colspan='3'>Data unavailable</td></tr>"
            continue
        gallons = data.get("gallons", 0) or 0
        per_unit = gallons / data["unit_count"] if data["unit_count"] else 0
        limit = limits.get(phase_id)
        if limit:
            over = gallons - limit
            if over > 0:
                limit_cell = (
                    f"<td style='color:#d9534f'>"
                    f"<b>{gallons:,.0f} / {limit:,} gal (+{over:,.0f} OVER)</b></td>"
                )
            else:
                limit_cell = (
                    f"<td style='color:#5cb85c'>"
                    f"{gallons:,.0f} / {limit:,} gal ({abs(over):,.0f} under)</td>"
                )
        else:
            limit_cell = f"<td>{gallons:,.0f} gal</td>"
        rows += (
            f"<tr>"
            f"<td><b>{data['name']}</b></td>"
            f"{limit_cell}"
            f"<td>{per_unit:.1f} gal/unit</td>"
            f"</tr>"
        )

    return f"""
<html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
<h2 style="color:#2c7be5">{prop_name}</h2>
<h3>Today's Water Usage — Running Total as of {date_str}</h3>
<table border="1" cellpadding="8" cellspacing="0" width="100%"
  style="border-collapse:collapse;font-size:14px">
  <thead style="background:#2c7be5;color:white">
    <tr>
      <th>Phase</th><th>Today vs Daily Limit</th><th>Per Unit</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
<p style="color:#666;font-size:12px;margin-top:24px">
  Water-saving tip: A running toilet wastes up to 200 gallons/day.
  Report leaks to management immediately.<br><br>
  You are receiving this as a board member of {prop_name}.
  To unsubscribe, reply with UNSUBSCRIBE.
</p>
</body></html>
"""


def send_email(to_list, subject, html_body, config):
    """Send individual HTML emails. Logs failures per-recipient but does not raise."""
    sender = config["email"]["sender"]
    password = config["email"]["app_password"]
    failed = []

    try:
        server = smtplib.SMTP(config["email"]["smtp_server"], config["email"]["smtp_port"])
        server.starttls()
        server.login(sender, password)
    except Exception as e:
        logger.error(f"SMTP connection failed: {e}")
        raise

    for recipient in to_list:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{config['property']['name']} Water Alerts <{sender}>"
            msg["To"] = recipient
            msg.attach(MIMEText(html_body, "html"))
            server.sendmail(sender, recipient, msg.as_string())
            logger.info(f"Email sent to {recipient}: {subject}")
        except smtplib.SMTPException as exc:
            logger.error(f"Failed to send to {recipient}: {exc}")
            failed.append(recipient)
            # Attempt to recover the SMTP session for the next recipient.
            try:
                server.quit()
            except Exception:
                pass
            try:
                server = smtplib.SMTP(config["email"]["smtp_server"], config["email"]["smtp_port"])
                server.starttls()
                server.login(sender, password)
            except Exception as reconnect_err:
                logger.error(f"SMTP reconnect failed, stopping sends: {reconnect_err}")
                break

    try:
        server.quit()
    except Exception:
        pass

    if failed:
        logger.warning(f"Failed to deliver to {len(failed)} recipient(s): {failed}")


def send_daily_digest(phase_data, baselines, residents, config):
    """Send morning digest: always_notify first (in order), then residents."""
    tz = pytz.timezone(config["property"]["timezone"])
    date_str = datetime.now(tz).strftime("%B %d, %Y")
    subject = f"[Water Report] Daily Usage Summary — {date_str}"
    html = _build_daily_digest_html(phase_data, baselines, config)

    board = config["email"]["always_notify"]
    board_set = set(board)
    resident_only = [e for e in residents if e not in board_set]

    # Board first — guaranteed delivery before any rate-limit risk.
    send_email(board, subject, html, config)
    if resident_only:
        send_email(resident_only, subject, html, config)


def send_spike_alert(spikes, phase_recipients, config):
    """
    Send threshold-crossing alert: board first (in order), then affected-phase residents.
    Board (always_notify) receives alerts for ALL phases.
    Residents receive alerts only for their own phase.
    phase_recipients: dict of { phase_id: [email, ...] }
    """
    if not spikes:
        return

    phase_summaries = []
    for s in spikes:
        t = s.get("threshold_hit", s["daily_limit"])
        phase_summaries.append(f"{s['phase_name']} @ {t:,} gal")
    subject = "[WATER ALERT] " + ", ".join(phase_summaries)
    html = _build_spike_alert_html(spikes, config)

    board = config["email"]["always_notify"]
    board_set = set(board)

    affected_phases = set(s["phase_id"] for s in spikes)
    resident_only = [
        e
        for phase_id in affected_phases
        for e in phase_recipients.get(phase_id, [])
        if e not in board_set
    ]

    send_email(board, subject, html, config)
    if resident_only:
        send_email(resident_only, subject, html, config)


def send_today_digest(phase_data, recipients, config):
    """Send running-total digest: always_notify first, then residents."""
    tz = pytz.timezone(config["property"]["timezone"])
    date_str = datetime.now(tz).strftime("%B %d, %Y")
    subject = f"[Water Report] Today's Running Total — {date_str}"
    html = _build_today_summary_html(phase_data, config)

    board = config["email"]["always_notify"]
    board_set = set(board)
    resident_only = [e for e in recipients if e not in board_set]

    send_email(board, subject, html, config)
    if resident_only:
        send_email(resident_only, subject, html, config)
