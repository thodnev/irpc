# encoding: utf-8
#
# Copyright (C) 2020 Tymofii Khodniev <thodnev@xinity.dev>
#
# This file is part of XRPC.
#
# XRPC is free software: you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# XRPC is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with XRPC.
# If not, see <https://www.gnu.org/licenses/>.

class CyPureCls:
    def __init__(self, ret=None, err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret}, err={self.err})'


class CySlottedCls:
    __slots__ = ['err', 'ret']

    def __init__(self, ret=None, err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret}, err={self.err})'


cdef class CyCdefIntObj:
    cdef readonly object ret
    cdef readonly int err

    def __cinit__(self, ret=None, int err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret}, err={self.err})'


cdef class CyCdefObjObj:
    cdef readonly object ret
    cdef readonly object err

    def __cinit__(self, ret=None, int err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret}, err={self.err})'


cdef class CyCdefObjObjNoType:
    cdef public object ret
    cdef public object err

    def __cinit__(self, ret=None, err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret}, err={self.err})'


cdef class CyCdefPub:
    cdef public object ret
    cdef public int err

    def __cinit__(self, ret=None, int err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret}, err={self.err})'


cdef class CyCdefNord:
    cdef object ret
    cdef int err

    def __cinit__(self, ret=None, int err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret}, err={self.err})'


def CyListFunc(ret=None, int err=0):
    return [ret, err]


def CyTupleFunc(ret=None, int err=0):
    return ret, err


def CyTupleNoTypeFunc(ret=None, err=0):
    return ret, err

def CyTupleNoTypeFuncExtArgs(ret=None, errcode=0, errdata=None):
    return ret, errcode, errdata

cdef class CyCandidateExtArgs:
    cdef readonly object ret
    cdef readonly int errcode
    cdef readonly object errdata

    def __cinit__(self, ret=None, int errcode=0, errdata=None):
        self.ret = ret
        self.errcode = errcode
        self.errdata = errdata

    def __repr__(self):
        fmt = '{cls}(ret={ret!r}, errcode={errcode!r}, errdata={errdata!r})'
        return fmt.format(cls=self.__class__.__name__,
                          ret=self.ret,
                          errcode=self.errcode,
                          errdata=self.errdata)


cdef class CyCandidateTypedExtArgs:
    cdef readonly object ret
    cdef readonly int errcode
    cdef readonly object errdata

    def __cinit__(self, object ret=None, int errcode=0, object errdata=None):
        self.ret = ret
        self.errcode = errcode
        self.errdata = errdata

    def __repr__(self):
        fmt = '{cls}(ret={ret!r}, errcode={errcode!r}, errdata={errdata!r})'
        return fmt.format(cls=self.__class__.__name__,
                          ret=self.ret,
                          errcode=self.errcode,
                          errdata=self.errdata)
