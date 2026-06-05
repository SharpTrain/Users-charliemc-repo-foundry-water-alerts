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
| Condition | Powered on and operational; live camera feed showing on monitor (no login lock observed) |

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

## Phase 3

*To be added after Charlie provides Phase 3 photos.*

---

*This inventory is part of The Foundry at Washington Park facilities documentation. Water monitoring system (BlueBot / Phase 1 & Phase 2) documented separately — see project README.*
