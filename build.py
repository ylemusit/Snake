import PyInstaller.__main__ as PI

PI.run([
    'src/main.py',
    '--onefile',
    '--name', 'Sneak',
    '--icon', 'assets/images/icon.ico',
    '--add-data', 'assets;assets',
    '--add-data', 'config;config',
    '--paths', 'src'
])