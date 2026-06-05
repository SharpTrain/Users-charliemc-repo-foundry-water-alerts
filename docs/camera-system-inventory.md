# The Foundry at Washington Park — Camera & AV System Inventory

**Building:** The Foundry at Washington Park, 225 South Plank Rd, Newburgh NY 12550  
**Inventory date:** 2026-06-05  
**Compiled by:** Charlie McC / ICOM Solutions  
**Scope:** Three-phase CCTV system — analog/HD-CVI (Phase 1 & 2) + full IP/PoE (Phase 3)  
**Prepared for:** Incoming technician handoff  
**Total cameras across all phases:** ~64 positions (18 P1 + 16 P2 + ~30 P3)

---

## Priority & Recommendation Summary

**Bottom line:** All three systems run Hikvision or Hikvision-compatible firmware. The wiring is intact and hard-wired throughout. The path to a fully operational, remotely viewable system across all three phases is almost entirely configuration work — not hardware replacement. Estimated out-of-pocket cost to get to full function is under $100, with one possible storage drive purchase for Phase 3.

---

### Immediate Actions — No Cost

**1. Unlock Phase 1 DVR**
The DVR is locked. Run the Hikvision SADP tool (free PC download) on any laptop connected to the same LAN as the Phase 1 DVR. SADP will find the unit, let you reset the password, and restore admin access. Login: `admin` / `Foundry1`. Once in, check HDD status and confirm which 14 channels are dead before touching any cable.

**2. Set a password on Phase 3 NVR**
Phase 3 (NR710-64) has password protection disabled. Go to System > General > check "Enable Password" and set `Foundry1` (or a stronger password) immediately. Any device on the building LAN currently has unrestricted access to the NVR.

**3. Set up unified viewing — iVMS-4200 (free)**
All three units — Phase 1 DVR, Phase 2 hybrid DVR, and Phase 3 NVR — speak the Hikvision protocol. Install **iVMS-4200** (free, Windows/Mac, from Hikvision) on one PC and add all three recorders. This gives a single dashboard showing all cameras across all three phases simultaneously, with playback, event search, and export. No subscription, no cost.

**4. Set up mobile app — Hik-Connect (free)**
Register all three recorders on **Hik-Connect** (free Hikvision cloud app, iOS and Android). This gives board members live remote viewing and motion alerts from their phones from anywhere — no port forwarding, no static IP required. One account can manage all three units. This is the fastest path to remote access.

**5. Fix Phase 2 channel names**
Channels A3, A5–A7, A13–A15 show partial or default names in the DVR sidebar. Log in with `Foundry1` and rename them from the Channel Config menu while doing the walk-through. Takes 10 minutes.

---

### Low-Cost Actions — Under $100

**6. Check and expand Phase 3 storage first**
The Phase 3 NVR HDD LED was dim at inspection. Go to Maintenance > HDD to check installed capacity and free space. With 30+ cameras, a single 4TB drive holds roughly 2–3 weeks of footage at standard quality. If the drive is nearly full or undersized, a **Seagate SkyHawk 4TB or 8TB surveillance HDD** runs $70–$130 and drops in without any configuration. Do this before worrying about the dead cameras — a full drive means Phase 3 may already be overwriting footage.

**7. Diagnose Phase 1 dead cameras — don't replace until confirmed**
Before ordering anything, do a quick bench test: unplug one of the dead BNC cables from the DVR rear and connect a known-good spare camera directly. If the DVR shows a picture, the cable run is fine and only the camera head is dead. If no picture, the problem is in the cable or the DVR channel. Start with channels closest to the DVR room — those are the easiest to rule out. The two spare black mini dome cameras on the Phase 2 desk can be used for this test.

---

### Unified Viewing Architecture (Target State)

```
Phase 1 DVR ──┐
Phase 2 DVR ──┤──► Building LAN ──► iVMS-4200 on PC (on-site, all cameras)
Phase 3 NVR ──┘         │
                         └──► Hik-Connect cloud ──► Board members' phones (remote)
```

All three units are already on the building LAN (or bridged via EnGenius). No new hardware is needed to achieve this — only configuration on each recorder's Network > Platform Access menu.

---

## PHASE 1 — Hardware & Software Inventory

**Status: 4 of 18 cameras operational (14 offline / NO VIDEO)**

### DVR Unit

