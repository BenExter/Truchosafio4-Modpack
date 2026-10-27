#!/usr/bin/env python3
"""One-click, checksum-verified publisher for the Truchosafio4 launcher.

Publishes all source files as one GitHub Release and updates manifest.json LAST.
Compatible with the launcher schema 1. No third-party dependencies.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
from urllib.parse import quote

from validar_manifest import validate

REPO = 'BenExter/Truchosafio4-Modpack'
ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'publish'
DIST = ROOT / 'dist'
FOLDERS = {'mods', 'config', 'defaultconfigs', 'shaderpacks', 'resourcepacks'}
MAX_FILES = 400
# Conservative safety limit per GitHub release asset; no large files go into git.
MAX_ASSET_SIZE = 2_000_000_000
SECRET_WORDS = {'access_token', 'secret_key', '.env', 'auth.json', 'accounts.json', 'ops.json', 'whitelist.json', 'banned-players.json', 'usercache.json'}


def fail(message):
    raise RuntimeError(message)


def run(*args, capture=True):
    p = subprocess.run(args, cwd=ROOT, text=True, encoding='utf-8',
                       stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.PIPE if capture else None,
                       check=False)
    if p.returncode:
        fail(f'Error {p.returncode} al ejecutar {args[0]} {" ".join(map(str,args[1:]))}:\n{p.stderr or ""}')
    return (p.stdout or '').strip()


def checksum(file):
    with file.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def prepare(tag):
    if not INPUT.exists():
        fail('No existe la carpeta publish/. Crea publish/mods y agrega los archivos del modpack.')
    staged = DIST / 'assets'
    if DIST.exists():
        shutil.rmtree(DIST)
    staged.mkdir(parents=True)
    specs = []
    seen_windows, seen_assets = set(), set()
    for file in sorted(INPUT.rglob('*'), key=lambda p: str(p).casefold()):
        if file.is_symlink():
            fail('No se permiten enlaces simbolicos: ' + str(file))
        if not file.is_file():
            continue
        rel = file.relative_to(INPUT)
        if any(parent.is_symlink() for parent in file.parents if parent != INPUT and INPUT in parent.parents):
            fail('No se permiten carpetas enlazadas: ' + str(file))
        if len(rel.parts) < 2 or rel.parts[0] not in FOLDERS:
            fail('Ruta no permitida: ' + rel.as_posix())
        if file.name.lower() in {'.gitkeep', '.ds_store', 'thumbs.db'}:
            continue
        if file.name.lower().startswith('.env') or any(x in file.name.lower() for x in SECRET_WORDS):
            fail('Posible archivo sensible, revisa antes de subir: ' + str(rel))
        if any(part in ('', '.', '..') or '\\' in part or ':' in part for part in rel.parts):
            fail('Ruta no permitida: ' + rel.as_posix())
        windows_key = rel.as_posix().casefold()
        if windows_key in seen_windows:
            fail('Dos archivos colisionan en Windows: ' + str(rel))
        seen_windows.add(windows_key)
        if len(specs) >= MAX_FILES:
            fail(f'Hay mas de {MAX_FILES} archivos; el launcher beta no admite tantos.')
        size = file.stat().st_size
        if size == 0:
            fail('Archivo vacio: ' + str(rel))
        if size > MAX_ASSET_SIZE:
            fail('Archivo demasiado grande para un asset: ' + str(rel))
        asset_name = '__'.join(rel.parts)
        if asset_name.casefold() in seen_assets:
            fail('Colision de nombre en GitHub Releases: ' + asset_name)
        seen_assets.add(asset_name.casefold())
        target = staged / asset_name
        shutil.copy2(file, target)
        sha = checksum(target)
        link = f'https://github.com/{REPO}/releases/download/{quote(tag)}/{quote(asset_name)}'
        specs.append({'path': rel.as_posix(), 'url': link, 'sha256': sha})
    if not specs:
        fail('La carpeta publish esta vacia. Coloca todos los mods en publish/mods antes de publicar.')
    manifest = {'schema': 1, 'event': 'Truchosafío 4',
                'minecraft': '1.21.1', 'loader': 'fabric', 'files': specs}
    manifest_file = DIST / 'manifest.json'
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    validate(manifest_file)
    return specs, staged, manifest_file


def ensure_environment():
    if not shutil.which('gh'):
        fail('GitHub CLI (gh) no esta instalado: https://cli.github.com/')
    if not shutil.which('git'):
        fail('Git no esta instalado: https://git-scm.com/download/win')
    who = run('gh', 'api', 'user', '--jq', '.login')
    if who.lower() != 'benexter':
        fail(f'Github CLI inicio sesion como {who!r}; se necesita la cuenta BenExter.')
    repo_info = json.loads(run('gh', 'repo', 'view', REPO, '--json', 'nameWithOwner,isPrivate'))
    if repo_info.get('isPrivate'):
        fail('Repositorio privado: este launcher necesita manifest y assets publicos.')
    branch = run('git', 'branch', '--show-current')
    if branch != 'main':
        fail('Debes publicar desde la rama main.')
    origin = run('git', 'remote', 'get-url', 'origin')
    if REPO.lower() not in origin.lower():
        fail('El remoto origin no corresponde al repositorio oficial: ' + origin)
    status = run('git', 'status', '--porcelain', '--untracked-files=no')
    if status:
        fail('Hay cambios sin guardar en archivos versionados. Haz commit antes de publicar:\n'+status)
    run('git','pull','--ff-only','origin','main',capture=False)


def upload_release(tag, assets):
    note = (f'Actualizacion oficial de Truchosafio 4: {tag}.\n'
            'Minecraft 1.21.1 + Fabric. Archivos comprobados por SHA-256 en manifest.json.')
    print('\nCreando Release en borrador...')
    run('gh', 'release', 'create', tag, '--repo', REPO, '--target', 'main',
        '--title', f'Truchosafio 4 | {tag}', '--notes', note, '--draft',capture=False)
    files = list(sorted(assets.iterdir()))
    print(f'Subiendo {len(files)} archivos a GitHub Releases...')
    for offset in range(0,len(files),35):
        chunk = files[offset:offset+35]
        run('gh','release','upload',tag,*(str(p) for p in chunk),'--repo',REPO,capture=False)
    print('Verificando assets publicados en el borrador...')
    result = json.loads(run('gh','release','view',tag,'--repo',REPO,'--json','assets,isDraft,tagName'))
    remote = {a['name']: a.get('size') for a in result.get('assets',[])}
    for f in files:
        if remote.get(f.name) != f.stat().st_size:
            fail(f'El asset {f.name} no aparece con el tamano esperado en el Release. No se actualizara el manifest.')
    if not result.get('isDraft'):
        fail('El Release no esta en borrador; cancelar por seguridad.')
    run('gh','release','edit',tag,'--repo',REPO,'--draft=false',capture=False)
    print('Release publicado. Actualizando el indice del launcher...')


def update_manifest(manifest_file, tag):
    dest = ROOT / 'manifest.json'
    # We do not modify the live index until ALL assets are public.
    shutil.copyfile(manifest_file, dest)
    run('git','add','manifest.json')
    run('git','commit','-m',f'Publicar modpack {tag}',capture=False)
    run('git','push','origin','main',capture=False)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--tag',help='Etiqueta de Release, por ejemplo pack-20261026-001')
    parser.add_argument('--dry-run', action='store_true',help='Solo generar assets y manifest sin publicar')
    parser.add_argument('--yes', action='store_true', help='No pedir confirmacion interactiva')
    args=parser.parse_args()
    tag=args.tag or dt.datetime.now(dt.timezone.utc).strftime('pack-%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]
    if not re.fullmatch(r'[A-Za-z0-9_.-]{1,80}',tag):
        fail('Etiqueta no valida: ' + tag)
    print('Preparando paquete:',tag)
    specs, staged, manifest_file = prepare(tag)
    print(f'Archivos: {len(specs)}; tamano total: {sum(x.stat().st_size for x in staged.iterdir())/1024/1024:.1f} MiB')
    for spec in specs:
        print(' -',spec['path'],spec['sha256'][:12]+'…')
    if args.dry_run:
        print('SIMULACION TERMINADA. Manifest listo en',manifest_file)
        return
    print('\nATENCION: esto PUBLICARA archivos en el repositorio PUBLICO de GitHub.')
    print('Confirma que tienes permiso de redistribucion y que publish/ contiene TODO el modpack.')
    if not args.yes and input('Escribe PUBLICAR para confirmar: ').strip() != 'PUBLICAR':
        print('Publicacion cancelada. No se ha subido nada.')
        return
    ensure_environment()
    upload_release(tag, staged)
    update_manifest(manifest_file, tag)
    print('\nEXITO. URL oficial: https://raw.githubusercontent.com/'+REPO+'/main/manifest.json')
    print('El launcher descargara esta version en su siguiente inicio.')

if __name__=='__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as ex:
        print('\nERROR:',ex,file=sys.stderr)
        print('La publicacion NO se da por terminada. El manifest actual se actualiza solo al final.',file=sys.stderr)
        sys.exit(1)
