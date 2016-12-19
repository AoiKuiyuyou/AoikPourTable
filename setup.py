# coding: utf-8
#
from __future__ import absolute_import

from setuptools import find_packages
from setuptools import setup


#
setup(
    name='AoikPourTable',

    version='0.1.0',

    description="""Pour data in out of table.""",

    long_description="""`Documentation on Github
<https://github.com/AoiKuiyuyou/AoikPourTable>`_""",

    url='https://github.com/AoiKuiyuyou/AoikPourTable',

    author='Aoi.Kuiyuyou',

    author_email='aoi.kuiyuyou@google.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='table import export',

    package_dir={
        '': 'src'
    },

    packages=find_packages('src'),

    install_requires=[
        'SQLAlchemy>=0.8, >=0.9, >=1.0'
    ],

    entry_points={
        'console_scripts': [
            'aoikpourtable=aoikpourtable.aoikpourtable:main',
        ],
    },
)
