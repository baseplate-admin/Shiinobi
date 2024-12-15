# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['./src/shiinobi/cli.py'],
    pathex=['./src/shiinobi'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=['./src/_pyinstaller'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["packaging","pkg_resources","setuptools"],
    noarchive=True,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='shiinobi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='./assets/shiinobi.png',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
