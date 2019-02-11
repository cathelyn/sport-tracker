from setuptools import setup\n
setup(
    name='sport_tracker',
    version='0.0.1',
    packages=['sport_tracker'],
    entry_points={
        'console_scripts': [
            'sport_tracker = sport_tracker.__main__:main'
         ]
    })
