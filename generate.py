#!/usr/bin/env python3
"""
Square Leg 2 — Updated UK nuclear target list
Generates: targets.csv, targets.geojson, targets.md

Edit the TARGETS list below and re-run to regenerate all outputs.
Canonical data source is this file; CSV/GeoJSON/MD are derived.
"""

import csv
import json
from pathlib import Path

OUT_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# TARGET DATA
# Each dict: id, name, cat, subcat, tier, lat, lon, yield_kt,
#             burst (ground|air), height_m, rationale, notes, sources
# ---------------------------------------------------------------------------
# Tier definitions:
#   T1 ~40-60  counterforce + decapitation
#   T2 ~100-130 cumulative — full military + major cities + top infrastructure
#   T3 ~200-300 cumulative — all-out: secondary cities, full infra, industry
# ---------------------------------------------------------------------------

TARGETS = [
    # =========================================================
    # A  STRATEGIC NUCLEAR FORCES & WARHEAD INFRASTRUCTURE
    # =========================================================
    {"id": "A01", "name": "AWE Aldermaston", "cat": "A", "subcat": "Warhead design/production",
     "tier": "T1", "lat": 51.3683, "lon": -1.1394, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "UK nuclear warhead design, plutonium processing, tritium. Sprawling above-ground campus — airburst sufficient.",
     "notes": "Companion to Burghfield (assembly).", "sources": "AWE"},

    {"id": "A02", "name": "AWE Burghfield", "cat": "A", "subcat": "Warhead assembly",
     "tier": "T1", "lat": 51.3989, "lon": -1.0544, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "UK warhead final assembly and dismantling. Sole site for this function. Soft industrial target.",
     "notes": "", "sources": "AWE"},

    {"id": "A03", "name": "HMNB Clyde (Faslane)", "cat": "A", "subcat": "SSBN operating base",
     "tier": "T1", "lat": 56.0669, "lon": -4.8267, "yield_kt": 475, "burst": "air", "height_m": 500,
     "rationale": "Sole Royal Navy SSBN and SSN operating base. Single point of failure for UK deterrent at sea. Airburst to destroy submarines in port and base infrastructure.",
     "notes": "Multi-warhead strike likely. Also cat E (naval base).", "sources": "RN"},

    {"id": "A04", "name": "RNAD Coulport", "cat": "A", "subcat": "Warhead storage",
     "tier": "T1", "lat": 56.0550, "lon": -4.8792, "yield_kt": 475, "burst": "ground", "height_m": 0,
     "rationale": "Strategic warhead storage and torpedo loading for Trident submarines. 8 miles from Faslane.",
     "notes": "", "sources": "RN"},

    {"id": "A05", "name": "HMNB Devonport", "cat": "A", "subcat": "SSN refit + nuclear drydock",
     "tier": "T1", "lat": 50.3833, "lon": -4.1833, "yield_kt": 475, "burst": "air", "height_m": 500,
     "rationale": "Largest naval base in Western Europe. Only UK facility able to refit nuclear submarines. Airburst to destroy drydocks and ships in refit.",
     "notes": "Also cat E (naval base). Adjacent Plymouth city (I37).", "sources": "Babcock, RN"},

    {"id": "A06", "name": "BAE Systems Barrow-in-Furness", "cat": "A", "subcat": "SSBN/SSN construction",
     "tier": "T1", "lat": 54.1130, "lon": -3.2347, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Sole UK shipyard building nuclear submarines (Astute-class SSN, Dreadnought-class SSBN). Irreplaceable industrial capability. Soft industrial site — airburst sufficient.",
     "notes": "Also cat H (defence industry).", "sources": "BAE Systems"},

    {"id": "A07", "name": "Rolls-Royce Raynesway, Derby", "cat": "A", "subcat": "Naval reactor production",
     "tier": "T1", "lat": 52.9175, "lon": -1.4300, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Only UK facility producing naval nuclear reactor cores (PWR2/PWR3). Sole-source supplier for SSN/SSBN propulsion. Soft industrial site.",
     "notes": "Also cat H. Adjacent Derby city (I20).", "sources": "Rolls-Royce"},

    # =========================================================
    # B  US FORCES IN THE UK
    # =========================================================
    {"id": "B01", "name": "RAF Lakenheath", "cat": "B", "subcat": "USAF strike (F-35A, B61-12)",
     "tier": "T1", "lat": 52.4093, "lon": 0.5610, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "48th FW: F-35As joining F-15Es. Reportedly hosting B61-12 gravity bombs from 2024. Largest USAF combat base in Europe.",
     "notes": "Also cat D (RAF base).", "sources": "USAFE, open sources"},

    {"id": "B02", "name": "RAF Mildenhall", "cat": "B", "subcat": "USAF tankers + AFSOC",
     "tier": "T2", "lat": 52.3614, "lon": 0.4864, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "100th ARW (KC-135 tankers) and 352nd SOW (special operations). 7 miles from Lakenheath.",
     "notes": "", "sources": "USAFE"},

    {"id": "B03", "name": "RAF Croughton", "cat": "B", "subcat": "USAF global comms relay",
     "tier": "T2", "lat": 51.9856, "lon": -1.1872, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "USAF 422nd ABG. Major satellite relay hub linking European and CONUS command networks. NSA presence.",
     "notes": "", "sources": "USAF"},

    {"id": "B04", "name": "RAF Menwith Hill", "cat": "B", "subcat": "NSA/GCHQ SIGINT station",
     "tier": "T2", "lat": 54.0086, "lon": -1.6883, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Largest NSA station outside the US. 30+ radomes. ECHELON/FIVE EYES overhead SIGINT processing hub. SIGINT, not directly nuclear forces.",
     "notes": "Also cat G (radar/SIGINT).", "sources": "NSA, public record"},

    {"id": "B05", "name": "RAF Fylingdales", "cat": "B", "subcat": "BMEWS early warning radar",
     "tier": "T1", "lat": 54.3614, "lon": -0.6700, "yield_kt": 475, "burst": "ground", "height_m": 0,
     "rationale": "Solid-state phased array radar (SSPARS). Part of US Ballistic Missile Early Warning System and Space Surveillance Network.",
     "notes": "Also cat G. Hardened structure — groundburst.", "sources": "MoD"},

    {"id": "B06", "name": "RAF Welford", "cat": "B", "subcat": "USAF conventional munitions storage",
     "tier": "T2", "lat": 51.4714, "lon": -1.3844, "yield_kt": 475, "burst": "ground", "height_m": 0,
     "rationale": "Largest USAF conventional munitions storage site in Europe. 100+ earth-covered bunkers. Nuclear weapons stored in WS3 vaults at operating bases, not here.",
     "notes": "", "sources": "USAF"},

    {"id": "B07", "name": "RAF Alconbury", "cat": "B", "subcat": "USAF intelligence",
     "tier": "T2", "lat": 52.3719, "lon": -0.2292, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "501st CSW. Co-located with Joint Analysis Center Molesworth. USAF intelligence fusion for EUCOM/AFRICOM.",
     "notes": "Effectively same complex as B08 Molesworth.", "sources": "USAF"},

    {"id": "B08", "name": "RAF Molesworth", "cat": "B", "subcat": "Joint Analysis Center",
     "tier": "T2", "lat": 52.3761, "lon": -0.4114, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Joint Analysis Center — primary USAF intelligence facility in UK. 3 miles west of Alconbury.",
     "notes": "", "sources": "USAF"},

    {"id": "B09", "name": "RAF Feltwell", "cat": "B", "subcat": "USSF Space Surveillance + support",
     "tier": "T2", "lat": 52.4914, "lon": 0.5386, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "5th Space Surveillance Squadron optical telescope site. Housing and support functions for Lakenheath/Mildenhall cluster.",
     "notes": "", "sources": "USSF"},

    {"id": "B10", "name": "RAF Fairford", "cat": "B", "subcat": "USAF strategic bomber forward base",
     "tier": "T2", "lat": 51.6822, "lon": -1.7900, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Forward operating location for US strategic bombers (B-52, B-2, B-1B). Routine rotations. Longest military runway in UK. Soft airfield target.",
     "notes": "", "sources": "USAFE"},

    # =========================================================
    # C  STRATEGIC COMMAND, GOV CONTINUITY, INTELLIGENCE
    # =========================================================
    {"id": "C01", "name": "PINDAR / Whitehall (Cabinet Office)", "cat": "C", "subcat": "Crisis command bunker",
     "tier": "T2", "lat": 51.5040, "lon": -0.1280, "yield_kt": 800, "burst": "air", "height_m": 2000,
     "rationale": "Cabinet Office crisis management centre under MoD Main Building. Part of 3-GZ London strike. COBR/COBRA crisis management.",
     "notes": "Overlap with London GZ 2 (I02).", "sources": "Declassified records"},

    {"id": "C02", "name": "Northwood HQ", "cat": "C", "subcat": "PJHQ + NATO MARCOM",
     "tier": "T2", "lat": 51.6050, "lon": -0.4172, "yield_kt": 475, "burst": "ground", "height_m": 0,
     "rationale": "UK Permanent Joint Headquarters (all UK joint ops) and NATO Maritime Command. Global military command node.",
     "notes": "", "sources": "MoD, NATO"},

    {"id": "C03", "name": "RAF High Wycombe (Air Command HQ)", "cat": "C", "subcat": "RAF headquarters",
     "tier": "T2", "lat": 51.6344, "lon": -0.8072, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "HQ Air Command. Command and control of all RAF operational forces. Underground operations centre.",
     "notes": "", "sources": "RAF"},

    {"id": "C04", "name": "Army HQ Andover (Marlborough Lines)", "cat": "C", "subcat": "British Army HQ",
     "tier": "T2", "lat": 51.2089, "lon": -1.4844, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "HQ British Army at Marlborough Lines, Andover. Top-level army command.",
     "notes": "", "sources": "British Army"},

    {"id": "C05", "name": "Navy Command Portsmouth (Portsdown Hill)", "cat": "C", "subcat": "Royal Navy HQ",
     "tier": "T2", "lat": 50.8500, "lon": -1.1000, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "HQ Navy Command on Portsdown Hill. Royal Navy operational command node.",
     "notes": "Partially covered by HMNB Portsmouth strike (E01).", "sources": "RN"},

    {"id": "C06", "name": "GCHQ Cheltenham", "cat": "C", "subcat": "SIGINT HQ",
     "tier": "T2", "lat": 51.8986, "lon": -2.1244, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "GCHQ Doughnut. UK signals intelligence and cyber HQ. Five Eyes keystone. Modern above-ground office complex — airburst sufficient.",
     "notes": "", "sources": "GCHQ"},

    {"id": "C07", "name": "MI5 Thames House", "cat": "C", "subcat": "Security Service HQ",
     "tier": "T2", "lat": 51.4942, "lon": -0.1250, "yield_kt": 800, "burst": "air", "height_m": 2000,
     "rationale": "MI5 headquarters, Millbank. Internal security decapitation.",
     "notes": "Covered by London GZ 2 (I02).", "sources": "Public record"},

    {"id": "C08", "name": "MI6 Vauxhall Cross", "cat": "C", "subcat": "SIS HQ",
     "tier": "T2", "lat": 51.4872, "lon": -0.1244, "yield_kt": 800, "burst": "air", "height_m": 2000,
     "rationale": "MI6 / SIS headquarters. Foreign intelligence decapitation.",
     "notes": "Covered by London GZ 2 (I02).", "sources": "Public record"},

    {"id": "C09", "name": "Credenhill (22 SAS / UKSF HQ)", "cat": "C", "subcat": "UK Special Forces HQ",
     "tier": "T2", "lat": 52.0897, "lon": -2.8158, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "HQ 22 SAS Regiment and UK Special Forces since 1999. UKSF operational base and strategic reserve capability.",
     "notes": "", "sources": "Public record"},

    {"id": "C10", "name": "RM Poole (SBS HQ)", "cat": "C", "subcat": "UK Special Forces (maritime)",
     "tier": "T2", "lat": 50.6992, "lon": -1.9436, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "HQ Special Boat Service. UK maritime special forces base.",
     "notes": "", "sources": "Public record"},

    {"id": "C11", "name": "Scottish Parliament, Holyrood", "cat": "C", "subcat": "Devolved administration",
     "tier": "T2", "lat": 55.9522, "lon": -3.1758, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Scottish Parliament and government. Political decapitation of Scotland.",
     "notes": "Covered by Edinburgh city strike (I12).", "sources": ""},

    {"id": "C12", "name": "Senedd / Senedd Cymru, Cardiff", "cat": "C", "subcat": "Devolved administration",
     "tier": "T2", "lat": 51.4642, "lon": -3.1628, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Welsh Parliament and government. Political decapitation of Wales.",
     "notes": "Covered by Cardiff city strike (I13).", "sources": ""},

    {"id": "C13", "name": "Stormont, Belfast", "cat": "C", "subcat": "Devolved administration",
     "tier": "T2", "lat": 54.6042, "lon": -5.8344, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Northern Ireland Assembly and Executive. Political decapitation of Northern Ireland.",
     "notes": "Covered by Belfast city strike (I14).", "sources": ""},

    # =========================================================
    # D  RAF MAIN OPERATING BASES
    # =========================================================
    {"id": "D01", "name": "RAF Coningsby", "cat": "D", "subcat": "Typhoon QRA South",
     "tier": "T2", "lat": 53.0930, "lon": -0.1658, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Quick Reaction Alert (South). Multiple Typhoon squadrons. Battle of Britain Memorial Flight.",
     "notes": "", "sources": "RAF"},

    {"id": "D02", "name": "RAF Lossiemouth", "cat": "D", "subcat": "Typhoon QRA North + P-8 Poseidon",
     "tier": "T2", "lat": 57.7053, "lon": -3.3392, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "QRA (Interceptor) North. All UK P-8A Poseidon maritime patrol aircraft. Covers GIUK gap ASW.",
     "notes": "", "sources": "RAF"},

    {"id": "D03", "name": "RAF Marham", "cat": "D", "subcat": "F-35B Lightning force",
     "tier": "T2", "lat": 52.6486, "lon": 0.5506, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "617 Sqn and 207 OCU F-35B Lightning. UK's principal strike aircraft base.",
     "notes": "", "sources": "RAF"},

    {"id": "D04", "name": "RAF Waddington", "cat": "D", "subcat": "ISTAR / intelligence aircraft",
     "tier": "T2", "lat": 53.1662, "lon": -0.5236, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "RC-135W Rivet Joint SIGINT, Sentinel R1, Shadow R2, Protector RG1 RPAS. All UK airborne intelligence assets.",
     "notes": "", "sources": "RAF"},

    {"id": "D05", "name": "RAF Brize Norton", "cat": "D", "subcat": "Strategic transport + tanker",
     "tier": "T2", "lat": 51.7500, "lon": -1.5836, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "UK strategic air transport hub. Voyager tanker, C-17, A400M Atlas. Sole air bridge for power projection.",
     "notes": "", "sources": "RAF"},

    {"id": "D06", "name": "RAF Odiham", "cat": "D", "subcat": "Chinook heavy-lift",
     "tier": "T2", "lat": 51.2344, "lon": -0.9428, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Sole Chinook HC6/6A operating base. Critical heavy helicopter lift for land forces.",
     "notes": "", "sources": "RAF"},

    {"id": "D07", "name": "RAF Benson", "cat": "D", "subcat": "Puma medium helicopter",
     "tier": "T2", "lat": 51.6161, "lon": -1.0958, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Puma HC2 squadrons. Medium helicopter lift and JHC support.",
     "notes": "", "sources": "RAF"},

    {"id": "D08", "name": "RAF Wittering", "cat": "D", "subcat": "Logistics + engineering",
     "tier": "T2", "lat": 52.6117, "lon": -0.4719, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "A4 Force HQ. RAF logistics, engineering and force development hub.",
     "notes": "", "sources": "RAF"},

    {"id": "D09", "name": "RAF Northolt", "cat": "D", "subcat": "London VIP + mil transport",
     "tier": "T2", "lat": 51.5531, "lon": -0.4183, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "32 (The Royal) Sqn VIP transport. London CASEVAC. RAF presence in London outskirts.",
     "notes": "", "sources": "RAF"},

    {"id": "D10", "name": "RAF Leeming", "cat": "D", "subcat": "Training + support",
     "tier": "T2", "lat": 54.2925, "lon": -1.5353, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "100 Sqn Hawk T1 aggressor/training. 2 MASU. Northern England RAF support hub.",
     "notes": "", "sources": "RAF"},

    {"id": "D11", "name": "RAF Valley", "cat": "D", "subcat": "Fast-jet pilot training",
     "tier": "T2", "lat": 53.2481, "lon": -4.5353, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "4 FTS Hawk T2. All UK fast-jet pilots train here. Destruction ends pipeline of combat pilots.",
     "notes": "", "sources": "RAF"},

    {"id": "D12", "name": "RAF Cranwell", "cat": "D", "subcat": "Officer + flying training",
     "tier": "T2", "lat": 53.0306, "lon": -0.4828, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "RAF College Cranwell. Basic flying training, officer cadet training. RAF's principal training establishment.",
     "notes": "", "sources": "RAF"},

    {"id": "D13", "name": "RAF Shawbury", "cat": "D", "subcat": "Rotary wing training",
     "tier": "T2", "lat": 52.7983, "lon": -2.6681, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Defence Helicopter Flying School. All three services train rotary-wing pilots here.",
     "notes": "", "sources": "RAF"},

    {"id": "D14", "name": "RAF Boulmer", "cat": "D", "subcat": "Control and Reporting Centre",
     "tier": "T2", "lat": 55.4244, "lon": -1.5814, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Air Surveillance and Control System CRC. Fuses UK radar picture for air defence.",
     "notes": "Also cat G.", "sources": "RAF"},

    {"id": "D15", "name": "RAF Spadeadam", "cat": "D", "subcat": "Electronic warfare range",
     "tier": "T3", "lat": 55.0306, "lon": -2.5500, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Largest electronic warfare tactics range in Europe. EW training for NATO fast jets.",
     "notes": "", "sources": "RAF"},

    # =========================================================
    # E  ROYAL NAVY BASES & FLEET SUPPORT
    # =========================================================
    {"id": "E01", "name": "HMNB Portsmouth", "cat": "E", "subcat": "Carrier + fleet base",
     "tier": "T2", "lat": 50.8036, "lon": -1.1092, "yield_kt": 475, "burst": "air", "height_m": 500,
     "rationale": "Home port of QE-class carriers, Type 45 destroyers, Type 23/26 frigates. Airburst to destroy ships in port and dockyard infrastructure.",
     "notes": "Also cat C (Navy Command nearby) and cat I (Portsmouth city I38).", "sources": "RN"},

    {"id": "E02", "name": "RNAS Yeovilton", "cat": "E", "subcat": "Wildcat + Commando Helicopter",
     "tier": "T2", "lat": 51.0094, "lon": -2.6389, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Wildcat HMA2 maritime attack and Commando Helicopter Force (Merlin Mk4). RM aviation.",
     "notes": "", "sources": "RN"},

    {"id": "E03", "name": "RNAS Culdrose", "cat": "E", "subcat": "Merlin ASW + AEW",
     "tier": "T2", "lat": 50.0864, "lon": -5.2564, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Merlin HM2 ASW and Crowsnest AEW helicopters. Largest helicopter base in Europe.",
     "notes": "", "sources": "RN"},

    {"id": "E04", "name": "HMS Collingwood (Fareham)", "cat": "E", "subcat": "Maritime Warfare School",
     "tier": "T2", "lat": 50.8333, "lon": -1.1667, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Maritime Warfare School and weapons engineering. Largest Royal Navy training establishment.",
     "notes": "", "sources": "RN"},

    {"id": "E05", "name": "HMS Raleigh (Torpoint)", "cat": "E", "subcat": "RN initial training",
     "tier": "T3", "lat": 50.3828, "lon": -4.2097, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Initial naval training for all ratings. Adjacent to Devonport — probably covered by that strike.",
     "notes": "Likely covered by A05 Devonport strike.", "sources": "RN"},

    {"id": "E06", "name": "RNAD Gosport (Frater/Bedenham)", "cat": "E", "subcat": "Naval armament depot",
     "tier": "T2", "lat": 50.8094, "lon": -1.1544, "yield_kt": 475, "burst": "ground", "height_m": 0,
     "rationale": "Royal Naval Armament Depot. Surface fleet munitions storage. Groundburst to destroy ordnance.",
     "notes": "", "sources": "RN, DE&S"},

    {"id": "E07", "name": "DM Glen Douglas", "cat": "E", "subcat": "NATO munitions depot",
     "tier": "T2", "lat": 56.1181, "lon": -4.7642, "yield_kt": 475, "burst": "ground", "height_m": 0,
     "rationale": "Defence Munitions Glen Douglas. Largest conventional munitions depot in Western Europe. NATO-tasked.",
     "notes": "", "sources": "DE&S"},

    {"id": "E08", "name": "Babcock Rosyth Dockyard", "cat": "E", "subcat": "Carrier refit + surface support",
     "tier": "T2", "lat": 56.0194, "lon": -3.4419, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "QE-class carrier assembly site (complete ship assembly here). Ongoing RN surface vessel refit.",
     "notes": "Also cat H (defence industry).", "sources": "Babcock"},

    {"id": "E09", "name": "BUTEC Kyle of Lochalsh", "cat": "E", "subcat": "Underwater test range",
     "tier": "T3", "lat": 57.2778, "lon": -5.7139, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "British Underwater Test and Evaluation Centre. Torpedo and sonar testing range in sea loch.",
     "notes": "", "sources": "QinetiQ"},

    # =========================================================
    # F  ARMY GARRISONS & TRAINING AREAS
    # =========================================================
    {"id": "F01", "name": "Catterick Garrison", "cat": "F", "subcat": "Largest UK army garrison",
     "tier": "T2", "lat": 54.3778, "lon": -1.7244, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Largest British Army garrison. Multiple brigades including 1st (UK) Armoured Infantry. Infantry Training Centre.",
     "notes": "", "sources": "British Army"},

    {"id": "F02", "name": "Aldershot Garrison", "cat": "F", "subcat": "Home of the British Army",
     "tier": "T2", "lat": 51.2528, "lon": -0.7583, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Historic Home of the British Army. Garrison HQ, Army training facilities. Paras relocated to Colchester.",
     "notes": "", "sources": "British Army"},

    {"id": "F03", "name": "Tidworth Garrison", "cat": "F", "subcat": "3 (UK) Div armoured",
     "tier": "T2", "lat": 51.2319, "lon": -1.6633, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Tidworth/Bulford/Larkhill complex. 3 (UK) Division armoured brigades. Salisbury Plain training area.",
     "notes": "Tidworth, Bulford, Larkhill all in same strike area.", "sources": "British Army"},

    {"id": "F04", "name": "Colchester Garrison (Merville Bks)", "cat": "F", "subcat": "16 Air Assault Bde",
     "tier": "T2", "lat": 51.8939, "lon": 0.9114, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Home of 16 Air Assault Brigade — UK's high-readiness rapid reaction force (2 PARA, 3 PARA etc).",
     "notes": "", "sources": "British Army"},

    {"id": "F05", "name": "Edinburgh Garrison (Redford/Dreghorn)", "cat": "F", "subcat": "Army barracks",
     "tier": "T3", "lat": 55.9167, "lon": -3.2464, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Redford and Dreghorn barracks. Army presence in Edinburgh.",
     "notes": "Covered by Edinburgh city strike (I12).", "sources": "British Army"},

    {"id": "F06", "name": "RMA Sandhurst", "cat": "F", "subcat": "Officer training",
     "tier": "T3", "lat": 51.3408, "lon": -0.7119, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Royal Military Academy Sandhurst. Training all British Army officers — destruction severs pipeline.",
     "notes": "", "sources": "British Army"},

    {"id": "F07", "name": "Infantry Training Centre Pirbright", "cat": "F", "subcat": "Phase 1 infantry training",
     "tier": "T3", "lat": 51.3172, "lon": -0.6317, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Phase 1 infantry training. Principal basic training establishment for infantry soldiers.",
     "notes": "", "sources": "British Army"},

    {"id": "F08", "name": "Thiepval Bks, Lisburn (HQ 38 Bde)", "cat": "F", "subcat": "NI Army HQ",
     "tier": "T3", "lat": 54.5167, "lon": -6.0408, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Thiepval Barracks, Lisburn. HQ 38 (Irish) Brigade. Army HQ for Northern Ireland.",
     "notes": "", "sources": "British Army"},

    # =========================================================
    # G  AIR DEFENCE, RADAR, SIGINT, EARLY WARNING
    # =========================================================
    {"id": "G01", "name": "RRH Saxa Vord (Unst, Shetland)", "cat": "G", "subcat": "Air defence radar",
     "tier": "T2", "lat": 60.8250, "lon": -0.8517, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Northernmost UK radar. Air surveillance over Norwegian Sea and GIUK gap. Recently reactivated 2023.",
     "notes": "", "sources": "RAF"},

    {"id": "G02", "name": "RRH Benbecula", "cat": "G", "subcat": "Air defence radar",
     "tier": "T2", "lat": 57.4800, "lon": -7.3633, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Remote Radar Head, Outer Hebrides. Western approaches air defence coverage.",
     "notes": "", "sources": "RAF"},

    {"id": "G03", "name": "RRH Buchan", "cat": "G", "subcat": "Air defence radar",
     "tier": "T2", "lat": 57.4719, "lon": -1.8767, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Remote Radar Head Buchan. Scottish east coast air surveillance. Former Master Diversion Airfield.",
     "notes": "", "sources": "RAF"},

    {"id": "G04", "name": "RRH Brizlee Wood", "cat": "G", "subcat": "Air defence radar",
     "tier": "T3", "lat": 55.4183, "lon": -1.8183, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Remote Radar Head. NE England coastal air surveillance.",
     "notes": "", "sources": "RAF"},

    {"id": "G05", "name": "RRH Staxton Wold", "cat": "G", "subcat": "Air defence radar",
     "tier": "T3", "lat": 54.1994, "lon": -0.4161, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Remote Radar Head, Yorkshire coast. Oldest continually operated radar site in UK.",
     "notes": "", "sources": "RAF"},

    {"id": "G06", "name": "RRH Portreath", "cat": "G", "subcat": "Air defence radar",
     "tier": "T3", "lat": 50.2508, "lon": -5.2878, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Remote Radar Head. South-west approaches air coverage.",
     "notes": "", "sources": "RAF"},

    {"id": "G07", "name": "GCHQ Bude (Morwenstow satellite station)", "cat": "G", "subcat": "Satellite SIGINT + cable tap",
     "tier": "T2", "lat": 50.8911, "lon": -4.5544, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "GCHQ satellite intercept station. Adjacent to primary transatlantic cable landings (Widemouth Bay). Taps both satellite and undersea fibre.",
     "notes": "Also cat N.", "sources": "GCHQ"},

    {"id": "G08", "name": "GCHQ Scarborough (Irton Moor)", "cat": "G", "subcat": "HF SIGINT",
     "tier": "T2", "lat": 54.2567, "lon": -0.4839, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "HF direction-finding and SIGINT station. Part of GCHQ's regional collection network.",
     "notes": "", "sources": "GCHQ"},

    {"id": "G09", "name": "DIS Chicksands", "cat": "G", "subcat": "Defence Intelligence",
     "tier": "T3", "lat": 52.0258, "lon": -0.3814, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Defence Intelligence Security Centre / DISC. Former NSA/GCHQ Chicksands site. Military intelligence training.",
     "notes": "", "sources": "MoD"},

    # =========================================================
    # H  DEFENCE INDUSTRY & SHIPBUILDING
    # =========================================================
    {"id": "H01", "name": "BAE Systems Warton", "cat": "H", "subcat": "Typhoon/F-35 final assembly + Tempest",
     "tier": "T2", "lat": 53.7453, "lon": -2.8839, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Typhoon Eurofighter final assembly, F-35 rear fuselage production, GCAP/Tempest development. UK's principal combat aircraft plant.",
     "notes": "Adjacent to Samlesbury (H02).", "sources": "BAE Systems"},

    {"id": "H02", "name": "BAE Systems Samlesbury", "cat": "H", "subcat": "F-35 + Typhoon fuselage",
     "tier": "T2", "lat": 53.7761, "lon": -2.5733, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "F-35B rear fuselage and Typhoon airframe structures. Sister site to Warton 12 miles away.",
     "notes": "", "sources": "BAE Systems"},

    {"id": "H03", "name": "BAE Systems Scotstoun", "cat": "H", "subcat": "Type 26/31 frigates",
     "tier": "T2", "lat": 55.8753, "lon": -4.3533, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Assembly of Type 26 City-class frigates (ASW hull). Adjacent to Govan.",
     "notes": "Adjacent to H04 Govan on Clyde.", "sources": "BAE Systems"},

    {"id": "H04", "name": "BAE Systems Govan", "cat": "H", "subcat": "Type 26/31 frigates",
     "tier": "T2", "lat": 55.8681, "lon": -4.3075, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Hull block fabrication for Type 26 frigates. Paired operation with Scotstoun on the Clyde.",
     "notes": "", "sources": "BAE Systems"},

    {"id": "H05", "name": "Thales UK Glasgow (Linthouse)", "cat": "H", "subcat": "Sonar + optronics",
     "tier": "T3", "lat": 55.8778, "lon": -4.2361, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Thales UK. Sonar suites for RN submarines, optronic mast systems, ship radar.",
     "notes": "", "sources": "Thales UK"},

    {"id": "H06", "name": "MBDA Stevenage", "cat": "H", "subcat": "Missile design HQ",
     "tier": "T2", "lat": 51.9033, "lon": -0.2019, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "MBDA UK HQ and design centre. Meteor, Brimstone, CAMM/Sea Ceptor, SPEAR, legacy Storm Shadow. UK's primary missile design capability.",
     "notes": "", "sources": "MBDA"},

    {"id": "H07", "name": "MBDA Lostock (Bolton)", "cat": "H", "subcat": "Missile production",
     "tier": "T3", "lat": 53.5869, "lon": -2.4617, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "MBDA production facility. CAMM/Sea Ceptor manufacture.",
     "notes": "", "sources": "MBDA"},

    {"id": "H08", "name": "Leonardo UK Edinburgh (Crewe Toll)", "cat": "H", "subcat": "Airborne radars + EW",
     "tier": "T3", "lat": 55.9344, "lon": -3.2692, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Captor-E/M radar (Typhoon/F-35), Osprey AESA, DAS systems. Sole UK airborne radar OEM.",
     "notes": "Covered by Edinburgh city strike (I12).", "sources": "Leonardo UK"},

    {"id": "H09", "name": "Leonardo UK Luton", "cat": "H", "subcat": "Defensive aids + EW",
     "tier": "T3", "lat": 51.8797, "lon": -0.4047, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Defensive Aids Sub-System, laser warning, EW systems for UK combat aircraft.",
     "notes": "", "sources": "Leonardo UK"},

    {"id": "H10", "name": "QinetiQ Boscombe Down", "cat": "H", "subcat": "Military flight test",
     "tier": "T2", "lat": 51.1519, "lon": -1.7472, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "UK Military Flying Test and Evaluation centre. Empire Test Pilots School. All UK military aircraft cleared here.",
     "notes": "", "sources": "QinetiQ"},

    {"id": "H11", "name": "DSTL Porton Down", "cat": "H", "subcat": "CBRN defence research",
     "tier": "T2", "lat": 51.1233, "lon": -1.7014, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Defence Science and Technology Laboratory. Chemical and biological defence research. Historic significance.",
     "notes": "", "sources": "DSTL"},

    {"id": "H12", "name": "QinetiQ Farnborough", "cat": "H", "subcat": "Defence research HQ",
     "tier": "T3", "lat": 51.2833, "lon": -0.7500, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "QinetiQ HQ. Historic RAE site. Wide-spectrum defence R&D.",
     "notes": "", "sources": "QinetiQ"},

    {"id": "H13", "name": "QinetiQ Portsdown Technology Park", "cat": "H", "subcat": "Maritime sensors + underwater R&D",
     "tier": "T3", "lat": 50.8533, "lon": -1.1086, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Maritime sensor systems, underwater weapons research. Portsdown West site.",
     "notes": "Portsmouth area — overlap with HMNB strike.", "sources": "QinetiQ"},

    {"id": "H14", "name": "QinetiQ Aberporth", "cat": "H", "subcat": "Weapons test range",
     "tier": "T3", "lat": 52.1389, "lon": -4.5683, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "West Wales test range. Air-to-surface and air-to-ground weapons qualification, UAV trials.",
     "notes": "", "sources": "QinetiQ"},

    {"id": "H15", "name": "Rolls-Royce Sinfin, Derby", "cat": "H", "subcat": "Aero engine manufacturing",
     "tier": "T3", "lat": 52.8953, "lon": -1.4839, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Rolls-Royce aero engine manufacture (EJ200 for Typhoon). Derby — overlap with Raynesway (A07) and Derby city (I20).",
     "notes": "Covered partly by Derby/A07 strikes.", "sources": "Rolls-Royce"},

    # =========================================================
    # I  POPULATION CENTRES (counter-value)
    # =========================================================
    {"id": "I01", "name": "London — City / East", "cat": "I", "subcat": "Financial + Docklands",
     "tier": "T3", "lat": 51.5144, "lon": -0.0919, "yield_kt": 800, "burst": "air", "height_m": 2000,
     "rationale": "City of London financial district, Bank of England, Docklands data centres. GZ 1 of 3 for London.",
     "notes": "Multi-GZ pattern with I02 and I03.", "sources": "ONS"},

    {"id": "I02", "name": "London — Westminster / Whitehall", "cat": "I", "subcat": "Government centre",
     "tier": "T3", "lat": 51.5007, "lon": -0.1246, "yield_kt": 800, "burst": "air", "height_m": 2000,
     "rationale": "Parliament, Whitehall, Downing St, MoD, PINDAR, MI5, MI6. GZ 2 of 3 for London. Decapitates UK government.",
     "notes": "Covers C01, C08, C09.", "sources": "ONS"},

    {"id": "I03", "name": "London — West / Slough corridor", "cat": "I", "subcat": "Industry + data centre cluster",
     "tier": "T3", "lat": 51.4700, "lon": -0.3800, "yield_kt": 800, "burst": "air", "height_m": 2000,
     "rationale": "West London industrial + transport + Slough data centre cluster. GZ 3 of 3 for London.",
     "notes": "Covers O01 (Slough DCs) and Heathrow (P01) on periphery.", "sources": "ONS"},

    {"id": "I04", "name": "Birmingham", "cat": "I", "subcat": "2nd largest city",
     "tier": "T3", "lat": 52.4862, "lon": -1.8904, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "2nd largest UK city (~1.15M). Midlands industrial and commercial heartland.",
     "notes": "", "sources": "ONS"},

    {"id": "I05", "name": "Manchester", "cat": "I", "subcat": "NW England regional capital",
     "tier": "T3", "lat": 53.4808, "lon": -2.2426, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Greater Manchester ~2.9M. NW England economic hub. Major logistics, tech and media centre.",
     "notes": "", "sources": "ONS"},

    {"id": "I06", "name": "Glasgow", "cat": "I", "subcat": "Scotland's largest city",
     "tier": "T3", "lat": 55.8642, "lon": -4.2518, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Greater Glasgow ~1.85M. Scotland's largest urban area. Naval shipbuilding on the Clyde.",
     "notes": "Covers H03/H04 Govan/Scotstoun shipyards.", "sources": "ONS"},

    {"id": "I07", "name": "Liverpool", "cat": "I", "subcat": "NW England port city",
     "tier": "T3", "lat": 53.4084, "lon": -2.9916, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Merseyside ~1.4M. Major Atlantic port and container terminal. Regional industrial hub.",
     "notes": "", "sources": "ONS"},

    {"id": "I08", "name": "Leeds", "cat": "I", "subcat": "Yorkshire financial centre",
     "tier": "T3", "lat": 53.8008, "lon": -1.5491, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "West Yorkshire financial and commercial centre. ~800k city, ~1.8M metro.",
     "notes": "", "sources": "ONS"},

    {"id": "I09", "name": "Sheffield", "cat": "I", "subcat": "Steel and engineering",
     "tier": "T3", "lat": 53.3811, "lon": -1.4701, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Historic steel and engineering city. Advanced manufacturing cluster. Pop ~580k.",
     "notes": "", "sources": "ONS"},

    {"id": "I10", "name": "Bristol", "cat": "I", "subcat": "SW England aerospace",
     "tier": "T3", "lat": 51.4545, "lon": -2.5879, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Aerospace industry (Airbus Filton, GKN). Port of Bristol. Pop ~470k.",
     "notes": "", "sources": "ONS"},

    {"id": "I11", "name": "Newcastle upon Tyne", "cat": "I", "subcat": "NE England regional capital",
     "tier": "T3", "lat": 54.9783, "lon": -1.6178, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Tyneside conurbation ~780k. NE regional capital.",
     "notes": "", "sources": "ONS"},

    {"id": "I12", "name": "Edinburgh", "cat": "I", "subcat": "Scottish capital",
     "tier": "T3", "lat": 55.9533, "lon": -3.1883, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Scotland's capital. Financial services hub. ~510k city. Scottish Parliament (C12) nearby.",
     "notes": "Covers C12 Holyrood and H08 Leonardo.", "sources": "ONS"},

    {"id": "I13", "name": "Cardiff", "cat": "I", "subcat": "Welsh capital",
     "tier": "T3", "lat": 51.4816, "lon": -3.1791, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Capital of Wales. Administrative and commercial centre. ~365k city.",
     "notes": "Covers C13 Senedd.", "sources": "ONS"},

    {"id": "I14", "name": "Belfast", "cat": "I", "subcat": "NI capital",
     "tier": "T3", "lat": 54.5973, "lon": -5.9301, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Capital of Northern Ireland. Aerospace industry (Spirit Aero, former Short Brothers). ~345k.",
     "notes": "Covers C14 Stormont.", "sources": "ONS"},

    {"id": "I15", "name": "Nottingham", "cat": "I", "subcat": "East Midlands",
     "tier": "T3", "lat": 52.9548, "lon": -1.1581, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "East Midlands regional centre. ~330k city. Pharmaceutical manufacturing.",
     "notes": "", "sources": "ONS"},

    {"id": "I16", "name": "Southampton", "cat": "I", "subcat": "S coast port city",
     "tier": "T3", "lat": 50.9097, "lon": -1.4044, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "South coast port — container, cruise and ro-ro. Pop ~270k. Adjacent Fawley refinery.",
     "notes": "Overlap with J01/L01.", "sources": "ONS"},

    {"id": "I17", "name": "Portsmouth", "cat": "I", "subcat": "RN city",
     "tier": "T3", "lat": 50.8198, "lon": -1.0880, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Royal Navy HQ city. Pop ~215k. Probably covered by HMNB Portsmouth strike.",
     "notes": "Overlap E01/C05.", "sources": "ONS"},

    {"id": "I18", "name": "Plymouth", "cat": "I", "subcat": "SW naval city",
     "tier": "T3", "lat": 50.3755, "lon": -4.1427, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "UK's largest naval city. Pop ~264k. Largely covered by HMNB Devonport strike.",
     "notes": "Overlap A05.", "sources": "ONS"},

    {"id": "I19", "name": "Leicester", "cat": "I", "subcat": "East Midlands",
     "tier": "T3", "lat": 52.6369, "lon": -1.1398, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "East Midlands manufacturing and commercial city. Pop ~370k.",
     "notes": "", "sources": "ONS"},

    {"id": "I20", "name": "Coventry", "cat": "I", "subcat": "Midlands engineering",
     "tier": "T3", "lat": 52.4068, "lon": -1.5197, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "West Midlands automotive and engineering. Pop ~345k. Rebuilt after WWII blitz.",
     "notes": "", "sources": "ONS"},

    {"id": "I21", "name": "Stoke-on-Trent", "cat": "I", "subcat": "Midlands industrial",
     "tier": "T3", "lat": 53.0027, "lon": -2.1794, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Midlands industrial city. Pop ~260k.",
     "notes": "", "sources": "ONS"},

    {"id": "I22", "name": "Wolverhampton", "cat": "I", "subcat": "West Midlands",
     "tier": "T3", "lat": 52.5862, "lon": -2.1282, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "West Midlands industrial city. Pop ~260k. Engineering and manufacturing.",
     "notes": "", "sources": "ONS"},

    {"id": "I23", "name": "Derby", "cat": "I", "subcat": "Aerospace + rail engineering",
     "tier": "T3", "lat": 52.9225, "lon": -1.4746, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Rolls-Royce HQ, Toyota, Bombardier trains. Pop ~260k. Overlap with A07 Raynesway.",
     "notes": "Overlap A07, H15.", "sources": "ONS"},

    {"id": "I24", "name": "Reading", "cat": "I", "subcat": "Thames Valley tech hub",
     "tier": "T3", "lat": 51.4543, "lon": -0.9781, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Thames Valley tech corridor HQ cluster. Pop ~320k. 10 miles from AWE Aldermaston.",
     "notes": "", "sources": "ONS"},

    {"id": "I25", "name": "Milton Keynes", "cat": "I", "subcat": "New city",
     "tier": "T3", "lat": 52.0406, "lon": -0.7594, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "New city, logistics hub. Pop ~290k. Strategic road junction (M1/A5).",
     "notes": "", "sources": "ONS"},

    {"id": "I26", "name": "Cambridge", "cat": "I", "subcat": "Science and tech cluster",
     "tier": "T3", "lat": 52.2053, "lon": 0.1218, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Cambridge science and biotech cluster. ARM Holdings, AstraZeneca, Mott MacDonald. Pop ~145k.",
     "notes": "", "sources": "ONS"},

    {"id": "I27", "name": "Oxford", "cat": "I", "subcat": "Academic and tech",
     "tier": "T3", "lat": 51.7520, "lon": -1.2577, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "University and tech cluster. BMW MINI plant. Pop ~160k.",
     "notes": "", "sources": "ONS"},

    {"id": "I28", "name": "Swansea", "cat": "I", "subcat": "South Wales",
     "tier": "T3", "lat": 51.6214, "lon": -3.9436, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "South Wales industrial and port city. Pop ~240k.",
     "notes": "", "sources": "ONS"},

    {"id": "I29", "name": "Aberdeen", "cat": "I", "subcat": "North Sea oil capital",
     "tier": "T3", "lat": 57.1497, "lon": -2.0943, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "North Sea oil and gas industry hub. Port and logistics. Pop ~200k.",
     "notes": "", "sources": "ONS"},

    {"id": "I30", "name": "Dundee", "cat": "I", "subcat": "East Scotland",
     "tier": "T3", "lat": 56.4620, "lon": -2.9707, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Scottish east coast city. Tech sector (video games — Rockstar/DC Thompson), biomedical. Pop ~150k.",
     "notes": "", "sources": "ONS"},

    {"id": "I31", "name": "Kingston upon Hull", "cat": "I", "subcat": "E Yorkshire port",
     "tier": "T3", "lat": 53.7456, "lon": -0.3367, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Humber estuary port city. Siemens wind turbine manufacture. Pop ~260k.",
     "notes": "", "sources": "ONS"},

    {"id": "I32", "name": "Middlesbrough / Teesside", "cat": "I", "subcat": "Industrial NE",
     "tier": "T3", "lat": 54.5742, "lon": -1.2349, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Teesside industrial conurbation. Steel, chemicals, Wilton industrial complex. ~300k area.",
     "notes": "", "sources": "ONS"},

    {"id": "I33", "name": "Sunderland", "cat": "I", "subcat": "NE England",
     "tier": "T3", "lat": 54.9069, "lon": -1.3833, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "NE port city. Nissan UK car plant — largest single car factory in UK. Pop ~275k.",
     "notes": "", "sources": "ONS"},

    {"id": "I34", "name": "Preston", "cat": "I", "subcat": "Lancashire",
     "tier": "T3", "lat": 53.7632, "lon": -2.7031, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Lancashire city. Near BAE Warton (H01) and Samlesbury (H02). Pop ~140k.",
     "notes": "", "sources": "ONS"},

    {"id": "I35", "name": "Brighton and Hove", "cat": "I", "subcat": "South coast",
     "tier": "T3", "lat": 50.8225, "lon": -0.1372, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "South coast. ~280k. University city, secondary commuter city for London.",
     "notes": "", "sources": "ONS"},

    {"id": "I36", "name": "Bournemouth / Poole", "cat": "I", "subcat": "South coast conurbation",
     "tier": "T3", "lat": 50.7192, "lon": -1.8808, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "South coast conurbation ~470k including Christchurch. SBS HQ at Poole (C11).",
     "notes": "Overlap C11 Poole SBS.", "sources": "ONS"},

    {"id": "I37", "name": "Norwich", "cat": "I", "subcat": "East Anglia",
     "tier": "T3", "lat": 52.6309, "lon": 1.2974, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "East Anglia regional centre. ~145k. Insurance/financial sector.",
     "notes": "", "sources": "ONS"},

    {"id": "I38", "name": "York", "cat": "I", "subcat": "Yorkshire",
     "tier": "T3", "lat": 53.9600, "lon": -1.0873, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "North Yorkshire. ~210k. Railway engineering (National Railway Museum, train maintenance).",
     "notes": "", "sources": "ONS"},

    {"id": "I39", "name": "Peterborough", "cat": "I", "subcat": "East",
     "tier": "T3", "lat": 52.5695, "lon": -0.2405, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Eastern England logistics hub. ~215k. A1/East Coast Main Line junction.",
     "notes": "", "sources": "ONS"},

    # =========================================================
    # J  PORTS & MARITIME LOGISTICS
    # =========================================================
    {"id": "J01", "name": "Port of Felixstowe", "cat": "J", "subcat": "Container port",
     "tier": "T2", "lat": 51.9539, "lon": 1.3511, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Britain's busiest container port. ~40% of UK container trade. Hutchison Ports.",
     "notes": "", "sources": "Felixstowe"},

    {"id": "J02", "name": "London Gateway", "cat": "J", "subcat": "Deep-water container port",
     "tier": "T2", "lat": 51.5158, "lon": 0.5000, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "DP World London Gateway. Deep-water container port on Thames. Adjacent data centre park.",
     "notes": "", "sources": "DP World"},

    {"id": "J03", "name": "Port of Tilbury", "cat": "J", "subcat": "General cargo + container",
     "tier": "T3", "lat": 51.4667, "lon": 0.3500, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Port of Tilbury. London's primary grain and bulk port. ro-ro and container.",
     "notes": "", "sources": "Forth Ports"},

    {"id": "J04", "name": "Liverpool / Birkenhead (Mersey Docks)", "cat": "J", "subcat": "Atlantic container port",
     "tier": "T2", "lat": 53.4419, "lon": -3.0069, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Mersey Docks container terminal at Seaforth. Main Atlantic container port for NW England.",
     "notes": "Covered partly by Liverpool city strike (I07).", "sources": "Peel Ports"},

    {"id": "J05", "name": "Port of Immingham", "cat": "J", "subcat": "Largest UK port by tonnage",
     "tier": "T2", "lat": 53.6306, "lon": -0.1814, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Largest UK port by tonnage. Oil, coal, bulk cargo. Drax biomass imports.",
     "notes": "", "sources": "ABP"},

    {"id": "J06", "name": "Port of Dover", "cat": "J", "subcat": "Cross-Channel ferry",
     "tier": "T2", "lat": 51.1261, "lon": 1.3139, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "~40% of UK ro-ro freight with the continent. Cross-Channel chokepoint.",
     "notes": "", "sources": "Port of Dover"},

    {"id": "J07", "name": "Milford Haven", "cat": "J", "subcat": "LNG + oil port",
     "tier": "T2", "lat": 51.7097, "lon": -5.0461, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "UK's 2nd largest port by tonnage. South Hook and Dragon LNG terminals. Valero refinery.",
     "notes": "Overlap L10, L11, L04.", "sources": "Milford Haven Port Authority"},

    {"id": "J08", "name": "Port of Grimsby", "cat": "J", "subcat": "Humber port",
     "tier": "T3", "lat": 53.5742, "lon": -0.0714, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Humber estuary. Adjacent to Immingham. Ro-ro and bulk.",
     "notes": "", "sources": "ABP"},

    {"id": "J09", "name": "Belfast Harbour", "cat": "J", "subcat": "NI main port",
     "tier": "T3", "lat": 54.6167, "lon": -5.9000, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Main Northern Ireland port. Harland and Wolff adjacent (Spirit Aero/H&W repair).",
     "notes": "Covered by Belfast city strike (I14).", "sources": "Belfast Harbour Commissioners"},

    {"id": "J10", "name": "Greenock / Clydeport", "cat": "J", "subcat": "Clyde container port",
     "tier": "T3", "lat": 55.9533, "lon": -4.7667, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Clydeport Greenock Ocean Terminal. Container and cruise. Clyde approaches.",
     "notes": "", "sources": "Peel Ports"},

    # =========================================================
    # K  ENERGY — NUCLEAR (power, reprocessing, enrichment)
    # =========================================================
    {"id": "K01", "name": "Sellafield", "cat": "K", "subcat": "Reprocessing + legacy high-level waste",
     "tier": "T2", "lat": 54.4208, "lon": -3.4961, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Magnox reprocessing, THORP, ~140 tonnes Pu stored, high-level waste tanks, legacy ponds. Single most radiologically hazardous target in the UK. Groundburst to contaminate site and deny access.",
     "notes": "Arguably strategic counterforce-level target due to Pu inventory.", "sources": "NDA"},

    {"id": "K02", "name": "Capenhurst (Urenco UK)", "cat": "K", "subcat": "Uranium enrichment",
     "tier": "T2", "lat": 53.2617, "lon": -2.9444, "yield_kt": 475, "burst": "ground", "height_m": 0,
     "rationale": "Urenco UK centrifuge enrichment plant. Sole UK uranium enrichment capability. Also stores depleted uranium.",
     "notes": "", "sources": "Urenco"},

    {"id": "K03", "name": "Hinkley Point C (Somerset)", "cat": "K", "subcat": "Nuclear power (new build)",
     "tier": "T2", "lat": 51.2081, "lon": -3.1328, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "EDF Hinkley Point C EPR under construction (~7% future UK electricity). Groundburst to contaminate and prevent completion.",
     "notes": "Hinkley Point B decommissioning adjacent.", "sources": "EDF"},

    {"id": "K04", "name": "Sizewell B + C (Suffolk)", "cat": "K", "subcat": "Nuclear power",
     "tier": "T2", "lat": 52.2142, "lon": 1.6200, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Sizewell B PWR (active) + Sizewell C planned. ~3% of current UK electricity.",
     "notes": "", "sources": "EDF"},

    {"id": "K05", "name": "Heysham 1 + 2 (Lancashire)", "cat": "K", "subcat": "Nuclear power",
     "tier": "T2", "lat": 54.0292, "lon": -2.9158, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Two active AGR stations. UK's largest nuclear generating site. ~10% of national nuclear capacity.",
     "notes": "", "sources": "EDF"},

    {"id": "K06", "name": "Hartlepool AGR", "cat": "K", "subcat": "Nuclear power",
     "tier": "T2", "lat": 54.6350, "lon": -1.1808, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Active AGR station on Teesside. Contributing to grid.",
     "notes": "", "sources": "EDF"},

    {"id": "K07", "name": "Torness AGR (East Lothian)", "cat": "K", "subcat": "Nuclear power",
     "tier": "T2", "lat": 55.9681, "lon": -2.4069, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Active AGR station south-east of Edinburgh. Scotland's only currently active nuclear power plant.",
     "notes": "", "sources": "EDF"},

    {"id": "K08", "name": "Dungeness B (Kent)", "cat": "K", "subcat": "Nuclear power (defuelling)",
     "tier": "T3", "lat": 50.9136, "lon": 0.9614, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "AGR in defuelling phase. Spent fuel on site — contamination risk.",
     "notes": "", "sources": "EDF"},

    {"id": "K09", "name": "Bradwell (Essex)", "cat": "K", "subcat": "Nuclear decommissioning",
     "tier": "T3", "lat": 51.7431, "lon": 0.8958, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Magnox decommissioning, Essex coast. Spent fuel in interim storage.",
     "notes": "", "sources": "NDA"},

    {"id": "K10", "name": "Trawsfynydd (N Wales)", "cat": "K", "subcat": "Nuclear decommissioning",
     "tier": "T3", "lat": 52.9236, "lon": -3.9467, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Magnox decommissioning. Proposed SMR candidate site. Radioactive inventory on site.",
     "notes": "", "sources": "NDA"},

    {"id": "K11", "name": "Chapelcross (Dumfriesshire)", "cat": "K", "subcat": "Nuclear decommissioning",
     "tier": "T3", "lat": 55.0167, "lon": -3.2361, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Former Magnox. Historically produced tritium for nuclear weapons. Decommissioning.",
     "notes": "", "sources": "NDA"},

    {"id": "K12", "name": "Dounreay (Caithness)", "cat": "K", "subcat": "Nuclear decommissioning",
     "tier": "T3", "lat": 58.5789, "lon": -3.7519, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Historic fast-reactor site. Significant radioactive inventory in decommissioning. Remote but significant.",
     "notes": "", "sources": "NDA"},

    # =========================================================
    # L  ENERGY — OIL, GAS & LNG
    # =========================================================
    {"id": "L01", "name": "Fawley Refinery", "cat": "L", "subcat": "Oil refinery",
     "tier": "T2", "lat": 50.8344, "lon": -1.3439, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "ExxonMobil Fawley. Largest UK refinery, ~20% capacity. Feeds South England, Heathrow jet fuel. Adjacent Southampton.",
     "notes": "", "sources": "ExxonMobil"},

    {"id": "L02", "name": "Stanlow Refinery", "cat": "L", "subcat": "Oil refinery",
     "tier": "T2", "lat": 53.2806, "lon": -2.8619, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "EET Fuels (ex-Essar) Stanlow, Cheshire. Second largest UK refinery. Feeds NW England.",
     "notes": "", "sources": "EET Fuels"},

    {"id": "L03", "name": "Grangemouth Refinery / Petrochemicals", "cat": "L", "subcat": "Oil refinery + petrochemicals",
     "tier": "T2", "lat": 56.0075, "lon": -3.7094, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Petroineos Grangemouth. Scotland's only refinery (transitioning 2025+). Only ethylene cracker in Scotland.",
     "notes": "Status in transition — may close as refinery.", "sources": "Petroineos"},

    {"id": "L04", "name": "Pembroke Refinery (Valero)", "cat": "L", "subcat": "Oil refinery",
     "tier": "T2", "lat": 51.6833, "lon": -4.9833, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Valero Pembroke, Wales. ~10 million tpa. One of largest European refineries.",
     "notes": "", "sources": "Valero"},

    {"id": "L05", "name": "Lindsey Oil Refinery (Humber)", "cat": "L", "subcat": "Oil refinery",
     "tier": "T2", "lat": 53.6400, "lon": -0.2014, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Prax Group, North Lincolnshire. Humber refinery complex.",
     "notes": "Adjacent to L06.", "sources": "Prax"},

    {"id": "L06", "name": "St Fergus Gas Terminal", "cat": "L", "subcat": "Gas import terminal",
     "tier": "T2", "lat": 57.5544, "lon": -1.8400, "yield_kt": 475, "burst": "ground", "height_m": 0,
     "rationale": "~40% of UK gas lands here via North Sea and Norwegian Vesterled pipeline. Destroying it collapses UK gas supply. Strategic energy chokepoint.",
     "notes": "Hardened/buried pipework — groundburst.", "sources": "National Gas"},

    {"id": "L07", "name": "Bacton Gas Terminal (Norfolk)", "cat": "L", "subcat": "Gas import terminal",
     "tier": "T2", "lat": 52.8519, "lon": 1.4494, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "North Sea gas plus BBL (NL) and IUK (BE) interconnectors. Second key gas entry point for UK.",
     "notes": "", "sources": "National Gas"},

    {"id": "L08", "name": "Easington Gas Terminal (E Yorks)", "cat": "L", "subcat": "Gas import terminal",
     "tier": "T2", "lat": 53.6500, "lon": 0.1400, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Langeled pipeline from Norway terminates here (~20% of UK gas). East Yorkshire coast.",
     "notes": "", "sources": "Equinor"},

    {"id": "L09", "name": "South Hook LNG (Milford Haven)", "cat": "L", "subcat": "LNG import terminal",
     "tier": "T2", "lat": 51.7050, "lon": -5.0550, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "QatarEnergy/ExxonMobil. Largest UK LNG import terminal. Critical winter peak-shaving capacity.",
     "notes": "Overlap J07.", "sources": "South Hook LNG"},

    {"id": "L10", "name": "Isle of Grain LNG (Kent)", "cat": "L", "subcat": "LNG import terminal",
     "tier": "T2", "lat": 51.4472, "lon": 0.7164, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "National Gas Grain LNG — largest UK LNG storage by volume. Thames Estuary. IFA interconnector nearby.",
     "notes": "Overlap M04 Sellindge.", "sources": "National Gas"},

    {"id": "L11", "name": "Dragon LNG (Milford Haven)", "cat": "L", "subcat": "LNG import terminal",
     "tier": "T3", "lat": 51.6956, "lon": -5.0358, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Second Milford Haven LNG terminal. Shell/Ancala. Adjacent to South Hook.",
     "notes": "", "sources": "Dragon LNG"},

    {"id": "L12", "name": "Sullom Voe Oil Terminal (Shetland)", "cat": "L", "subcat": "Oil terminal",
     "tier": "T3", "lat": 60.4558, "lon": -1.3239, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "North Sea and West of Shetland oil terminal. BP-operated. Critical to N Sea production.",
     "notes": "", "sources": "BP"},

    {"id": "L13", "name": "Flotta Oil Terminal (Orkney)", "cat": "L", "subcat": "Oil terminal",
     "tier": "T3", "lat": 58.8333, "lon": -3.1333, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Repsol/Repsol Sinopec oil terminal, Orkney. Piper/Claymore/Flotta field output.",
     "notes": "", "sources": "Repsol"},

    # =========================================================
    # M  ELECTRICITY TRANSMISSION & GENERATION
    # =========================================================
    {"id": "M01", "name": "Drax Power Station (N Yorks)", "cat": "M", "subcat": "Biomass power",
     "tier": "T2", "lat": 53.7358, "lon": -0.9986, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Drax — UK's largest power station by capacity (~3.9 GW). ~6% of UK electricity. Biomass + CCS.",
     "notes": "", "sources": "Drax"},

    {"id": "M02", "name": "Dinorwig (Llanberis, N Wales)", "cat": "M", "subcat": "Pumped storage",
     "tier": "T3", "lat": 53.1194, "lon": -4.1133, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Electric Mountain pumped storage, 1.7 GW. Critical for grid frequency stability during peak demand.",
     "notes": "", "sources": "Engie"},

    {"id": "M03", "name": "Cruachan (Argyll)", "cat": "M", "subcat": "Pumped storage",
     "tier": "T3", "lat": 56.3942, "lon": -5.1150, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Hollow Mountain pumped storage, 440 MW. Scottish grid stability.",
     "notes": "", "sources": "Drax"},

    {"id": "M04", "name": "Sellindge / Folkestone (IFA HVDC)", "cat": "M", "subcat": "UK-France interconnector",
     "tier": "T2", "lat": 51.1025, "lon": 1.0222, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "IFA and IFA2 UK converter stations. 2 GW to France. Destroying severs major import/export link.",
     "notes": "", "sources": "National Grid"},

    {"id": "M05", "name": "Richborough (Nemo Link)", "cat": "M", "subcat": "UK-Belgium interconnector",
     "tier": "T3", "lat": 51.2883, "lon": 1.3261, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Nemo Link 1 GW HVDC converter station at Richborough, Kent. UK-Belgium.",
     "notes": "", "sources": "National Grid"},

    {"id": "M06", "name": "Bicker Fen (Viking Link)", "cat": "M", "subcat": "UK-Denmark interconnector",
     "tier": "T3", "lat": 52.9275, "lon": -0.1022, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Viking Link 1.4 GW HVDC converter station near Boston, Lincs. UK-Denmark.",
     "notes": "", "sources": "National Grid"},

    {"id": "M07", "name": "National Grid ESO Control Centre (Wokingham)", "cat": "M", "subcat": "Grid control",
     "tier": "T2", "lat": 51.4011, "lon": -0.7953, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "National Grid Electricity System Operator main control centre. UK transmission system operation.",
     "notes": "", "sources": "NESO"},

    {"id": "M08", "name": "Iron Acton 400kV Substation", "cat": "M", "subcat": "400 kV super-grid node",
     "tier": "T3", "lat": 51.5500, "lon": -2.4750, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Major 400 kV super-grid node, South Gloucestershire. SW England grid hub.",
     "notes": "", "sources": "National Grid"},

    {"id": "M09", "name": "Wylfa (Anglesey)", "cat": "M", "subcat": "Nuclear decom + major grid node",
     "tier": "T3", "lat": 53.4167, "lon": -4.4833, "yield_kt": 100, "burst": "ground", "height_m": 0,
     "rationale": "Wylfa Magnox decommissioning and 400 kV super-grid substation. Future large-scale nuclear candidate site.",
     "notes": "", "sources": "NDA, National Grid"},

    # =========================================================
    # N  TELECOMS, UNDERSEA CABLES, SATELLITE GROUND STATIONS
    # =========================================================
    {"id": "N01", "name": "Widemouth Bay cable landing (Cornwall)", "cat": "N", "subcat": "Transatlantic cable bundle",
     "tier": "T2", "lat": 50.7919, "lon": -4.5561, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Primary UK transatlantic cable bundle: TAT-14, Apollo North, Yellow, FLAG Atlantic, AEConnect. Severs most UK-US fibre capacity.",
     "notes": "GCHQ Bude 3 miles north (G07).", "sources": "TeleGeography"},

    {"id": "N02", "name": "Oxwich Bay cable landing (S Wales)", "cat": "N", "subcat": "Transatlantic cable",
     "tier": "T2", "lat": 51.5519, "lon": -4.1600, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Amitie, 2Africa and other major cables landing S Wales coast. Growing strategic importance.",
     "notes": "", "sources": "TeleGeography"},

    {"id": "N03", "name": "Goonhilly Earth Station (Cornwall)", "cat": "N", "subcat": "Satellite + cable",
     "tier": "T2", "lat": 50.0472, "lon": -5.1825, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Major satellite uplink facility (GEO, MEO, deep space). Adjacent undersea cable landings at Porthcurno.",
     "notes": "Also covers nearby Porthcurno.", "sources": "Goonhilly Earth Station"},

    {"id": "N04", "name": "Highbridge / Brean (Somerset)", "cat": "N", "subcat": "Cable landing",
     "tier": "T3", "lat": 51.2972, "lon": -3.0208, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "TAT-14 Bristol Channel landing point at Brean. Secondary transatlantic route.",
     "notes": "", "sources": "TeleGeography"},

    {"id": "N05", "name": "Lowestoft cable landing (Suffolk)", "cat": "N", "subcat": "N Sea + Scandinavian cables",
     "tier": "T3", "lat": 52.4750, "lon": 1.7500, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Scandinavian and North Sea cable landings. East Anglia coast.",
     "notes": "", "sources": "TeleGeography"},

    {"id": "N06", "name": "Winterton-on-Sea cable landing (Norfolk)", "cat": "N", "subcat": "N Sea cables",
     "tier": "T3", "lat": 52.7139, "lon": 1.6972, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Pan-European and North Sea cable landings, Norfolk coast.",
     "notes": "", "sources": "TeleGeography"},

    {"id": "N07", "name": "Holyhead cable landing (Anglesey)", "cat": "N", "subcat": "Ireland cables",
     "tier": "T3", "lat": 53.3089, "lon": -4.6333, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Cable landing connecting UK-Ireland. Severs critical cross-Irish Sea links.",
     "notes": "", "sources": "TeleGeography"},

    {"id": "N08", "name": "Scrabster / Thurso cable landing (Caithness)", "cat": "N", "subcat": "Nordic cables",
     "tier": "T3", "lat": 58.6128, "lon": -3.5444, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Far-north cable landings connecting UK-Iceland-Faroes-Scandinavia.",
     "notes": "", "sources": "TeleGeography"},

    {"id": "N09", "name": "Telehouse / LINX Docklands", "cat": "N", "subcat": "UK internet exchange",
     "tier": "T2", "lat": 51.5081, "lon": -0.0080, "yield_kt": 800, "burst": "air", "height_m": 2000,
     "rationale": "LINX (London Internet Exchange) primary site at Telehouse North. UK internet traffic interchange. Covered by London GZ 1.",
     "notes": "Overlap I01/O02.", "sources": "LINX"},

    # =========================================================
    # O  DATA CENTRES & CLOUD INFRASTRUCTURE
    # =========================================================
    {"id": "O01", "name": "Slough data centre cluster", "cat": "O", "subcat": "Hyperscale DC cluster",
     "tier": "T2", "lat": 51.5112, "lon": -0.5950, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Slough Trading Estate: Equinix LD4/LD5/LD6/LD8, Virtus, Digital Realty, Ark. Densest data centre cluster in Europe. AWS, Azure, Google, Oracle European points of presence.",
     "notes": "Partly covered by London GZ 3 (I03).", "sources": "Uptime Institute, DCD"},

    {"id": "O02", "name": "Docklands DC cluster (London)", "cat": "O", "subcat": "Internet exchange + hyperscale",
     "tier": "T2", "lat": 51.5083, "lon": -0.0200, "yield_kt": 800, "burst": "air", "height_m": 2000,
     "rationale": "Telehouse North/East/West, Equinix LD1-3. LINX core. London main internet interconnect.",
     "notes": "Covered by London GZ 1 (I01).", "sources": "Uptime Institute"},

    {"id": "O03", "name": "Farnborough / Fleet DC cluster (Ark Zeta)", "cat": "O", "subcat": "Secure/gov DC",
     "tier": "T2", "lat": 51.2839, "lon": -0.7681, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Ark Data Centres Farnborough Zeta / Leap DC. Major public-sector and defence-adjacent cloud hosting.",
     "notes": "Overlap H12 QinetiQ Farnborough.", "sources": "Ark"},

    {"id": "O04", "name": "Park Royal DC cluster (West London)", "cat": "O", "subcat": "Colocation",
     "tier": "T3", "lat": 51.5269, "lon": -0.2836, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "West London DC cluster: Global Switch Park Royal, Pulsant. London overspill capacity.",
     "notes": "Partly covered by London GZ 3 (I03).", "sources": "DCD"},

    {"id": "O05", "name": "Equinix Manchester MA1+", "cat": "O", "subcat": "N England DC",
     "tier": "T3", "lat": 53.4856, "lon": -2.2944, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Equinix Manchester data centre cluster. Primary cloud on-ramp for NW England.",
     "notes": "Covered by Manchester city strike (I05).", "sources": "Equinix"},

    {"id": "O06", "name": "NGD Newport / Vantage (S Wales)", "cat": "O", "subcat": "Large DC",
     "tier": "T3", "lat": 51.5814, "lon": -3.0081, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Next Generation Data / Vantage Newport. One of Europe's largest single-site data centres. AWS, UK Gov data.",
     "notes": "", "sources": "Vantage"},

    {"id": "O07", "name": "STACK Infrastructure (West Drayton / Hayes)", "cat": "O", "subcat": "Hyperscale DC",
     "tier": "T3", "lat": 51.5100, "lon": -0.4800, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Large west London hyperscale campus. Near Heathrow. Major cloud anchor.",
     "notes": "Partly covered by London GZ 3.", "sources": "STACK"},

    # =========================================================
    # P  CIVIL AVIATION HUBS
    # =========================================================
    {"id": "P01", "name": "London Heathrow (LHR)", "cat": "P", "subcat": "Primary UK hub airport",
     "tier": "T3", "lat": 51.4700, "lon": -0.4543, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "UK's primary international hub. ~80M pax/year. Strategic airlift capability. Jet fuel depot.",
     "notes": "Partly covered by London GZ 3 (I03).", "sources": "Heathrow"},

    {"id": "P02", "name": "London Gatwick (LGW)", "cat": "P", "subcat": "Secondary London hub",
     "tier": "T3", "lat": 51.1537, "lon": -0.1821, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "2nd London airport. ~45M pax. Backup international routing.",
     "notes": "", "sources": "Gatwick"},

    {"id": "P03", "name": "East Midlands Airport (EMA)", "cat": "P", "subcat": "DHL/UPS cargo hub",
     "tier": "T3", "lat": 52.8311, "lon": -1.3281, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "UK's largest pure-cargo airport (DHL, UPS, Royal Mail). Strategic logistics vulnerability.",
     "notes": "", "sources": "EMA"},

    {"id": "P04", "name": "Manchester Airport (MAN)", "cat": "P", "subcat": "N England hub",
     "tier": "T3", "lat": 53.3537, "lon": -2.2750, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Primary airport for N England and Scotland. ~28M pax. Adjacent to Manchester.",
     "notes": "Covered by Manchester city strike (I05).", "sources": "MAG"},

    {"id": "P05", "name": "Prestwick Airport (PIK)", "cat": "P", "subcat": "NATO diversion + USAF transit",
     "tier": "T3", "lat": 55.5094, "lon": -4.5867, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "NATO designated diversion airfield. USAF transatlantic transit hub. Historically: Cold War strategic use.",
     "notes": "", "sources": "Prestwick Airport"},

    {"id": "P06", "name": "Edinburgh Airport (EDI)", "cat": "P", "subcat": "Scotland hub",
     "tier": "T3", "lat": 55.9500, "lon": -3.3725, "yield_kt": 300, "burst": "air", "height_m": 2000,
     "rationale": "Busiest Scottish airport. Adjacent to Edinburgh city.",
     "notes": "Covered by Edinburgh city strike (I12).", "sources": "Edinburgh Airport"},

    {"id": "P07", "name": "Belfast International / Aldergrove (BFS)", "cat": "P", "subcat": "NI airport + military",
     "tier": "T3", "lat": 54.6575, "lon": -6.2158, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Belfast International. Former RAF Aldergrove, 5 Regiment Army Air Corps present. Military-civil dual use.",
     "notes": "", "sources": "Belfast Airport"},

    {"id": "P08", "name": "London Stansted (STN)", "cat": "P", "subcat": "London NE airport + cargo",
     "tier": "T3", "lat": 51.8850, "lon": 0.2350, "yield_kt": 100, "burst": "air", "height_m": 500,
     "rationale": "Low-cost hub and freight. Amazon Air UK hub.",
     "notes": "", "sources": "Stansted"},
]

