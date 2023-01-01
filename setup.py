# -*- coding: utf-8 -*-
import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    README = f.read()

setuptools.setup(
    name='sqlite-tools',
    version='0.0.1',
    description='This is a collection of tools to help you work with SQLite databases.',
    author='VeronicaAlexia',
    author_email='',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/VeronicaAlexia/sqlite-tools',
    download_url='https://github.com/VeronicaAlexia/sqlite-tools',
    packages=[
        'tools_sqlite'
    ],
    keywords=[
        'typing',
        'sqlite3',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
    ],
    license='MIT',
    python_requires='>=3.6',
)