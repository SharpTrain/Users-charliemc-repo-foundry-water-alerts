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

    items = ""
    for s in spikes:
        items += f"""
<tr>
  <td><b>{s['phase_name']}</b></td>
  <td>{s['gallons_today']:,.0f} gal used today</td>
  <td style="color:#d9534f"><b>+{s['gallons_over']:,.0f} gal</b> over {s['daily_limit']:,} gal limit</td>
  <td>{s['per_unit_gallons']:.1f} gal/unit</td>
</tr>"""

    return f"""
<html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
<div style="background:#d9534f;color:white;padding:16px;border-radius:4px">
  <h2 style="margin:0">Water Usage Alert</h2>
  <p style="margin:4px 0 0 0">{prop_name} — {now_str}</p>
</div>
<p>Today's water usage has exceeded the daily limit. Please inspect for leaks,
running toilets, or open faucets.</p>
<table border="1" cellpadding="8" cellspacing="0" width="100%"
  style="border-collapse:collapse;font-size:14px;margin-top:16px">
  <thead style="background:#d9534f;color:white">
    <tr><th>Phase</th><th>Usage Today</th><th>vs Daily Limit</th><th>Per Unit</th></tr>
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


def send_email(to_list, subject, html_body, config):
    """Send an HTML email to a list of addresses."""
    sender = config["email"]["sender"]
    password = config["email"]["app_password"]

    try:
        server = smtplib.SMTP(config["email"]["smtp_server"], config["email"]["smtp_port"])
        server.starttls()
        server.login(sender, password)

        for recipient in to_list:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{config['property']['name']} Water Alerts <{sender}>"
            msg["To"] = recipient
            msg.attach(MIMEText(html_body, "html"))
            server.sendmail(sender, recipient, msg.as_string())
            logger.info(f"Email sent to {recipient}: {subject}")

        server.quit()
    except Exception as e:
        logger.error(f"Email send failed: {e}")
        raise


def send_daily_digest(phase_data, baselines, recipients, config):
    """Send the morning usage digest to all recipients."""
    tz = pytz.timezone(config["property"]["timezone"])
    date_str = datetime.now(tz).strftime("%B %d, %Y")
    subject = f"[Water Report] Daily Usage Summary — {date_str}"
    html = _build_daily_digest_html(phase_data, baselines, config)

    all_recipients = list(set(recipients + config["email"]["always_notify"]))
    send_email(all_recipients, subject, html, config)


def send_spike_alert(spikes, phase_recipients, config):
    """
    Send spike alert to affected-phase residents + board.
    phase_recipients: dict of { phase_id: [email, ...] }
    """
    if not spikes:
        return

    affected_phases = set(s["phase_id"] for s in spikes)
    recipients = set(config["email"]["always_notify"])

    for phase_id in affected_phases:
        recipients.update(phase_recipients.get(phase_id, []))

    subject = (
        f"[WATER ALERT] Daily Limit Exceeded — "
        + ", ".join(s["phase_name"] for s in spikes)
    )
    html = _build_spike_alert_html(spikes, config)
    send_email(list(recipients), subject, html, config)
