#!/usr/bin/env python3
"""Configure the existing launcher, leaving all unrelated preferences unchanged."""
import json
import os
from pathlib import Path
URL = "https://raw.githubusercontent.com/BenExter/Truchosafio4-Modpack/main/manifest.json"
appdata = Path(os.getenv('APPDATA') or (Path.home() / 'AppData' / 'Roaming'))
file = appdata / '.truchosafio4' / 'launcher.json'
file.parent.mkdir(parents=True, exist_ok=True)
if file.is_file():
    obj = json.loads(file.read_text(encoding='utf-8-sig'))
    if not isinstance(obj, dict):
        raise RuntimeError('La configuracion actual no es un objeto JSON. No se modifico.')
else:
    obj = {'nickname': 'Jugador', 'memoryGb': 6}
old = obj.get('manifestUrl')
obj['manifestUrl'] = URL
backup = file.with_suffix('.json.backup')
if file.is_file():
    backup.write_bytes(file.read_bytes())
file.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('URL de GitHub configurada:', URL)
print('Configuracion:', file)
if old and old != URL:
    print('URL anterior:', old)
if backup.exists():
    print('Copia de seguridad:', backup)
