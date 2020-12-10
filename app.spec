# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['D:\\Users\\mathi\\Documents\\1.Marketing Madheads\\0. Development\\Python1\\Linkbuilding-automation'],
             binaries=[],
             datas=[('templates', 'templates'),
                    ('static', 'static'),
                    ('chromedriver.exe', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='linkbuilder',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')
