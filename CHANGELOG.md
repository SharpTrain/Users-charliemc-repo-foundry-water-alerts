# Changelog

## 2026-06-11 — Phase 1 residents added to email alerts

Phase 1 resident email list loaded into RESIDENTS_EMAIL_CSV GitHub Secret.

- 29 Phase 1 resident email addresses added (units 101J–306J)
- Charlie MC removed from Phase 1 slot (already covered as board member via always_notify)
- Phase 2 recipient list unchanged (40 entries)
- 7 named residents had no email on file, but 6 of those units already had
  coverage via a co-resident at the same unit: 102J (Terri Kearney),
  108J (Andrew Schrijver), 110J (Carol Lawrence), 205J (Rick Lauro),
  301J (Desiree LeGrand), 306J (Terron Johnson). Only 211J remains with
  no resident name or email on file (status unknown/vacant).

No code changes. Alert rules, thresholds, timing, and digest schedule unchanged.

## 2026-06-15 — Verified Phase 1/2 roster integrity

- Confirmed all 69 rows in RESIDENTS_EMAIL_CSV (29 Phase 1, 40 Phase 2):
  valid email format, no duplicates
- Confirmed daily digest already sends to board (always_notify) + every
  resident across both phases (load_email_list returns a flat list,
  not phase-filtered)
- 211J remains the only unit with zero email coverage

---

## 2026-05-10 — Switched to absolute daily gallon thresholds

- Phase 1 limit: 1,750 gal/day
- Phase 2 limit: 2,650 gal/day
- Each phase alerts once at limit, then every 250 gal above
- Daily digest shows yesterday vs. daily limit (red/green)
- alert_state.json resets each day (gitignored)

---

## 2026-05-06 — BlueBot API field fix

- Fixed all-zero data bug: BlueBot /flow/v2 returns `total` not `gallons`
- Real baseline confirmed: Phase 1 ~1,357 gal/day, Phase 2 ~2,640 gal/day

---

## 2026-05-03 — Twilio Toll-Free Verification submitted

- TFN: +18338963879
- Legal entity: THE FOUNDRY AT WASHINGTON PARK CONDOMINIUM ASSOC
- EIN: 14-1790507
- Status: IN_REVIEW (no code changes needed once approved)
