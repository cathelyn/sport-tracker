from setuptools import setup

with open("requirements.txt") as req_file:
    REQUIREMENTS: list = req_file.readlines()

setup(
    name='sport_tracker',
    version='0.0.3',
    author='Katarina Bulkova',
    author_email='bulkova.katarina@gmail.com',
    description='CLI Sport Diary',
    packages=['sport_tracker', 'sport_tracker.common', 'sport_tracker.controller', 'sport_tracker.view'],
    platforms=['linux'],
    python_requires=">=3.7",
    license="GPL",
    entry_points={
        'console_scripts': [
            'sport_tracker = sport_tracker.__main__:main'
         ]
    },
    install_requires=REQUIREMENTS
)
