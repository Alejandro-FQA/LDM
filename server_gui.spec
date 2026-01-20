# -*- mode: python ; coding: utf-8 -*-
import os
from PyQt5.QtCore import QLibraryInfo

a = Analysis(
    ['divulgacion_server/server_gui.py'],
    pathex=[os.path.abspath(os.getcwd())],  # Add project root to help find local modules
    binaries=[],
    datas=[
        ('divulgacion_server/templates', 'divulgacion_server/templates'),
        (os.path.join(QLibraryInfo.location(QLibraryInfo.PluginsPath), 'platforms'), 'platforms'),
    ],
    hiddenimports=[
        'flask_socketio',
        'socketio',
        'engineio',
        'engineio.socketio', 
        'engineio.async_drivers.threading',  # Critical for threading mode
        'engineio.async_threading',         # Older versions sometimes use this
        'simple_websocket',                 # Used in newer python-socketio versions
    ],
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
    name='server_gui',
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