#!/usr/bin/env python3
"""Builds porsche-sound-standalone.html: same app, no manifest / service worker, icon inlined."""
import re, base64, pathlib
d = pathlib.Path(__file__).parent
html = (d / 'index.html').read_text(encoding='utf-8')
icon = base64.b64encode((d / 'icon.svg').read_bytes()).decode()
html = re.sub(r'<!--PWA-START-->.*?<!--PWA-END-->',
              f'<link rel="icon" href="data:image/svg+xml;base64,{icon}">', html, flags=re.S)
html = re.sub(r'/\*PWA-START\*/.*?/\*PWA-END\*/', '/* standalone build: no service worker */', html, flags=re.S)
(d / 'porsche-sound-standalone.html').write_text(html, encoding='utf-8')
print('wrote porsche-sound-standalone.html', len(html), 'bytes')
