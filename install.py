import sys
import subprocess


ALL = [
    'kivy==1.11.1',
    'Pillow==6.2.0',
    'pylint>=2.4.2',
    'mock==3.0.5',
    'coverage>=4.5.4',
    'kivymd>=0.100.2'
]

WINDOWS = [
    'pypiwin32',
    'kivy-deps.sdl2',
    'kivy-deps.gstreamer',
    'kivy-deps.angle',
    'kivy-deps.glew'
]

LINUX = []

MACOS = []


def install(packages):
    for package in packages:
        subprocess.call([sys.executable, '-m', 'pip', 'install', package])


install(ALL)
platform = sys.platform
if platform == 'win32':
    install(WINDOWS)
elif platform == 'darwin':
    install(MACOS)
else:
    install(LINUX)
