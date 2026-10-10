# travisroth.dev

Personal portfolio site. Static HTML generated from Jinja templates and
hosted as a free Render static site at https://travisroth.dev.

## How it works

- `templates/` – pages, all extending `base.html` (nav, analytics tags).
- `static/` – CSS, scripts, images, PDFs; copied to `dist/static/` as is.
- `build.py` – renders each page in `PAGES` to `dist/<path>/index.html`, so
  the old Flask URLs (`/projects`, `/weather_home`, ...) still work.
- The weather page is the only dynamic feature. `static/scripts/weather.js`
  reads `?city=` from the URL and calls `https://kiln-api.travisroth.dev/weather`,
  a small endpoint on the shared projects API (repo `kiln_monitor`) that holds
  the OpenWeatherMap key.

The previous Flask server, its Google Analytics dashboard (which had no
template and was unreachable) and the 118-line frozen requirements file were
removed in October 2026; every deploy had failed since 2024.

## Build locally

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python3 build.py
python3 -m http.server 8787 --directory dist
```

## Deploy

Render static site, branch `main`:

- Build command: `pip install -r requirements.txt && python3 build.py`
- Publish directory: `dist`

Pushes to `main` deploy automatically. DNS: `travisroth.dev` ALIAS and
`www` CNAME at Porkbun point at the Render static site.
