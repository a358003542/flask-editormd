#!/usr/bin/env python
# -*-coding:utf-8-*-


from setuptools import setup, find_packages
import codecs

REQUIREMENTS = ['flask', 'flask-bootstrap', 'flask-wtf']


def long_description():
    with codecs.open('README.rst', encoding='utf-8') as f:
        return f.read()


setup(
    name='flask_editormd',
    version='0.0.2',
    description='Implementation of editor.md the markdown editor for Flask and Flask-WTF.',
    url='https://github.com/a358003542/flask-editormd',
    long_description=long_description(),
    author='wanze',
    author_email='a358003542@gmail.com',
    maintainer='wanze',
    maintainer_email='a358003542@gmail.com',
    license='MIT',
    platforms='Linux',
    keywords=['flask'],
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'License :: OSI Approved :: MIT License',
                 'Framework :: Flask',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6'],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    setup_requires=REQUIREMENTS,
    install_requires=REQUIREMENTS,
)
