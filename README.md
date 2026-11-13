# Flat-Six Sound – engine synthesizer for the Tesla in-car browser

A web app that synthesizes, in real time, the sound of a flat-six engine **inspired by** the Porsche 911 and plays it through the car's cabin speakers.
It has no sound files, external libraries, CDNs or web fonts. Everything is generated with the Web Audio API.

> Not affiliated with, endorsed or sponsored by Porsche AG or Tesla, Inc. Names are used descriptively only ("inspired by").

## Files
| File | What it is |
|---|---|
| `index.html` | The full app (inline CSS and JS); registers the service worker when served over http(s) |
| `sw.js` | Service worker that caches every file for offline use after the first online visit |
| `manifest.json`, `icon.svg`, `icon-192.png`, `icon-512.png` | Web app manifest and icons |
| `porsche-sound-standalone.html` | Single-file build with no service worker or extra files (also works opened locally) |
| `build_standalone.py` | Rebuilds the standalone file from `index.html` |
| `preview.png`, `preview-drive.png` | 1920x1200 screenshots (GPS off with action buttons, and Follow-speed mode at ~114 km/h) |
| `tesla-mockup.png` | Illustrative mockup of the app inside a Tesla-style browser (not a real Tesla screenshot) |
| `preview.wav` | Offline-rendered demo (GT3, Turbo S, classic) |

## Loading it in a Tesla
The Tesla browser **cannot open local files or HTML from a USB drive**, so the folder must be hosted on an HTTPS URL.

1. Upload the folder to a free static host:
   - **Netlify Drop**: drag the folder onto app.netlify.com/drop and you get a URL.
   - **GitHub Pages**: create a repository, push the files, enable Pages in the settings.
   - **Cloudflare Pages**: use Direct Upload with the folder.
2. In the car, **in Park**, open the browser and go to the URL **once while online**, so the service worker caches the app.
3. Press the round **ENGINE START** button. That touch also enables audio (browsers only allow sound after a tap).
4. Allow location access when the browser asks, so the engine can follow your speed.
5. Bookmark the URL in the browser.

### Notes on GPS
- The Tesla browser supports location on recent software versions and asks for permission the first time; if it was refused, re-allow location for the site in the browser settings.
- GPS updates about once per second, so the sound lags real speed changes by roughly 0.5–1.5 s (the app extrapolates between fixes to hide steps). In tunnels or parking garages the signal drops and the engine falls back to idle (action buttons still work).

### Important notes
- The Tesla browser generally plays audio in Park. Some software versions also play it while driving, but this varies.
- Offline caching in the Tesla browser **may be unreliable**: the car can clear the cache after a software update or reboot. If the page doesn't load offline, open it again while online.
- Audio plays through the car's cabin speakers; web pages can't reach the external pedestrian-warning speaker.
- You can open `porsche-sound-standalone.html` on a computer (even as a local file) to try the sound before uploading.

## Using it
- **Character**: GT3 4.0 naturally aspirated (9,000 rpm redline), Turbo S twin-turbo (turbo whistle and blow-off valve), classic air-cooled 911 (cooling-fan whine, rasp and pops).
- **ENGINE START / STOP**: big round button – starter crank, catch and settle to idle; press again for shutdown.
- **Drive mode: Follow speed (GPS)** (on by default): the app reads your speed with `navigator.geolocation.watchPosition` (high accuracy; uses `coords.speed`, or computes speed from successive positions when it's missing), smooths it, and maps it to rpm through a simulated 7-speed PDK with per-preset ratios. Hard acceleration upshifts around 6,000–6,500 rpm, gentle cruising shifts early, slowing down downshifts (with rev-match blips) and stopping returns to idle. Accelerating adds load (more intake/exhaust and boost); coasting gives overrun crackle. The speedometer shows the GPS speed and the tach shows the gear (D1–D7). Status shows "Waiting for GPS…", "Location denied - idle", "GPS unavailable - idle", "GPS signal lost - idle" or "GPS off - idle"; without GPS the engine idles and the action buttons still work.
- **Debug drive**: add `?sim=1` to the URL to fake a 0 → 120 → 0 km/h drive.
- **Buttons**: Idle, Rev blip, Rev to redline (into the limiter), Launch & upshifts, Downshift with blip, Overrun pops.
- **Cluster**: center tachometer with shift lights, speedometer, and a boost gauge (Turbo) or oil temperature (other presets).

## How the sound is made
- The firing frequency of a 4-stroke flat-six is rpm/60×3. The base oscillator is one full engine cycle (rpm/120) with a harmonic stack where the 6th harmonic is the firing frequency. Half-order, crank-order and bank-to-bank harmonics give the uneven flat-six character, plus a per-cycle amplitude lope.
- Low-frequency random modulation adds small cycle-to-cycle pitch and level variation.
- Exhaust: soft-clip waveshaper and resonant bandpass filters (one tracks rpm), split into left/right "tailpipes" with a slight path difference, plus a short synthetic cabin reflection (generated impulse response).
- Intake: filtered noise that rises with throttle, modulated by the firing pulses, plus a high-harmonic induction howl with a resonance-flap boost above ~5,600 rpm on the GT3 preset.
- Turbo: whistle that rises with boost, air hiss, and a fluttering blow-off on lift.
- Pops: short random noise bursts on lift-off, on upshifts and on the limiter. Subtle gearbox whine in gear.
- Physics: rpm-dependent torque, friction, gear-dependent inertia, rev limiter, idle control, turbo lag.

## ⚠️ Use responsibly
Cabin only. Don't operate or look at the app while driving – use it parked, or let a passenger run it.
Keep the volume reasonable, never mask the car's own warning sounds, and be considerate of people around you.
