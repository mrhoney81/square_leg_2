# How It Works — Square Leg 2

A guide to the project structure, how to edit things, and how to deploy.

---

## Architecture

```
squareleg2/
  generate.py            <-- Canonical data source. Edit targets HERE.
  targets.csv            <-- Auto-generated. Don't edit directly.
  targets.json           <-- Auto-generated. Feeds the web app.
  targets.geojson        <-- Auto-generated. For QGIS / mapping tools.
  targets.md             <-- Auto-generated. Human-readable table.
  targets_nukemap.csv    <-- Auto-generated. NUKEMAP batch import.
  nuke_icon.png          <-- Favicon for the web app.
  square_leg.jpg         <-- Original 1980 "Soviet hit list" map (reference).
  README.md              <-- GitHub front page.
  HOW_IT_WORKS.md        <-- This file.
  web/
    index.html           <-- Interactive warhead budget planner (single file).
```

**One-way data flow:** `generate.py` is the single source of truth. All other data files are derived from it. Never edit `targets.csv`, `targets.json`, etc. directly — your changes will be overwritten on the next run.

---

## Regenerating outputs

After editing `generate.py`:

```bash
python3 generate.py
```

This regenerates all six output files. No dependencies beyond Python 3 standard library.

---

## Editing targets

All target data lives in the `TARGETS` list in `generate.py` (starts around line 27). Each target is a Python dict:

```python
{"id": "A03", "name": "HMNB Clyde (Faslane)", "cat": "A", "subcat": "SSBN operating base",
 "tier": "T1", "lat": 56.0669, "lon": -4.8267, "yield_kt": 475, "burst": "air", "height_m": 500,
 "rationale": "Sole Royal Navy SSBN and SSN operating base.",
 "notes": "Also cat E (naval base).", "sources": "RN"},
```

| Field | What it does |
|-------|-------------|
| `id` | Unique identifier. Format: category letter + two-digit number (e.g. `A03`, `K01`). |
| `name` | Display name. |
| `cat` | Category letter (A-P). Must match a key in `CATEGORIES` dict. |
| `subcat` | Short subcategory label. |
| `tier` | `T1`, `T2`, or `T3`. Controls which tier the target appears in. |
| `lat`, `lon` | WGS84 coordinates, 4 decimal places. |
| `yield_kt` | Warhead yield in kilotons. |
| `burst` | `ground` or `air`. |
| `height_m` | Burst height in metres (0 for ground burst). |
| `rationale` | Why this target matters. Shows in the web app and markdown table. |
| `notes` | Cross-references, overlaps, etc. |
| `sources` | Attribution. |

**To add a target:** add a new dict to the `TARGETS` list in the appropriate category section, then add its ID to the `PRIORITY_ORDER` list at the desired position.

**To remove a target:** delete the dict and remove the ID from `PRIORITY_ORDER`. Renumber remaining IDs in the category if needed.

**To change a target's priority:** move its ID to a different position in `PRIORITY_ORDER`.

---

## Editing the priority order

The `PRIORITY_ORDER` list in `generate.py` (after the `TARGETS` list) defines the strategic value ranking. Position in the list = priority number (1 = highest). The web app's warhead budget slider uses this to determine which targets are struck first.

The list is grouped with comments:

```python
PRIORITY_ORDER = [
    # 1-9: Anti-nuclear forces (T1 counterforce)
    "A03",  # Faslane — SSBNs in port
    "A04",  # Coulport — warhead storage
    ...
    # 10-17: Critical C2 and intelligence
    "B04",  # Menwith Hill — SIGINT
    ...
]
```

Every target ID must appear exactly once. After editing, run `generate.py` — it will error if any ID is missing or duplicated.

---

## Editing the web app

The entire web app is a single file: `web/index.html`. No build step, no dependencies beyond two CDN scripts (Leaflet for the map, CARTO for map tiles).

### Changing the page title

Edit this line near the top of `web/index.html`:

```html
<title>Square Leg 2 — Warhead Budget Planner</title>
```

