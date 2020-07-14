#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (C) 2020 Tymofii Khodniev <thodnev@xinity.dev>
#
# This file is part of IRPC.
#
# IRPC is free software: you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# IRPC is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with IRPC.
# If not, see <https://www.gnu.org/licenses/>.

import os
import pathlib as pth
import sys
import irpc
from setuptools import Extension, find_packages, setup
from Cython.Build import cythonize


def warn(msg, *args, **kwargs):
    print('\nWarning:', msg, *args, end='\n\n', file=sys.stderr, **kwargs)


# Dirty hack used to avoid including some stuff in binary distributions
is_bdist = any(['bdist' in i for i in sys.argv[1:]])

# Use architecture-dependent optimizations for builds from source. Passing -march=native
# provides better performance, but compiled extensions will be unable to run on machines
# other than used to build them.
# So we don't use -march=native for distributing binary packages (bdist)
CFLAGS_DEFAULT = '-O2'
LDFLAGS_DEFAULT = '-flto'
if not is_bdist:
    CFLAGS_DEFAULT += ' -march=native'

# access through resource manager API
# long_description = pkg_resources.resource_string(__name__, 'README.rst').decode('utf-8')

project_dir = pth.Path(__file__).resolve().parent
long_description = project_dir.joinpath('README.rst').read_text()
CFLAGS = os.environ.get('CFLAGS', CFLAGS_DEFAULT)
LDFLAGS = os.environ.get('LDFLAGS', LDFLAGS_DEFAULT)
use_line_trace = bool(int(os.environ.get('USE_LINE_TRACE', '0')))

if use_line_trace:
    warn('Cython line trace enabled (USE_LINE_TRACE env var set). '
         'This is intended only for coverage and profiling')
    CFLAGS += ' -DCYTHON_TRACE=1'

if is_bdist and use_line_trace:
    exit('Error: building binary distribution with line tracing is inefficient and disallowed')

if '-march=native' in CFLAGS.split(' '):
    warn('Using architecture-dependent optimizations to build package with higer performance.',
         'But it will be unable to run on architectures other than the current one')

extensions = [
    Extension(
        name='irpc.native.*',
        sources=['irpc/native/*.pyx'],
        extra_compile_args=CFLAGS.split(' '),
        extra_link_args=LDFLAGS.split(' '),
        language='c'
    )
]

extensions = cythonize(
    extensions,
    compiler_directives=dict(
        embedsignature=True,        # needed for Sphinx to parse
        language_level=3,           # no python 2 compatability makes it faster
        emit_code_comments=True,    # add original code as C comments
        linetrace=use_line_trace    # needed for coverage reports
    )
)


setup(
    packages=find_packages(exclude=['tests']),
    package_data={'': ['*.pyx' if not is_bdist else '']},
    ext_modules=extensions,
    name='irpc',
    version=irpc.__version__,
    install_requires=[],
    author='thodnev',
    author_email='thodnev@xinity.dev',
    description='Lightning-fast transport-agnostic RPC with asyncio support',
    license='LGPL-3.0-or-later',
    license_files=['COPYING', 'COPYING.LESSER'],
    long_description=long_description,
    long_description_content_type='text/x-rst',   # text, text/x-rst or text/markdown
    keywords=['some', 'key', 'words'],
    python_requires='>=3.8',
    # platforms=[],
    url='https://github.com/thodnev/irpc',
    # project_urls={
    #     "Bug Tracker": "https://bugs.example.com/HelloWorld/",
    #     "Documentation": "https://docs.example.com/HelloWorld/",
    #     "Source Code": "https://code.example.com/HelloWorld/",
    # },
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Object Brokering',
    ]
)
