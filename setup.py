import sys
from setuptools import setup
from pkg_resources import get_distribution, DistributionNotFound

try:
    get_distribution('pyredmine')
    sys.stdout.write('''
{delimiter}
                  INSTALLATION ABORTED

PyRedmineWS library was found on this system. Unfortunately
Python Redmine and PyRedmineWS can't work together because
they both use the same package name, i.e. redmine. There is
no need to use PyRedmineWS because it's development seems
to be discontinued and Python Redmine provides a lot more
features than PyRedmineWS. In order to complete the install
process, please uninstall PyRedmineWS first and rerun the
installation procedure for Python Redmine afterwards
{delimiter}

'''.format(delimiter='=' * 60))
    sys.exit(0)
except DistributionNotFound:
    pass

exec(open('redmine/version.py').read())

setup(
    name='python-redmine',
    version=globals()['__version__'],
    packages=['redmine'],
    url='https://github.com/maxtepkeev/python-redmine',
    license=open('LICENSE').read(),
    author='Max Tepkeev',
    author_email='tepkeev@gmail.com',
    description='Library for communicating with a Redmine project management application',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    keywords='redmine',
    install_requires=['requests >= 0.12.1'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
