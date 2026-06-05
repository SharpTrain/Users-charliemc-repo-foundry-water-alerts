# The Foundry at Washington Park — Camera & AV System Inventory

**Building:** The Foundry at Washington Park, 225 South Plank Rd, Newburgh NY 12550  
**Inventory date:** 2026-06-05  
**Compiled by:** Charlie McC / ICOM Solutions  
**Scope:** Three-phase analog CCTV + wireless backhaul system

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
| Condition | Powered on; POWER + READY LEDs lit; DVR is locked (admin login required to unlock) |

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

## Phase 2 and Phase 3

*To be added after Charlie provides Phase 2 and Phase 3 photos.*

---

*This inventory is part of The Foundry at Washington Park facilities documentation. Water monitoring system (BlueBot / Phase 1 & Phase 2) documented separately — see project README.*
