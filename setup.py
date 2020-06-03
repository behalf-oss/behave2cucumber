from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='behave2cucumber',

    version='1.0.4.1',

    description='Behave to Cucumber json converter (lawnmowerlatte fork)',
    long_description='This project helps solving the incompatibilty of Behave\'s genereated json reports '
                     'to tools using Cucumber json reports. '
                     'Its done by reformatting the Behave json to Cucumber json. '
                     'This fork contains a fix by lawnmowerlatte which has not been pulled into the main repo.',

    url='https://github.com/lawnmowerlatte/behave2cucumber',

    author='Andrey Goldgamer, Zvika Messing',
    author_email='andrey.goldgamer@behalf.com, zvika@behalf.com ',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='behave2cucumber setuptools development cucumber behave automation json',

    packages=find_packages(),

    install_requires=[],

    extras_require={},

    data_files=[],

    entry_points={
        'console_scripts': [
            'behave2cucumber = behave2cucumber.behave2cucumber.__main__:main'
        ],
    },
)
