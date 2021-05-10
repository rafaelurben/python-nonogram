from setuptools import setup

setup(
    name="python-nonogram",
    version="0.1.1",
    install_requires=[
        "rich>=10.1.0",
        "click>=7.1.2",
    ],
    entry_points='''
        [console_scripts]
        nonogram=nonogram.commands:main
    ''',
)