| Field | Detail |
|---|---|
| Brand | Hikvision |
| Type | Analog / HD-CVI Digital Video Recorder |
| Channel capacity | 16–18 channels (display shows 18 camera slots) |
| Likely model family | DS-7300 series (DS-7316HWI-SH or similar) |
| Front indicators | POWER (green), READY (green), STATUS, ALARM, HDD, Tx/Rx |
| Front controls | D-pad, Enter, SHIFT, MENU/F1, F2/ABC, ESC, EDIT, PLAY, REC, PTZ, PREV, jog wheel |
| Front I/O | 2× USB-A ports, optical/DVD disc slot |
| Rear I/O | 16–18× BNC camera inputs, audio RCA (in/out), HDMI out, VGA out, RJ45 network, alarm terminal blocks (green screw terminals), RS-485 |
| Power | Standard IEC C13, connected via UPS/surge strip |
| **Admin Password** | **Foundry1** |
| Condition | Powered on; POWER + READY LEDs lit; DVR is locked — use SADP tool or physical reset to restore access, then log in with password above |

### Display Monitor

| Field | Detail |
|---|---|
| Brand / Model | TCL Roku TV (~32") |
| Connection | VGA (VGA cable visible at desk; VGA-to-DVI adapter also present) |
| Display mode | 16-up multiview grid showing all 18 camera slots |
| Condition | Operational — displays DVR output |

### Network Equipment

| Device | Detail |
|---|---|
| Switch | TRENDnet small desktop switch (5–8 port, unmanaged; visible at floor cable junction) |
| Wireless bridge | EnGenius EnStation outdoor CPE/wireless bridge — mounted on exterior brick wall at roofline |
| Bridge connection | PoE Ethernet; white CAT cable from bridge runs into building conduit |
| Bridge purpose | Provides network backhaul for DVR remote access over building WiFi or point-to-point link |

### Power Infrastructure

| Device | Detail |
|---|---|
| UPS / Surge strip | APC or equivalent — black rack/desktop unit with multiple outlets; DVR and monitor plugged in |
| Outdoor power | Weatherproof outdoor outlet box at floor-level cable junction point (exterior grade) |

### Cabling

| Run | Detail |
|---|---|
| Camera coax | RG59 BNC coaxial — white and black jacketed runs; 14–18 individual cables |
| Routing — interior | Cables routed through ceiling/attic void; metal hat-channel framing visible; bundled with cable ties |
| Routing — grade level | Cables run through metal EMT conduit along floor/exterior grade into building |
| Routing — exterior | Conduit bundle exits building at grade; terminates at outdoor switch/outlet junction |
| DVR-to-monitor | VGA cable (desktop length) |
| Network | CAT5/6 from DVR to TRENDnet switch; CAT from switch to EnGenius EnStation (PoE run to exterior) |

### Camera Endpoints — Summary

| Item | Count | Notes |
|---|---|---|
| Total camera slots (DVR) | 18 | |
| Operational / live video | 4 | Appear to be hallway / elevator cameras based on DVR preview |
| Offline (NO VIDEO) | 14 | No signal at DVR — likely failed cameras, cut/damaged coax, or power loss at camera end |
| Camera connection type | Analog / HD-CVI | BNC coaxial wiring to DVR |
| Camera power method | Likely 12VDC siamese coax or PoC | No separate PoE switch observed; power likely via siamese coax or local supply at each camera |

### Camera Endpoints — By Type

#### Type A: Indoor Dome Camera
| Field | Detail |
|---|---|
| Form factor | Small dome / eyeball |
| Housing color | White |
| Mount location | Interior ceiling corner (wall-ceiling junction) |
| Environment | Indoor — common area / hallway |
| Lens | Fixed wide-angle; appears to be ~2.8mm or 3.6mm based on housing size |
| Observed location | Hallway or lobby common area; warm-lit wall sconce visible below camera |
| Condition | Visually intact; operational status unknown without DVR access |
| Typical model | Hikvision DS-2CE56D0T-IRPF or similar analog/HD-CVI mini dome |

#### Type B: Outdoor Bullet Camera
| Field | Detail |
|---|---|
| Form factor | Bullet / cylindrical |
| Housing color | Black |
| Mount location | Exterior brick wall, under soffit overhang |
| Environment | Outdoor — building perimeter / alley / parking area |
| Mount hardware | Black surface-mount junction box behind camera body |
| Lens | Varifocal or fixed telephoto (elongated body); aimed toward parking/alley |
| Observed location | Building exterior corner near parking area (vehicle visible in background) |
| Condition | Visually intact; operational status unknown without DVR access |
| Typical model | Hikvision DS-2CE16D0T-EXIF or similar analog/HD-TVI outdoor bullet |

#### Type C: Outdoor Mini Dome / Turret Camera
| Field | Detail |
|---|---|
| Form factor | Mini dome / turret |
| Housing color | Black |
| Mount location | Exterior brick wall, under soffit overhang |
| Environment | Outdoor — building perimeter |
| Lens | Short fixed lens; wider angle than Type B |
| Observed location | Same exterior overhang zone as Type B bullet; aimed at approach/entry area |
| Condition | Visually intact; operational status unknown without DVR access |
| Typical model | Hikvision DS-2CE56D0T-IRMMF or similar analog/HD-CVI mini dome |

#### Type D: Cylindrical Ceiling-Mounted Device (conduit-mounted)
| Field | Detail |
|---|---|
| Form factor | Cylindrical metal canister, ~3" long |
| Housing color | Silver / bare metal |
| Mount location | Interior ceiling — mounted directly to EMT conduit run via conduit clamp |
| Visible label | Label present on body (text not fully legible in photo) |
| Likely function | PIR motion detector, or covert pinhole camera; mounted inline with conduit run |
| Notes | Unconventional mount — clamped to conduit rather than ceiling box; label should be photographed up close for positive ID |
| Condition | Visually intact; function and operational status unverified |

### Conduit Infrastructure (Interior)

| Item | Detail |
|---|---|
| Conduit type | Rigid / IMC metal EMT conduit, ~3/4" or 1" diameter |
| Routing | Runs along interior ceilings; visible in common areas and mechanical spaces |
| Fittings | Conduit LB body / raintight conduit bodies at junction/turn points |
| Associated devices | Smoke/heat detector visible alongside conduit run in ceiling space |
| Condition | Conduit appears intact; fittings show typical aging; no obvious damage visible |

### Software / Firmware

| Item | Detail |
|---|---|
| DVR OS | Hikvision embedded Linux firmware (version unknown — need to log in to check) |
| DVR UI | Hikvision native GUI (multiview, playback, config menus) |
| Remote access | Hikvision iVMS-4200 (PC) or Hik-Connect app (mobile) — status unknown; DVR must first be unlocked |
| DVR admin account | Username: `admin` — currently locked (login prompt shown on screen); password reset required |
| NVR web interface | Accessible on LAN via browser at DVR IP once network path confirmed |

---

## Known Issues — Phase 1

1. **DVR locked** — admin password must be reset (physical reset button on unit, or Hikvision SADP tool over network) before any config changes or remote access is possible.
2. **14 of 18 cameras offline** — root causes to investigate per camera:
   - Coaxial cable cut, damaged, or disconnected at junction
   - Camera head failed (power or image sensor)
   - BNC connector corroded or loose at DVR rear
   - Camera power supply failed at the camera end
3. **Cabling exposed at grade** — conduit bundle runs along floor at grade; outdoor runs appear unsecured at points and exposed to weather/foot traffic.
4. **Structural cracking visible at wireless bridge mount** — brick/mortar cracking at exterior wall where EnGenius EnStation is mounted; worth flagging to the board for masonry inspection.
5. **VGA connection to monitor** — lossier signal path than HDMI; worth switching to HDMI if DVR rear HDMI port is unused.

---

---

## PHASE 2 — Hardware & Software Inventory

**Status: 13 of 16 cameras operational (3 offline)**  
*Camera types: same as Phase 1 — Type A indoor dome, Type B outdoor bullet, Type C outdoor mini dome*

### DVR Unit

| Field | Detail |
|---|---|
| Brand | Hikvision |
| Type | Hybrid DVR — supports both analog/HD-CVI (A channels) AND IP/digital cameras (D channels) |
| Channel capacity | 16 analog (A1–A16) + 8–9 IP channels (D1–D9); visible on monitor sidebar |
| Likely model family | Hikvision DS-7300 Hybrid series (DS-7316HGHI-SH or similar) |
| Front indicators | POWER (green), READY (green/amber), STATUS, ALARM, HDD, Tx/Rx |
| Front controls | D-pad, Enter, SHIFT, MENU/F1, F2/ABC, ESC, EDIT, PLAY, REC, PTZ, PREV, jog wheel |
| Front I/O | 2× USB-A ports, optical/DVD disc slot |
| Rear I/O | 16× BNC analog inputs (8–9 in use/visible in photo), HDMI, VGA, RJ45 network, audio RCA, RS-485, alarm terminals |
| Power | CyberPower 450VA UPS (confirmed in photo — black desktop UPS) |
| **Admin Password** | **Foundry1** |
| Condition | Powered on and operational; live camera feed showing on monitor |

### Named Camera Channel List (read from monitor sidebar, Photo 3)

| Channel | Name | Status |
|---|---|---|
| A1 | bld front | — |
| A2 | lobby | — |
| A3 | (partially legible) | — |
| A4 | 2 laundry | — |
| A5 | (partially legible) | — |
| A6 | (partially legible) | — |
| A7 | (partially legible) | — |
| A8 | 4 laundry | — |
| A9 | edward lobby | — |
| A10 | edward-1st fl view | — |
| A11 | road conf (road corner?) | — |
| A12 | 1st in hall to court | — |
| A13 | (partially legible) | — |
| A14 | (partially legible) | — |
| A15 | (partially legible) | — |
| A16 | edward street | — |
| D1–D9 | IPCamera 0 (default/unnamed) | Likely unconfigured or unused IP slots |
| Active view | 2 fl corner | Live at time of photo (03-18-2026 19:59:59) |

*Note: Channel names indicate cameras cover building front, lobby, laundry rooms (floors 2 and 4), Edward St side lobby, 1st-floor hallway, courtyard approach, Edward St exterior. A full channel-by-channel status check requires DVR access.*

### Display Monitor

| Field | Detail |
|---|---|
| Brand / Model | TCL Roku TV (~32"), same model as Phase 1 |
| Connection | HDMI (monitor shows crisp image; HDMI cable visible at rear) |
| Display mode | Single-camera fullscreen + channel list sidebar (playback UI visible) |
| Condition | Operational |

### Camera Power Distribution Panel

| Field | Detail |
|---|---|
| Type | Wall-mounted multi-output 12VDC camera power distribution board |
| Housing | Small metal enclosure, open-face, mounted on wall adjacent to DVR |
| Indicators | Multiple red LEDs (per-channel status) + green LED; visible in Photo 3 |
| Purpose | Distributes 12VDC power to individual analog cameras via dedicated outputs |
| Condition | Powered on; LEDs lit; visual status only — individual channel fuse check needed |

### Network Equipment

| Device | Detail |
|---|---|
| Wireless bridge | EnGenius EnStation outdoor CPE — mounted on exterior painted brick wall near downspout |
| Switch | Gray unmanaged network switch (8+ port, brand TBD — visible in telecom room photo) |
| ISP demarc | Verizon / Bell Atlantic FIOS enclosure — large green metal panel labeled "Bell Atlantic access only"; mounted in building telecom closet |
| ISP device | Verizon ONT or router (black Verizon-branded box mounted alongside demarc panel) |
| Secondary network | Black cable modem/router (Arris or similar) + small PoE injector/adapter at floor level — appears to be in a common area or office |

### Power Infrastructure

| Device | Detail |
|---|---|
| UPS | CyberPower 450VA — confirmed brand/model in Photo 8; battery backup + surge protected outlets |
| Surge strip | Older white 6-outlet surge protector strip (on desk alongside CyberPower) |

### Cabling

| Run | Detail |
|---|---|
| Camera coax | RG59 BNC — white and black jacketed; 8–9 runs visible at DVR rear (red BNC collar connectors) |
| Network | CAT5/6 from DVR to switch; CAT to EnGenius EnStation (PoE) |
| Building distribution | Central cable distribution box in meter/utility room — CAT5/6 and coax; currently very disorganized (see Known Issues) |

### Building Telecom / Utility Room

| Item | Detail |
|---|---|
| Room type | Building meter room / main telecom termination point |
| Electric meters | Bank of individual unit meters on right wall — unit numbers visible (101, 103, 107, 109, etc.) |
| Telecom panel | Central open junction box with large tangled cable mass — CAT5/6 and coax; unsecured, exposed |
| Motorola device | Motorola-branded unit wall-mounted (older cable signal amplifier or gateway) |
| Monitoring panel | Small device below Motorola unit — possibly older alarm or access control panel component |
| Conduit | Large 3" gray EMT sweeps running along ceiling — main building infrastructure conduit |
| Fire safety | CO2 fire extinguisher mounted on wall |
| Condition | Poor — cable distribution box is completely disorganized; a fire/safety hazard; needs professional remediation |

### Spare / On-Hand Equipment (Photo 8)

| Item | Qty | Detail |
|---|---|---|
| Spare cameras — mini dome | 2 | Black mini dome/turret cameras in anti-static bags; Type C form factor — appear to be new/unused |
| Coaxial cable spool | 1 | Black RG59 or RG6 coax, pre-spooled, with BNC connector; appears to be ~50–100 ft |
| White coaxial cable | 1 run | Loose white coax visible on desk — additional spare run |
| Red/white siamese cable | 1 run | Siamese coax+power cable spool (red wire visible); used for camera power + video combined |
| Mounting hardware | Misc | Camera mounting brackets/hardware visible in bag with spare cameras |
| Installation manual | 1 | Camera installation instruction sheet visible in bag |

### Software / Firmware

| Item | Detail |
|---|---|
| DVR OS | Hikvision embedded Linux firmware (version visible in playback UI — timestamp format matches Hikvision 3.x/4.x) |
| DVR UI | Hikvision native GUI — live view + playback confirmed operational |
| Playback | Recording confirmed active; playback timeline visible in Photo 4 (date range: 11-22-2026 through 03-10-2026) |
| IP channel slots | D1–D9 labeled "IPCamera 0" — default names suggest unconfigured; could be enabled for future IP cam expansion |
| Remote access | Hikvision iVMS-4200 / Hik-Connect — DVR is accessible (not locked like Phase 1) |

---

## Known Issues — Phase 2

1. **3 of 16 cameras offline** — run same diagnostic as Phase 1: BNC connectors, coax continuity, camera power, power board fuse per channel.
2. **Camera channel names incomplete** — sidebar shows several channels with generic or partially legible names; full rename/label audit needed via DVR menu.
3. **IP camera slots D1–D9 unnamed** — either unused or connected cameras that were never configured; verify in DVR network camera menu.
4. **Building telecom/cable distribution box (meter room) is a serious hazard** — completely disorganized exposed wiring; no cable management; a remediation project is needed independent of camera work.
5. **EnGenius EnStation mount location** — near downspout on painted CMU wall; same cracking concern as Phase 1 mount; verify waterproofing on Ethernet cable entry point.
6. **CyberPower 450VA may be undersized** — a Hikvision 16-channel hybrid DVR + monitor can draw 60–100W; 450VA ≈ 270W usable capacity; adequate for basic runtime but battery should be load-tested.
7. **Playback timeline gap noted** — Photo 4 shows timeline range 11-22-2026 to 03-10-2026; the current date is 2026-06-05, suggesting the DVR may not have been recording continuously or the HDD is nearly full.

---

---

## PHASE 3 — Hardware & Software Inventory

**Status: All cameras operational (~30+ of 64 channels configured and live)**  
**System type: Full IP / PoE NVR — newer, clean installation**  
**Known gaps: No remote viewing configured (no app or URL); storage capacity unverified**

### NVR Unit — Confirmed from device label + on-screen System Info

| Field | Detail |
|---|---|
| Device type | Network Video Recorder (NVR) — pure IP, no analog inputs |
| Brand | Hikvision OEM / white-label (UI and firmware are identical to Hikvision; "NR" model prefix used by some distributors) |
| **Model** | **NR710-64** |
| **Serial No.** | **1620221116CCRRK84597410WCVU** |
| **MAC Address** | **24:32:AE:58:32:8D** |
| **Firmware Version** | **V4.61.000, Build 220809** (built 2022-08-09 — approx. 4 years old) |
| **Hardware Version** | **0100054C02000000** |
| Channel capacity | 64 IP camera channels (NR710-**64** suffix) |
| Active channels | ~30+ (all operational per on-site assessment) |
| Front indicators | ALARM (off), READY (blue, lit), STATUS (blue, lit), HDD (off/dim), Tx/Rx (blue, lit), GUARD (blue, lit) |
| Front controls | D-pad + Enter, PTZ, PLAY, REC, SHOT, F1, F2, MENU, ESC, WIPER, LIGHT, AUX, MAINSPOT, IRIS±, FOCUS±, ZOOM±, AUTO |
| Outputs | HDMI1/VGA1, HDMI2/VGA2 (both confirmed in System > General) |
| Power | CyberPower UPS (larger unit; brand confirmed in photo — model unread) |
| Input voltage | 100V–240V~, 50/60Hz, 2A, 70W Max (confirmed from label) |
| Password protection | **DISABLED** — "Enable Password" unchecked in System > General |
| Auto logout | Never |

### System Configuration (read from NVR screens)

| Setting | Value |
|---|---|
| Language | English |
| Time Zone | (GMT-05:00) Eastern Time |
| Date Format | MM-DD-YYYY |
| System Date at inspection | 06-03-2026 (accurate, 2 days before this report) |
| System Time at inspection | 14:35:18 |
| Device Name | Network Video Recorder (default — not renamed) |
| Device No. | 1 |
| HDMI1/VGA1 Resolution | 1024×768 @ 60Hz |
| HDMI2/VGA2 Resolution | 1024×768 @ 60Hz |
| DST | Enabled: Apr 1st Sun 2:00 → Oct last Sun 2:00, +60 min |
| IoT / Business Applications | Access Control (Entrance/Exit Channel Control) + Alarm (Event Linkage Management) — available in firmware, not confirmed active |
| Remote access | **Not configured** — no Hik-Connect, iVMS-4200, or URL access set up |

### Display Monitor

| Field | Detail |
|---|---|
| Brand / Model | TCL Roku TV (~43–50"), same brand as Phase 1 & 2 |
| Connection | HDMI (resolution shown as 1024×768 — can be increased to 1920×1080) |
| Condition | Operational |

### Camera Type — Phase 3 (IP Turret / Dome)

| Field | Detail |
|---|---|
| Form factor | IP turret dome, flush ceiling mount |
| Housing color | White |
| Sensors visible | 1× square IR LED illuminator (night vision) + 1× camera lens |
| Connection | PoE Ethernet (CAT6 via EMT conduit to NVR or PoE switch) |
| Environment | Indoor — common areas, hallways |
| Conduit | EMT conduit from camera ceiling mount into ceiling void; standard installation |
| Condition | All units operational and visually clean; installation is new |
| Likely model | Hikvision DS-2CD2343G2-I or DS-2CD2347G2-LU turret camera (or OEM equivalent) |
| Count | ~30+ (exact count to be confirmed via NVR camera menu) |

### Network Equipment

| Device | Detail |
|---|---|
| PoE Switch | TRENDnet GreenNet series (black with green logo) — visible in photos with yellow CAT6 connections |
| Switch ports | 8+ ports; multiple yellow CAT6 cables terminated |
| Cable labeling | Yellow CAT6 runs have printed white label tags — labeled with zone/location identifiers |
| Outlet | Metal weatherproof duplex outlet box mounted at switch location |

### Power Infrastructure

| Device | Detail |
|---|---|
| UPS | CyberPower — larger tower model (brand confirmed; specific VA rating not readable from photo) |
| Location | On desk/shelf adjacent to NVR |

### Cabling

| Run | Detail |
|---|---|
| Camera runs | Yellow CAT6 — all labeled; routed through EMT conduit and along wooden backboard shelf |
| Conduit | Galvanized EMT (1"+), vertical wall runs; pull boxes at transitions |
| Termination | GreenNet PoE switch at shelf distribution point |
| Condition | Clean and organized — substantially better than Phase 1 & 2 |

---

## Known Issues — Phase 3

1. **Password protection is OFF** — `Enable Password` is unchecked in System > General. Any device on the local network can access the NVR without credentials. Enable a strong admin password immediately.
2. **No remote viewing configured** — Hik-Connect / iVMS-4200 / DDNS not set up. The NVR is inaccessible from outside the local LAN. Remote access should be configured via Hik-Connect (cloud) or a static-IP/DDNS setup through the Network menu.
3. **Storage status unverified** — HDD LED was dim/off on NVR front panel. The HDD submenu (Maintenance > HDD) should be checked for installed capacity, free space, and drive health. A 64-channel NVR with 30+ cameras recording continuously will fill storage quickly.
4. **Firmware is ~4 years old** — V4.61.000, Build 220809 (August 2022). Current Hikvision firmware for equivalent hardware is V4.7x+. Check Maintenance > Upgrade for available updates.
5. **Display resolution set to 1024×768** — Both HDMI outputs are at sub-HD resolution. Should be changed to 1920×1080 in System > General for a usable monitoring view.
6. **Device name is default** — "Network Video Recorder" is the generic name. Should be renamed to "Foundry Phase 3 NVR" or similar for identification on the network.
7. **IoT/Access Control modules visible** — The Business Application menu shows Access Control and Alarm Linkage modules available. If door/access control hardware is present in Phase 3 areas, these may need configuration.

---

## Cross-Phase Summary

| Item | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|
| Recorder type | Hikvision DVR (analog/HD-CVI) | Hikvision Hybrid DVR (analog + IP slots) | NR710-64 NVR (pure IP, 64-ch) |
| Model | DS-7300 series (est.) | DS-7300 Hybrid series (est.) | NR710-64 (confirmed) |
| Firmware | Unknown (DVR locked) | Unknown (check via menu) | V4.61.000, Build 220809 (confirmed) |
| Camera count | 18 total / **4 operational** | 16 total / **13 operational** | ~64 slots / **~30+ operational** |
| Camera type | Analog/HD-CVI BNC | Analog/HD-CVI BNC | PoE IP turret (CAT6) |
| Camera housing | White dome (indoor), Black bullet + dome (outdoor) | Same as Phase 1 | White IP turret dome (indoor) |
| Monitor | TCL Roku TV ~32" via VGA | TCL Roku TV ~32" via HDMI | TCL Roku TV ~43–50" via HDMI |
| UPS / Power | APC-style surge strip | CyberPower 450VA (confirmed) | CyberPower (larger; VA unread) |
| Network backhaul | EnGenius EnStation (exterior) | EnGenius EnStation (exterior) | GreenNet PoE switch (internal) |
| Remote access | Not available (DVR locked) | Possible (DVR unlocked; not confirmed set up) | Not configured |
| Password | DVR locked (needs reset) | Accessible (check password state) | **Disabled — no password set** |
| Condition | Poor — 14 cameras down, DVR locked | Fair — 3 cameras down, usable | Good — all cameras live; software config needed |

---

## Open Items for Incoming Technician

### Phase 1 — Priority Actions
- [ ] Reset DVR admin password using Hikvision SADP tool (PC on same LAN) or physical reset button
- [ ] After login: check firmware version, HDD status, channel list
- [ ] Walk all 14 dead BNC runs — check BNC connectors at DVR rear first, then trace to camera; test with a spare camera or BNC loopback tool
- [ ] Switch monitor connection from VGA to HDMI (port visible on DVR rear)
- [ ] Inspect EnGenius EnStation mount — masonry cracks at mount location flagged

### Phase 2 — Priority Actions
- [ ] Confirm admin password status (DVR was accessible at inspection)
- [ ] Check firmware version via Maintenance menu
- [ ] Check HDD status and remaining storage
- [ ] Check power distribution board fuses for the 3 offline cameras
- [ ] Rename all partially legible channel names (A3, A5, A6, A7, A13, A14, A15)
- [ ] Verify D1–D9 IP channel slots — determine if unused or connected but unconfigured
- [ ] Address building meter room cable distribution box — this is a safety/fire hazard; needs professional remediation
- [ ] Verify recording timeline gap (playback showed last recording ~March 2026)

### Phase 3 — Priority Actions
- [ ] **Enable password protection immediately** (System > General > check "Enable Password"; create strong admin password)
- [ ] Set up remote access: go to Network > Platform Access > enable Hik-Connect, or configure DDNS/port forwarding
- [ ] Check HDD: Maintenance > HDD — verify installed capacity, health, and free space; add drive if needed
- [ ] Update firmware: Maintenance > Upgrade — check for updates to V4.7x+ for security patches
- [ ] Change display resolution: System > General > HDMI1/VGA1 Resolution → 1920×1080
- [ ] Rename device: System > General > Device Name → "Foundry Phase 3 NVR"
- [ ] Get exact camera count and confirm all channel names via Camera menu

---

*This inventory is part of The Foundry at Washington Park facilities documentation.*  
*Water monitoring system (BlueBot / Phase 1 & Phase 2) documented separately — see project README.*  
*Property management: HE Development Construction Property Management (document visible in Phase 3 photos).*
