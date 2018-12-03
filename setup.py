from os import path
from setuptools import setup


HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='storm-indicator-pyqt',
    version='1.0',
    description='PyQt based indicator for connecting to your SSH connections easily.',
    long_description=LONG_DESCRIPTION,

    url='https://github.com/olegbuevich/storm-indicator',

    license='MIT',

    author='Oleg Buevich',
    author_email='gangs1989@gmail.com',

    packages=['storm_indicator_pyqt'],

    entry_points={
        'console_scripts': [
            'ssh-indicator-pyqt = storm_indicator_pyqt.__main__',
        ]
    },

    package_data={'storm_indicator_pyqt': ['icons/tray.svg']},

    install_requires=[
        "stormssh",
        "PyQt5",
        "envparse",
    ],
)
