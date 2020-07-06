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

cdef class XRPCResponse:
    cdef readonly object ret
    cdef readonly int errcode
    cdef readonly object errdata

    def __cinit__(self, ret=None, int errcode=0, errdata=None):
        self.ret = ret
        self.errcode = errcode
        self.errdata = errdata

    def __repr__(self):
        msg = f'{self.__class__.__name__}('
        if self.errcode == 0 and self.errdata is None:
            return msg + f'ret={self.ret!r})'
        if self.ret is not None:
            msg += f'ret={self.ret!r}, '
        msg += f'errcode={self.errcode!r}'
        if self.errdata is not None:
            return msg + f', errdata={self.errdata!r})'
        return msg + ')'
