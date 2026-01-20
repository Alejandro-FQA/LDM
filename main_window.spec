# -*- mode: python ; coding: utf-8 -*-

import os
from PyQt5.QtCore import QLibraryInfo

a = Analysis(
    ['main_window.py'],
    pathex=[os.path.abspath(os.getcwd())],
    binaries=[],
    datas=[
        ('atomic_mass.txt', '.'),
        (os.path.join(QLibraryInfo.location(QLibraryInfo.PluginsPath), 'platforms'), 'platforms'),
    ],
    hiddenimports=[
        'activities',                     # Top-level package
        'activities.CAT',
        'activities.CAT.activity1_CAT',
        'activities.CAT.activity2_CAT',
        'activities.EN',
        'activities.EN.activity1_EN',
        'activities.EN.activity2_EN',
        'activities.ES',
        'activities.ES.activity1_ES',
        'activities.ES.activity2_ES',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main_window',
    console=False,
)
