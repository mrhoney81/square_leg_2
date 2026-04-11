# NUKEMAP Multi-Detonation URLs

NUKEMAP supports loading multiple detonation sites via URL query parameters using array-indexed notation. This is undocumented — the FAQ says only single detonations are supported — but it works.

## URL Format

```
https://nuclearsecrecy.com/nukemap/?kt[0]=100&lat[0]=51.5&lng[0]=-0.12&airburst[0]=1&hob_ft[0]=1640&fallout[0]=0&kt[1]=50&lat[1]=48.8&lng[1]=2.35&airburst[1]=0&hob_ft[1]=0&fallout[1]=1&zm=6
```

Each detonation is indexed `[0]`, `[1]`, `[2]`, etc. The maximum number of detonations is 80.

## Parameters

### Per detonation (indexed)

| Parameter | Description | Example |
|-----------|-------------|---------|
| `kt[i]` | Yield in kilotons | `kt[0]=475` |
| `lat[i]` | Latitude (decimal degrees) | `lat[0]=56.0669` |
| `lng[i]` | Longitude (decimal degrees) | `lng[0]=-4.8267` |
| `hob_ft[i]` | Height of burst in feet. 0 = ground burst. | `hob_ft[0]=1640` |
| `airburst[i]` | 1 = airburst, 0 = ground burst | `airburst[0]=1` |
| `fallout[i]` | 1 = show fallout plume, 0 = no fallout | `fallout[0]=0` |
| `ff[i]` | Fission fraction percentage (0-100). Default 100. | `ff[0]=50` |
| `fallout_wind[i]` | Fallout wind speed in mph. Default 15. | `fallout_wind[0]=20` |
| `fallout_angle[i]` | Fallout wind direction in degrees. Default 225. | `fallout_angle[0]=180` |

### Global (not indexed)

| Parameter | Description |
|-----------|-------------|
| `zm` | Map zoom level (1-18) |

## Bugs and Pitfalls

### 1. Brackets must NOT be percent-encoded

The square brackets in parameter names (e.g. `kt[0]`) must be literal `[` and `]` characters in the URL. NUKEMAP's parser looks for literal brackets — if they are percent-encoded as `%5B` and `%5D`, the parameters will not be parsed as arrays and it will fail.

**This means you cannot use `URLSearchParams` to build the URL**, because it automatically encodes brackets. Build the query string manually via string concatenation instead.

Wrong: `kt%5B0%5D=100` — will not work
Correct: `kt[0]=100` — works

### 2. `zm` is mandatory

If `zm` is missing the page crashes. Always include it. Use 4-6 for country-scale, 8-12 for city-scale.

### 2. You must set every parameter on every detonation

NUKEMAP has a bug where parameter values leak between detonations. If you set `fallout[1]=1` but don't set `fallout[2]`, detonation 2 will inherit `fallout=1` from detonation 1. This applies to all parameters.

**Always explicitly set `kt`, `lat`, `lng`, `hob_ft`, `airburst`, and `fallout` on every single detonation.** Never rely on defaults.

### 3. Do not use `hob_opt`

Including the `hob_opt` parameter can interfere with airburst/ground burst rendering. Just use `airburst` and `hob_ft` to control burst type.

### 4. Do not use the permalink system for multiple detonations

NUKEMAP's permalink system (`?t=HASH`) stores multi-detonation data correctly server-side but has a client-side rendering bug — only the last detonation displays.

## CSV Field Mapping

NUKEMAP's CSV format is: `yieldKt,latitude,longitude,heightOfBurstFt,showFallout,falloutWindSpeed,falloutWindDirection,fissionFraction`

| CSV Field | URL Parameter | Notes |
|-----------|---------------|-------|
| yieldKt | `kt[i]` | |
| latitude | `lat[i]` | |
| longitude | `lng[i]` | |
| heightOfBurstFt | `hob_ft[i]` | |
| showFallout | `fallout[i]` | |
| falloutWindSpeed | `fallout_wind[i]` | Default 15 |
| falloutWindDirection | `fallout_angle[i]` | Default 225 |
| fissionFraction | `ff[i]` | Default 100 |

Derive `airburst[i]` from heightOfBurstFt: if > 0 then 1, if 0 then 0.

## Examples

### Two airbursts

```
https://nuclearsecrecy.com/nukemap/?kt[0]=100&lat[0]=51.5074&lng[0]=-0.1278&hob_ft[0]=1640&airburst[0]=1&fallout[0]=0&kt[1]=50&lat[1]=48.8566&lng[1]=2.3522&hob_ft[1]=1640&airburst[1]=1&fallout[1]=0&zm=5
```

### Mix of airbursts and ground bursts

```
https://nuclearsecrecy.com/nukemap/?kt[0]=475&lat[0]=56.0669&lng[0]=-4.8267&hob_ft[0]=1640&airburst[0]=1&fallout[0]=0&ff[0]=50&kt[1]=475&lat[1]=56.055&lng[1]=-4.8792&hob_ft[1]=0&airburst[1]=0&fallout[1]=1&ff[1]=50&kt[2]=100&lat[2]=51.3683&lng[2]=-1.1394&hob_ft[2]=1640&airburst[2]=1&fallout[2]=0&ff[2]=50&kt[3]=100&lat[3]=51.3989&lng[3]=-1.0544&hob_ft[3]=1640&airburst[3]=1&fallout[3]=0&ff[3]=50&kt[4]=475&lat[4]=50.3833&lng[4]=-4.1833&hob_ft[4]=1640&airburst[4]=1&fallout[4]=0&ff[4]=50&kt[5]=100&lat[5]=54.113&lng[5]=-3.2347&hob_ft[5]=1640&airburst[5]=1&fallout[5]=0&ff[5]=50&kt[6]=100&lat[6]=52.9175&lng[6]=-1.43&hob_ft[6]=1640&airburst[6]=1&fallout[6]=0&ff[6]=50&kt[7]=100&lat[7]=52.4093&lng[7]=0.561&hob_ft[7]=1640&airburst[7]=1&fallout[7]=0&ff[7]=50&kt[8]=475&lat[8]=54.3614&lng[8]=-0.67&hob_ft[8]=0&airburst[8]=0&fallout[8]=1&ff[8]=50&zm=6
```

### JavaScript helper

```javascript
function buildNukemapUrl(detonations, zoom = 6) {
    // Do NOT use URLSearchParams — it percent-encodes brackets which breaks NUKEMAP
    let query = '';
    detonations.forEach((det, i) => {
        query += `&kt[${i}]=${det.kt}`;
        query += `&lat[${i}]=${det.lat}`;
        query += `&lng[${i}]=${det.lng}`;
        query += `&hob_ft[${i}]=${det.hob_ft ?? 0}`;
        query += `&airburst[${i}]=${det.hob_ft > 0 ? 1 : 0}`;
        query += `&fallout[${i}]=${det.fallout ? 1 : 0}`;
        if (det.ff != null) query += `&ff[${i}]=${det.ff}`;
        if (det.fallout) {
            if (det.fallout_wind != null) query += `&fallout_wind[${i}]=${det.fallout_wind}`;
            if (det.fallout_angle != null) query += `&fallout_angle[${i}]=${det.fallout_angle}`;
        }
    });
    query += `&zm=${zoom}`;
    return `https://nuclearsecrecy.com/nukemap/?${query.substring(1)}`;
}
```
