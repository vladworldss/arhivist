import os
import sys
from distutils.sysconfig import get_python_lib

from pip.req import parse_requirements
from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 3.6.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

This version of Arhivist requires Python {}.{}, but you're trying to
install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install arhivist

This will install the latest version of Arhivist which works on your
version of Python. If you can't upgrade your pip (or Python), request
an older version of Arhivist:

    $ python -m pip install "arhivist"
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "arhivist"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break


EXCLUDE_FROM_PACKAGES = ['old']

install_reqs = parse_requirements('requirements.txt', session='build')
install_reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='Arhivist',
    version="1.1.1",

    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    install_requires=install_reqs,

    url='https://github.com/vladworldss/arhivist',
    author='Vladimir Gerasimenko',
    author_email='vladworldss@yandex.ru',
    description=('Arhivist is a web application based on Django.'),

    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    package_dir={'dist': 'dist/'},
    package_data={'dist': ['wheel/*']},
    include_package_data=True,

    scripts=['arhivist/bin/arhivist-admin.py'],
    entry_points={'console_scripts': [
        'arhivist-admin = arhivist.parser.store:execute_from_command_line',
    ]},

    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django :: 1.11',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
)

if overlay_warning:
    sys.stderr.write("""

========
WARNING!
========

You have just installed Arhivist over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
RNT. This is known to cause a variety of problems. You
should manually remove the

%(existing_path)s

directory and re-install Arhivist.

""" % {"existing_path": existing_path})
