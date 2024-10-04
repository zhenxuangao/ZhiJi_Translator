import PyInstaller.__main__

PyInstaller.__main__.run([
    'codes/ZhiJiTranslator.py',
    '--onefile',
    '--windowed',
    '--name=ZhiJiTranslator',
    '--add-data=translator_config.json;.',
    '--add-data=assets;assets',
])