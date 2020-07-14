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

import pyximport
import platform
import sys
from timeit import repeat

# Cythonize once for faster runs
pyximport.install(build_in_temp=True, inplace=False, language_level=3)
import cy

N_ITERS = 100000
N_REPEAT = 1000

totest = ('PureCls', 'SlottedCls', 'CyPureCls', 'CySlottedCls', 'CyCdefIntObj', 'CyCdefObjObj',
          'CyCdefObjObjNoType', 'CyCdefPub', 'CyCdefNord',
          'CyListFunc', 'CyTupleFunc', 'CyTupleNoTypeFunc',
          'CyTupleNoTypeFuncExtArgs', 'CyCandidateExtArgs', 'CyCandidateTypedExtArgs'
          # 'DataCls', 'FrozenAnyDataCls'
          )

init = r"""
from random import randint
try:
    from pure import {name}
except ImportError:
    from cy import {name}
TestCls = {name}
a, b = [randint(0, 100) for i in range(2)]
"""

cmd = r"""
var = TestCls(a, b)
del var
"""

res = {}
for name in totest:
    print(f'>> {name}: ', end='', file=sys.stderr)
    t = repeat(stmt=cmd, setup=init.format(name=name), repeat=N_REPEAT, number=N_ITERS)
    t = sum(t) / len(t)
    print('{:.4f} ms'.format(1000 * t), file=sys.stderr)
    res[name] = t

print(f'*** Results N_ITERS={N_ITERS} N_REPEAT={N_REPEAT}')
print(f'*** ({platform.platform()}):')
res = {k: res[k] for k in sorted(res, key=lambda var: res[var])}
m = max(res.values())
for k, v in res.items():
    print(
        f'{k}: {1000 * v:.4f} ms',
        '({:.2f} % speedup)'.format(100.0 * (m - v) / v) if m != v else '(*)',
        '= {:.2f} op/s'.format(1 / (v / N_ITERS)),
    )