# ---------------------------------------------------------------------------
# CATEGORY METADATA
# ---------------------------------------------------------------------------

CATEGORIES = {
    "A": "Strategic nuclear forces & warhead infrastructure",
    "B": "US forces in the UK",
    "C": "Strategic command, government continuity, intelligence",
    "D": "RAF main operating bases",
    "E": "Royal Navy bases & fleet support",
    "F": "Army garrisons & training areas",
    "G": "Air defence, radar, SIGINT, early warning",
    "H": "Defence industry & shipbuilding",
    "I": "Population centres (counter-value)",
    "J": "Ports & maritime logistics",
    "K": "Energy — nuclear",
    "L": "Energy — oil, gas & LNG",
    "M": "Electricity transmission & generation",
    "N": "Telecoms, undersea cables & satellite ground stations",
    "O": "Data centres & cloud infrastructure",
    "P": "Civil aviation hubs",
}

CATEGORY_DOCTRINE = {
    "A": "Counterforce priority. Decapitates the UK deterrent at its industrial and basing chokepoints. T1 only.",
    "B": "All US strategic assets in the UK — nuclear, intelligence, command. T1/T2 only.",
    "C": "Decapitation of UK political-military command and intelligence apparatus.",
    "D": "Destruction of UK air combat capability, transport, and training pipeline.",
    "E": "Destruction of Royal Navy surface and sub-surface basing, support and training.",
    "F": "Destruction of UK land forces garrisons and operational readiness.",
    "G": "Blind the UK/US air and signals intelligence picture. Many overlap with B.",
    "H": "Destruction of the UK defence industrial base — long-term attrition of reconstitution. Includes unique capability chokepoints (Barrow, Raynesway).",
    "I": "Counter-value: population, infrastructure, political will. Tiered by population size and strategic weight.",
    "J": "Maritime logistics — severing imports of food, fuel and materiel.",
    "K": "Nuclear power and reprocessing. Sellafield is arguably a strategic target in its own right due to Pu inventory.",
    "L": "Energy supply. Oil refineries, gas terminals and LNG — destroying these collapses transport and heating.",
    "M": "Electricity grid — cascading failure and prolonged blackout.",
    "N": "Communications and internet — international isolation.",
    "O": "Digital infrastructure — cloud, financial systems, government IT.",
    "P": "Aviation hubs — strategic airlift, civil logistics, post-strike movement.",
}

