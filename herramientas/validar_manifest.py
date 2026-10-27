#!/usr/bin/env python3
"""Static validation of the JSON schema expected by Truchosafio Launcher beta."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse, unquote

REPO = 'BenExter/Truchosafio4-Modpack'
ALLOWED = {'mods','config','resourcepacks','shaderpacks','defaultconfigs'}


def validate(path):
    m = json.loads(Path(path).read_text(encoding='utf-8'))
    if m.get('schema') != 1 or m.get('minecraft') != '1.21.1' or m.get('loader') != 'fabric':
        raise ValueError('Schema, version de Minecraft o loader incorrectos')
    files = m.get('files')
    if not isinstance(files, list) or len(files) > 400:
        raise ValueError('La lista de archivos debe contener entre 0 y 400 entradas')
    paths, asset_names = set(), set()
    for i, item in enumerate(files):
        if not isinstance(item, dict):
            raise ValueError(f'Entrada {i} no es un objeto JSON')
        path = item.get('path','')
        if not isinstance(path, str) or '\\' in path or ':' in path or '..' in path.split('/'):
            raise ValueError(f'Ruta invalida: {path!r}')
        parts = path.split('/')
        if len(parts) < 2 or any(not x or x in ('.','..') for x in parts) or parts[0] not in ALLOWED:
            raise ValueError(f'Ruta invalida: {path!r}')
        if path.casefold() in paths:
            raise ValueError('Archivo duplicado o colision en Windows: ' + path)
        paths.add(path.casefold())
        hash_value = item.get('sha256','')
        if not isinstance(hash_value,str) or not re.fullmatch(r'[0-9a-f]{64}',hash_value):
            raise ValueError('SHA-256 incorrecto para ' + path)
        uri = urlparse(item.get('url',''))
        if uri.scheme != 'https' or uri.netloc != 'github.com':
            raise ValueError('URL no autorizada en ' + path)
        prefix = '/' + REPO + '/releases/download/'
        if not uri.path.startswith(prefix) or uri.query or uri.fragment:
            raise ValueError('URL de Release incorrecta: ' + uri.geturl())
        asset_name = unquote(uri.path.rsplit('/',1)[-1])
        if asset_name in asset_names:
            raise ValueError('Nombre de asset duplicado: ' + asset_name)
        asset_names.add(asset_name)
    print(f'OK: esquema 1, Minecraft 1.21.1, Fabric, {len(files)} archivos validados')
    return m

if __name__ == '__main__':
    import sys
    validate(sys.argv[1] if len(sys.argv)>1 else 'manifest.json')