And the visible heading in the `<header>` section:

```html
<h1>Square Leg 2 — Warhead Budget Planner</h1>
```

### Changing the description / blurb

Edit the `<p>` tag immediately after the `<h1>` in the `<header>` section:

```html
<p>Allocate a warhead budget and generate a prioritised target list. Targets ranked by strategic value.
   Russia has ~1,500 deployed strategic warheads total (New START); realistic UK allocation is 30-80.</p>
```

### Changing preset buttons

The preset buttons are in the `.presets` div:

```html
<button data-n="9" data-t1only="true">Nuclear counterforce (9)</button>
<button data-n="20">Counterforce + C2 (20)</button>
...
```

- `data-n` sets the warhead budget when clicked.
- `data-t1only="true"` (optional) locks to T1-only targets regardless of budget.
- The button text is just a label — change it to whatever you like.

### Changing the population filter settlements

The `UK_SETTLEMENTS` array in the JavaScript contains ~88 UK towns/cities with coordinates and populations. To add a settlement, add an entry:

```javascript
{n:'Townname', lat:51.234, lon:-1.234, pop:50000},
```

### Changing the favicon

Replace `nuke_icon.png` in the project root. The HTML references it as `../nuke_icon.png`.

---

## Deploying to GitHub Pages

1. Push the entire repo to GitHub.
2. Go to **Settings → Pages**.
3. Set source to **Deploy from a branch**, branch `main`, folder `/ (root)`.
4. The planner will be live at `https://username.github.io/reponame/web/`

The web app fetches `../targets.json` relative to its own location, so the file structure must stay as-is. If you rename or move files, update the `fetch()` path in `web/index.html`.

### Important: the web app needs targets.json

The web app loads data from `targets.json` at runtime via `fetch()`. This file must exist and be accessible from the web server. Always run `python3 generate.py` before deploying to ensure it's up to date.

---

## Data formats

### targets.csv

Standard CSV, one row per target, sorted by priority. Fields:

```
id, name, cat, subcat, tier, priority, lat, lon, yield_kt, burst, height_m, rationale, notes, sources
```

### targets.json

JSON object with three keys:

```json
{
  "targets": [ ... ],         // Array of target objects (same fields as CSV)
  "categories": { "A": "Strategic nuclear forces...", ... },
  "category_doctrine": { "A": "Counterforce priority...", ... }
}
```

### targets_nukemap.csv

NUKEMAP batch import format:

```
yieldKt,latitude,longitude,heightOfBurstFt,showFallout,falloutWindSpeed,falloutWindDirection,fissionFraction
```

- Heights converted to feet. Ground burst = 0 ft.
- `showFallout`: 1 for ground burst, 0 for air burst.
- Wind: 15 mph from 225° (UK prevailing SW wind).
- Fission fraction: 50% (thermonuclear standard).

### targets.geojson

Standard GeoJSON FeatureCollection. Each feature is a Point with all CSV fields as properties. Drag into QGIS, geojson.io, or any GIS tool.

### KML (from web app)

The web app generates KML files on demand (Download KML button). Targets are styled by category colour. Opens in Google Earth, Google Maps, QGIS, etc.

---

## Overpressure model (population filter)

The web app's "Avoid population centres" filter uses Glasstone & Dolan cube-root scaling to compute overpressure radii:

```
radius_km = R_1kt × yield_kt^(1/3)
```

Where `R_1kt` is the radius at 1 kt for the selected overpressure level:

| Level | R_1kt (km) | Meaning |
|-------|-----------|---------|
| 5 psi | 0.71 | Severe structural damage, high fatalities |
| 3 psi | 0.96 | Moderate damage, significant casualties |
| 1 psi | 1.91 | Light damage, window breakage |

Ground bursts use 80% of the airburst radius (more energy goes into ground shock).

For each target, the filter checks whether any UK settlement above the population threshold falls within this radius. If so, the target is excluded and replaced by the next-priority non-excluded target.
