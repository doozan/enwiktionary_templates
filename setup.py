from setuptools import setup

setup(
    name='enwiktionary_templates',
    description='A just-enough implementation of some enwiktionary.org templates to generate useful data',
    url='https://github.com/doozan/enwiktionary_templates',
    author='Jeff Doozan',
    author_email='github@doozan.com',
    license='GPL 3',
    packages=['enwiktionary_templates', 'enwiktionary_templates.module', 'enwiktionary_templates.es'],
    install_requires=['mwparserfromhell'],
)
