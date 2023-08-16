from setuptools import setup, find_packages

setup(
    name='aris',
    version='0.1',
    install_requires=[
        'asciimatics',
    ],
    entry_points={
        'console_scripts': [
            'aris = aris_pack.aris:main'
        ]
    },
)