TIER_LABELS = {"T1": "T1", "T2": "T2", "T3": "T3"}

# ---------------------------------------------------------------------------
# PRIORITY ORDER — strategic value ranking for warhead-budget modelling
# Position in list = priority (1 = highest). Filter priority <= N for N warheads.
# ---------------------------------------------------------------------------
PRIORITY_ORDER = [
    # 1-10: Anti-nuclear forces (T1 counterforce)
    "A03",  # Faslane — SSBNs in port, the deterrent itself
    "A04",  # Coulport — warhead storage
    "A01",  # AWE Aldermaston — warhead design
    "A02",  # AWE Burghfield — warhead assembly
    "A05",  # Devonport — SSN refit
    "A06",  # Barrow — submarine construction
    "A07",  # Raynesway — reactor cores
    "B01",  # Lakenheath — B61-12 in WS3 vaults
    "B05",  # Fylingdales — BMEWS early warning

    # 10-17: Critical C2 and intelligence
    "B04",  # Menwith Hill — SIGINT (not directly nuclear forces)
    "C02",  # Northwood — PJHQ (commands all UK joint ops)
    "C06",  # GCHQ Cheltenham — SIGINT HQ
    "C03",  # High Wycombe — Air Command
    "C01",  # PINDAR — in London, highly escalatory
    "C09",  # Credenhill — SAS / UKSF HQ
    "C07",  # MI5 Thames House
    "C08",  # MI6 Vauxhall Cross

    # 18-20: Irreplaceable infrastructure chokepoints
    "K01",  # Sellafield — 140t plutonium, radiological weapon
    "L06",  # St Fergus — 40% of UK gas
    "N01",  # Widemouth Bay — transatlantic fibre

    # 21-27: Primary strike bases
    "E01",  # HMNB Portsmouth — carrier home port
    "D01",  # Coningsby — Typhoon QRA South
    "D02",  # Lossiemouth — Typhoon QRA North
    "D03",  # Marham — F-35B
    "D04",  # Waddington — ISTAR / Reaper
    "D05",  # Brize Norton — strategic airlift
    "D06",  # Odiham — Chinook / SOF support

    # 28-34: Remaining US bases
    "B02",  # Mildenhall — tankers + AFSOC
    "B03",  # Croughton — USAF comms relay
    "B06",  # Welford — conventional munitions depot
    "B10",  # Fairford — bomber forward operating location
    "B07",  # Alconbury — USAF intelligence
    "B08",  # Molesworth — Joint Analysis Center
    "B09",  # Feltwell — space/relay

    # 35-39: Key defence industry
    "H01",  # BAE Warton — Typhoon / F-35 rear fuselage
    "H02",  # BAE Samlesbury — F-35 fuselage
    "H03",  # BAE Scotstoun — Type 26 frigates
    "H04",  # BAE Govan — Type 31 frigates
    "H06",  # MBDA Stevenage — Storm Shadow / ASRAAM

    # 40-44: Secondary C2 + intelligence
    "C04",  # Army HQ Andover
    "C05",  # Navy Command Portsmouth
    "C10",  # RM Poole — SBS HQ
    "G07",  # GCHQ Bude / Morwenstow
    "G08",  # GCHQ Scarborough

    # 45-52: Remaining naval
    "E02",  # RNAS Yeovilton
    "E03",  # RNAS Culdrose
    "E04",  # HMS Collingwood
    "E06",  # RNAD Gosport — munitions
    "E07",  # DM Glen Douglas — NATO munitions
    "E08",  # Babcock Rosyth — carrier refit
    "E05",  # HMS Raleigh
    "E09",  # BUTEC Kyle of Lochalsh

    # 53-60: Remaining RAF
    "D07",  # Benson — Puma
    "D08",  # Wittering — logistics hub
    "D09",  # Northolt — VIP / London mil aviation
    "D10",  # Leeming
    "D11",  # Valley — fast jet training
    "D12",  # Cranwell — officer training
    "D13",  # Shawbury — helicopter training
    "D14",  # Boulmer — air surveillance

    # 61-68: Army garrisons
    "F01",  # Catterick
    "F02",  # Aldershot
    "F03",  # Tidworth / Bulford / Salisbury Plain
    "F04",  # Colchester — 16 AAB
    "F05",  # Edinburgh garrison
    "F06",  # Sandhurst
    "F07",  # Pirbright
    "F08",  # Lisburn Thiepval — NI

    # 69-73: Radar / air defence
    "G01",  # Saxa Vord
    "G02",  # Benbecula
    "G03",  # Buchan
    "G04",  # Brizlee Wood
    "G05",  # Staxton Wold

    # 74-79: Key energy infrastructure
    "L01",  # Fawley refinery
    "L02",  # Stanlow refinery
    "L03",  # Grangemouth refinery
    "L09",  # South Hook LNG
    "L10",  # Isle of Grain LNG
    "M01",  # Drax — ~6% UK generation

    # 80-85: Nuclear power stations (operational)
    "K02",  # Capenhurst — enrichment
    "K03",  # Hinkley Point C
    "K04",  # Sizewell B+C
    "K05",  # Heysham 1+2
    "K06",  # Hartlepool
    "K07",  # Torness

    # 86-91: Remaining energy
    "L04",  # Pembroke refinery
    "L05",  # Lindsey refinery
    "L07",  # Bacton gas terminal
    "L08",  # Easington gas terminal
    "M04",  # Sellindge HVDC interconnector
    "M07",  # National Grid ESO control centre

    # 92-100: Ports + data centres + telecoms
    "J01",  # Felixstowe
    "J02",  # London Gateway
    "J04",  # Liverpool docks
    "J05",  # Immingham
    "O01",  # Slough DC cluster
    "O02",  # Docklands DC cluster
    "N09",  # Telehouse / LINX
    "N02",  # Oxwich Bay cables
    "N03",  # Goonhilly

    # 101-110: Remaining defence industry + testing
    "H10",  # QinetiQ Boscombe Down
    "H11",  # DSTL Porton Down
    "H05",  # Thales Glasgow
    "H07",  # MBDA Lostock
    "H08",  # Leonardo Edinburgh
    "H09",  # Leonardo Luton
    "H12",  # QinetiQ Farnborough
    "H13",  # QinetiQ Portsdown
    "H14",  # QinetiQ Aberporth
    "H15",  # Rolls-Royce Sinfin

    # 111-115: Remaining radar + EW
    "G06",  # Portreath
    "G09",  # Chicksands
    "D15",  # Spadeadam — EW range

    # 116-120: Remaining ports
    "J06",  # Dover
    "J07",  # Milford Haven
    "J03",  # Tilbury
    "J08",  # Grimsby
    "J09",  # Belfast Harbour

    # 121-125: Remaining grid + energy
    "M02",  # Dinorwig pumped storage
    "M03",  # Cruachan pumped storage
    "M05",  # Richborough Nemo Link
    "M06",  # Bicker Fen Viking Link
    "M08",  # Iron Acton 400kV

    # 126-135: Remaining telecoms + data centres + misc infra
    "O03",  # Farnborough DC
    "N04",  # Highbridge / Brean
    "N05",  # Lowestoft cables
    "N06",  # Winterton-on-Sea cables
    "N07",  # Holyhead cables
    "N08",  # Scrabster cables
    "O04",  # Park Royal DC
    "O05",  # Manchester DC
    "O06",  # Newport DC
    "O07",  # STACK West Drayton DC

    # 136-140: Remaining energy + decom nuclear + ports
    "L11",  # Dragon LNG
    "L12",  # Sullom Voe
    "L13",  # Flotta
    "K08",  # Dungeness (decom)
    "K09",  # Bradwell (decom)

    # 141-145: Remaining decom nuclear + grid + misc
    "K10",  # Trawsfynydd
    "K11",  # Chapelcross
    "K12",  # Dounreay
    "M09",  # Wylfa
    "J10",  # Greenock / Clydeport

    # 146-148: Devolved governments
    "C11",  # Holyrood
    "C12",  # Senedd
    "C13",  # Stormont

    # 149-187: Cities by strategic weight / population
    "I01",  # London — City / East
    "I02",  # London — Westminster
    "I03",  # London — West / Slough
    "I04",  # Birmingham
    "I05",  # Manchester
    "I06",  # Glasgow
    "I07",  # Liverpool
    "I08",  # Leeds
    "I09",  # Sheffield
    "I10",  # Bristol
    "I11",  # Newcastle
    "I12",  # Edinburgh
    "I13",  # Cardiff
    "I14",  # Belfast
    "I15",  # Nottingham
    "I16",  # Southampton
    "I17",  # Portsmouth
    "I18",  # Plymouth
    "I19",  # Leicester
    "I20",  # Coventry
    "I21",  # Stoke-on-Trent
    "I22",  # Wolverhampton
    "I23",  # Derby
    "I24",  # Reading
    "I25",  # Milton Keynes
    "I26",  # Cambridge
    "I27",  # Oxford
    "I28",  # Swansea
    "I29",  # Aberdeen
    "I30",  # Dundee
    "I31",  # Hull
    "I32",  # Middlesbrough
    "I33",  # Sunderland
    "I34",  # Preston
    "I35",  # Brighton
    "I36",  # Bournemouth
    "I37",  # Norwich
    "I38",  # York
    "I39",  # Peterborough

    # 188-193: Civil aviation
    "P01",  # Heathrow
    "P02",  # Gatwick
    "P03",  # East Midlands (cargo)
    "P04",  # Manchester
    "P05",  # Prestwick (NATO diversion)
    "P06",  # Edinburgh
    "P07",  # Belfast International
    "P08",  # Stansted
]

