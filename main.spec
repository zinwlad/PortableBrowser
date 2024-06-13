# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['I:\MY_PROGRAMS\PortableBrowser\pythonProject\dist'],
             binaries=[],
             datas=[('site_data.py', '.')],  # Включаем файл site_data.py
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PortableBrowser',  # Имя вашего исполняемого файла без расширения
          debug=False,
          strip=False,
          upx=True,
          console=False)  # Установите True, если вы хотите консольное приложение

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PortableBrowser')  # Имя вашего итогового каталога или exe-файла

