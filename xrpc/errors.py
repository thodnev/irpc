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

"""Contains XRPC-related exceptions."""


class XRPCError(Exception):
    """Common base class for all XRPC exceptions."""

    pass


class XRPCBuildError(XRPCError):
    """Used for all exceptions related to XRPC declarations building process."""

    pass


class XRPCAppError(XRPCError):
    """Unknown (generic) error.

    Also serves as a common base for all XRPC Errors respond to clients.

    Attributes:
        errno (int): Error number
        msg (Optional[str]): Error description message

    Each Error must have at least an `errno` provided.
    Error numbers from -100 to -1 are reserved and should not be used by a user.
    """

    errno = -1
    msg = None
    __errnos__ = {errno}    # contains all errnos to ensure their uniqueness

    def __init_subclass__(cls, /, check_errnos=True):
        """
        Require that every `errno` is unique and subclass does provide a default for it,
        unless a `check_errnos` argument set to False during subclassing.
        """
        if not check_errnos:
            return
        try:
            errno = int(cls.errno)
            errnos = cls.__errnos__
            if errno not in errnos:
                errnos.add(errno)
                return
        except Exception:
            pass
        raise XRPCError(f'Class "{cls.__qualname__}" does not provide valid errno')

    def __init__(self, msg=None, *args, errno=None, **kwargs):
        if errno is not None:
            self.errno = errno
        if msg is not None:
            self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        """Fancy representation."""
        m = f'{self.__class__.__name__}(msg={self.msg!r}'
        m += f', *{self.args!r}' if self.args else ''
        m += f', errno={self.errno}'
        m += f', **{self.kwargs!r})' if self.kwargs else ')'
        return m


class XRPCFormatError(XRPCAppError):
    """Indicates XPRC request has wrong format."""

    errno = -2


class XRPCNotFoundError(XRPCAppError):
    """Indicates requested XRPC method or other resource was not found in endpoint."""

    errno = -3


class XRPCArgumentError(XRPCAppError):
    """Indicates XRPC transport is probably ok, but the method was called with wrong arguments."""

    errno = -4


class XRPCExpiredError(XRPCAppError):
    """Denotes some resource is already expired."""

    errno = -5


class XRPCAuthError(XRPCAppError):
    """Common authentification error serving numerous purposes.

    We don't need to be to specific on errors since we don't want to
    disclose useful information to an attacker.
    """

    errno = -6
