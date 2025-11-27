# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['dotenv', 'mysql.connector', 'mysql.connector.plugins', 'mysql.connector.plugins.mysql_native_password', 'mysql.connector.plugins.caching_sha2_password']
hiddenimports += collect_submodules('mysql.connector')
hiddenimports += collect_submodules('dotenv')


a = Analysis(
    ['main.py'],
    pathex=['./venv/lib/python3.13/site-packages'],
    binaries=[],
    datas=[('img', 'img')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GestionClientesJP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
