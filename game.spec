# -*- mode: python -*-

block_cipher = None

added_files = 	[
		('assets/images/*.png', 'assets/images'),
		('assets/fonts/*','assets/fonts'),
		('assets/levels/*','assets/levels'),
		('assets/music/*','assets/music'),
		('assets/sounds/*','assets/sounds'),
		]

a = Analysis(['game.py'],
             pathex=['/home/tester/GameJam'],
             binaries=None,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='game',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='game')
