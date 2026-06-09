# hue-crazy

Python scripts for controlling Philips Hue lights via the local bridge API.

- **hue.py** — set a light to a named color
- **cycle.py** — slowly cycle a light through a color sequence

## Requirements

Python 3 and the `requests` library:

```
pip install requests
```

## Setup

### 1. Find your bridge IP

Either:
- Hue app → Settings → My Hue System → your bridge → IP address
- Or visit `https://discovery.meethue.com` from any browser — returns JSON with `internalipaddress`

### 2. Get an API key

The bridge exposes a local REST API. To get a key:

1. Open `http://<bridge-ip>/debug/clip.html` in a browser on your local network
2. Set the URL field to `/api`
3. Set the body to `{"devicetype":"hue-crazy#yourname"}`
4. **Press the physical button on top of the bridge**, then click POST within 30 seconds
5. The response will contain a `"username"` value — that is your API key

### 3. Create config.py

Create a `config.py` in the project root (it's already gitignored):

```python
BRIDGE  = "192.168.x.x"    # your bridge IP
API_KEY = "abc123..."       # the username from step 2
```

### 4. Find your light IDs

Open this URL in a browser (or curl it):

```
http://<bridge-ip>/api/<api-key>/lights
```

Returns a JSON object keyed by light ID, with each light's name and state. Use those IDs with the `--light` flag or set `DEFAULT_LIGHT` in `hue.py`.

## Usage

### hue.py — set a color

```
python3 hue.py <color>              # set default light (ID 6)
python3 hue.py <color> <light_id>  # set a specific light
python3 hue.py list                 # show available colors
```

Available colors: `blue`, `green`, `lavender`, `orange`, `pink`, `purple`, `red`, `teal`, `white`, `yellow`

### cycle.py — loop through colors

```
python3 cycle.py                              # cycle all colors, 5s each
python3 cycle.py --secs 10                   # 10 seconds per color
python3 cycle.py --light 3                   # use a different light
python3 cycle.py --colors blue purple white  # custom sequence
python3 cycle.py --once                      # run through once and stop
```

## How the API works

The Hue bridge runs a local HTTP server. All requests go to:

```
http://<bridge-ip>/api/<api-key>/lights/<id>/state
```

Colors are set using CIE xy chromaticity coordinates — a pair of floats that map to a point in the color gamut. The `COLORS` dict in `hue.py` has hand-tuned values for each named color.
