import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dj-git',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License', 
    description='A simple Django app to manage your Git projects.',
    long_description=README,
    author='Taurus Olson',
    author_email='taurusolson@gmail.com',
    url = 'https://github.com/TaurusOlson/django-git',
    keywords = ['django', 'application', 'git', 'projects'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',  
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['pygal', 'django', 'pygit2', 'pytz'],
)
