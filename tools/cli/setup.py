from setuptools import setup

setup(
    name='caladrius',
    version='0.1',
    py_modules=['caladrius'],
    install_requires=[
        'click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        caladrius=caladrius:cli
    ''',
)
