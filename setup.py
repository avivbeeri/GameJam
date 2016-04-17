"""
py2app build script for MyApplication

Usage:
    python setup.py py2app
"""
from setuptools import setup
setup(
    app=["game.py"],
	setup_requires=["py2app"],
	options={'py2app':{'iconfile':'Ghost.ico'}}
)