# Build priority lookup — assign priority = position in list (1-based)
_priority_lookup = {tid: i + 1 for i, tid in enumerate(PRIORITY_ORDER)}

# Inject priority into each target
for _t in TARGETS:
    _t["priority"] = _priority_lookup.get(_t["id"], 999)

# Sort TARGETS by priority for consistent output
TARGETS.sort(key=lambda x: x["priority"])

CSV_FIELDS = [
    "id", "name", "cat", "subcat", "tier", "priority",
    "lat", "lon", "yield_kt", "burst", "height_m",
    "rationale", "notes", "sources",
]

# ---------------------------------------------------------------------------
# GENERATION FUNCTIONS
# ---------------------------------------------------------------------------

def write_csv():
    out = OUT_DIR / "targets.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(TARGETS)
    print(f"  → {out} ({len(TARGETS)} rows)")


def write_geojson():
    features = []
    for t in TARGETS:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [t["lon"], t["lat"]],
            },
            "properties": {k: t[k] for k in CSV_FIELDS if k not in ("lat", "lon")},
        })
    fc = {"type": "FeatureCollection", "features": features}
    out = OUT_DIR / "targets.geojson"
    out.write_text(json.dumps(fc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → {out} ({len(features)} features)")


def write_markdown():
    lines = []
    lines.append("# Square Leg 2 — Target List\n")
    lines.append(
        "> Auto-generated from `generate.py`. "
        "To add or edit targets, update the `TARGETS` list in that file and re-run.\n"
    )

    # Tier summary table
    tier_counts = {t: sum(1 for x in TARGETS if x["tier"] == t) for t in ["T1", "T2", "T3"]}
    t1 = tier_counts["T1"]
    t2 = tier_counts["T2"]
    t3 = tier_counts["T3"]
    lines.append("## Attack size quick-reference\n")
    lines.append("| Tier | Targets in tier | Cumulative | Scenario |")
    lines.append("|------|----------------|------------|---------|")
    lines.append(f"| **T1** | {t1} | {t1} | Counterforce + decapitation only |")
    lines.append(f"| **T2** | {t2} | {t1+t2} | Full military + major cities + top infrastructure |")
    lines.append(f"| **T3** | {t3} | {t1+t2+t3} | All-out: secondary cities, full infrastructure |")
    lines.append("")

    # Per-category sections
    for cat_id, cat_name in CATEGORIES.items():
        cat_targets = [t for t in TARGETS if t["cat"] == cat_id]
        if not cat_targets:
            continue
        lines.append(f"---\n\n## {cat_id}. {cat_name}\n")
        lines.append(f"*{CATEGORY_DOCTRINE[cat_id]}*\n")

        header = "| # | ID | Target | Tier | Lat | Lon | Yield (kt) | Burst | Rationale |"
        sep    = "|---|-----|--------|------|-----|-----|-----------|-------|-----------|"
        lines.append(header)
        lines.append(sep)
        for t in sorted(cat_targets, key=lambda x: x["priority"]):
            tier_badge = f"**{t['tier']}**"
            rationale = t["rationale"].replace("|", "/")
            lines.append(
                f"| {t['priority']} | {t['id']} | {t['name']} | {tier_badge} | "
                f"{t['lat']:.4f} | {t['lon']:.4f} | "
                f"{t['yield_kt']} | {t['burst']} | {rationale} |"
            )
        lines.append("")

    out = OUT_DIR / "targets.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def write_json():
    """JSON export for the web app."""
    data = {
        "targets": [{k: t[k] for k in CSV_FIELDS} for t in TARGETS],
        "categories": CATEGORIES,
        "category_doctrine": CATEGORY_DOCTRINE,
    }
    out = OUT_DIR / "targets.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → {out} ({len(TARGETS)} targets)")


def write_nukemap():
    """NUKEMAP batch CSV format.

    Columns: yieldKt,latitude,longitude,heightOfBurstFt,showFallout,
             falloutWindSpeed,falloutWindDirection,fissionFraction

    - heightOfBurstFt: metres → feet.  Ground burst → 0.
    - showFallout: 1 for ground burst, 0 for air burst.
    - falloutWindSpeed: default 15 mph (prevailing UK average).
    - falloutWindDirection: default 225° (SW — prevailing UK wind).
    - fissionFraction: 50% for thermonuclear weapons (standard assumption).
    """
    M_TO_FT = 3.28084
    out = OUT_DIR / "targets_nukemap.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        f.write("yieldKt,latitude,longitude,heightOfBurstFt,"
                "showFallout,falloutWindSpeed,falloutWindDirection,"
                "fissionFraction\n")
        for t in TARGETS:
            height_ft = round(float(t["height_m"]) * M_TO_FT)
            show_fallout = 1 if t["burst"] == "ground" else 0
            f.write(f"{t['yield_kt']},{t['lat']},{t['lon']},"
                    f"{height_ft},{show_fallout},15,225,50\n")
    print(f"  → {out} ({len(TARGETS)} rows)")


if __name__ == "__main__":
    print("Square Leg 2 — generating outputs...")
    write_csv()
    write_geojson()
    write_markdown()
    write_nukemap()
    write_json()

    # Quick stats
    cats = sorted(CATEGORIES.keys())
    print(f"\nTotal targets: {len(TARGETS)}")
    for tier in ["T1", "T2", "T3"]:
        n = sum(1 for t in TARGETS if t["tier"] == tier)
        cum = sum(1 for t in TARGETS if t["tier"] <= tier)
        print(f"  {tier}: {n} in tier, {cum} cumulative")
    print(f"\nBy category:")
    for c in cats:
        n = sum(1 for t in TARGETS if t["cat"] == c)
        tiers = [t["tier"] for t in TARGETS if t["cat"] == c]
        tier_str = ", ".join(f"{tr}:{tiers.count(tr)}" for tr in ["T1","T2","T3"] if tiers.count(tr))
        print(f"  {c} {CATEGORIES[c][:40]:40s}  {n:3d}  [{tier_str}]")
    print("\nDone.")
