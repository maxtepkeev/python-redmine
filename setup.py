import sys

from setuptools import setup, find_packages
from setuptools.command.test import test

try:
    import multiprocessing  # https://bugs.python.org/issue15881
except ImportError:
    pass


class NoseTests(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import nose
        nose.run_exit(argv=['nosetests'])

tests_require = ['nose', 'coverage']

if sys.version_info[:2] < (3, 3):
    tests_require.append('mock')
    if sys.version_info[:2] == (2, 6):
        tests_require.append('unittest2')

exec(open('redminelib/version.py').read())

setup(
    name='python-redmine',
    version=globals()['__version__'],
    packages=find_packages(exclude=('tests', 'tests.*')),
    package_data={'requests': ['*.pem']},
    include_package_data=True,
    url='https://python-redmine.com',
    license=open('LICENSE').read(),
    author='Maxim Tepkeev',
    author_email='support@python-redmine.com',
    description='Library for communicating with a Redmine project management application',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    keywords='redmine,redmineup,redminecrm,redminelib,easyredmine',
    tests_require=tests_require,
    cmdclass={'test': NoseTests},
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
