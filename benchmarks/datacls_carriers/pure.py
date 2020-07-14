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

import typing
from dataclasses import dataclass


class PureCls:
    def __init__(self, ret=None, err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret!r}, err={self.err!r})'


class SlottedCls:
    __slots__ = ['err', 'ret']

    def __init__(self, ret=None, err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret!r}, err={self.err!r})'


@dataclass(init=True, repr=False, eq=True, order=False, unsafe_hash=True, frozen=False)
class DataCls:
    ret: typing.Any
    err: int

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret!r}, err={self.err!r})'


@dataclass(init=True, repr=False, eq=True, order=False, unsafe_hash=True, frozen=True)
class FrozenAnyDataCls:
    ret: typing.Any
    err: typing.Any

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret!r}, err={self.err!r})'
