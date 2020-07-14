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

"""..."""


import errors
import functools
import inspect
import logging
import re
# import typing
# from dataclasses import dataclass

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
_hdl = logging.StreamHandler()
_hdl.setFormatter(logging.Formatter('>> %(levelname)s: %(message)s'))
logger.addHandler(_hdl)

# Matches against RFC 3986 section 2.3 Unreserved Characters
_re_urlsafe_match = re.compile(r'[a-zA-Z0-9\-_.~]+').fullmatch


def name_urlsafe(name):
    if not _re_urlsafe_match(name):
        raise errors.IRPCBuildError(f'Name "{name}" does not match url-safe naming scheme')
    return name


def name_urlsafe_lowercase(name):
    return name_urlsafe(name).lower()


def irpcmethod(wrapped_or_empty=None, *, name=None):
    """..."""
    if wrapped_or_empty is not None:
        # assume used as
        #   @method
        #   def somefunc(...):
        func = wrapped_or_empty

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__irpc_name__ = func.__name__
    else:
        # assume used as
        #   @method(name='something')
        #   def somefunc(...):
        def wrapper(func):
            @functools.wraps(func)
            def real_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            real_wrapper.__irpc_name__ = name
            return real_wrapper
    return wrapper


class IRPCMeta(type):
    """..."""

    def __new__(mcls, clsname, clsbases, clsnamespace, *, name=None):
        """..."""
        # perform some checks for fast fail behavior
        for fld in ['__irpc_methods__', '__irpc_name__']:
            if fld in clsnamespace:
                raise errors.IRPCBuildError(f'{fld} field is built by {mcls.__qualname__}')

        # collect all rpc methods and unwrap them
        rpcmethods = []     # list of tuples (rpcname, unwrapped_method)
        for key, val in clsnamespace.items():
            try:
                rpcname = val.__irpc_name__
            except AttributeError:
                continue
            # stop as soon as we reach first wrapper
            # this implies @irpcmethod is used as the outermost decorator
            # method = inspect.unwrap(val, stop=lambda wrp: not hasattr(wrp, '__irpc_name__'))
            method = val.__wrapped__
            logger.debug(f'Unwrapping stage {val}, {method}, {id(val)}, {id(method)}')
            if hasattr(method, '__irpc_name__'):
                raise errors.IRPCBuildError(
                    f'Could not unwrap method "{key}", @irpcmethod must be outermost decorator')

            clsnamespace[key] = method      # set to unwrapped
            rpcmethods.append((rpcname, method))

        # build class eary as we'll need some of its stuff like mro
        retcls = super().__new__(mcls, clsname, clsbases, clsnamespace)
        mro = [base for base in inspect.getmro(retcls) if isinstance(base, mcls)]
        logger.debug(f'Orig mro {inspect.getmro(retcls)}, our mro {mro}')

        # build config values
        config = dict()
        for cls in reversed(mro):
            try:
                config.update(cls.__irpc_config__)
            except AttributeError:
                continue
        logger.debug(f'Config after gathering {config}')

        # Get naming scheme func. It also implies config is not empty and provided somewhere
        naming_scheme = config.get('naming_scheme')
        if not callable(naming_scheme):
            raise errors.IRPCBuildError('naming_scheme not callable, check __irpc_config__')

        # Assign name to class
        #
        # !!!!! CHECK that it works via composition
        #
        retcls.__irpc_name__ = naming_scheme(name if name is not None else clsname)

        # Update class config dict
        retcls.__irpc_config__ = config

        # Collect rpc methods declared inside class
        clsrpc = dict()
        for mtdname, mtd in rpcmethods:
            print(f'processing method "{mtdname}"')
            mtdname = naming_scheme(mtdname)      # perform conversion according to naming scheme
            if mtdname in clsrpc:
                raise errors.IRPCBuildError(
                    f'Duplicate IRPC method name "{mtdname}" in class {retcls.__qualname__}')
            clsrpc[mtdname] = mtd

        logger.debug(f'Collected {len(clsrpc)} rpc methods from class {retcls.__qualname__}: '
                     f'{clsrpc}')

        # Collect rpc methods from base classes
        # here we allow to override names via inheritance
        ...

        # Assign all resulting RPC methods to class
        # this will also allow for fast calls without long traversals
        ...

        # Return our built class
        return retcls

    # def __call__(cls, *args, **kwargs):
    #     raise AttributeError(f'{cls} is not meant for instance creation')

    @classmethod
    def irpc_catchall_method(cls, method, *args, **kwargs):
        """
        This method is used as a catch-all and is called when the requested method
        was not found in the endpoint.
        Default raises a NotFound error resond to client.
        Overriding in subclasses allows to customize its behavior as needed.
        """
        raise errors.IRPCNotFoundError(msg=method)

    @classmethod
    def irpc_handle(cls, method, args=(), kwargs=None, env=None):
        kwargs = kwargs or {}

        ...


# TODO: should there be an env passed as a first argument
# Note: always use / for positional-only arguments
class IRPC(metaclass=IRPCMeta):
    __irpc_config__ = {
        'naming_scheme': name_urlsafe_lowercase
    }

    def gg(self, env, /, arg):
        print('gg', arg)
    pass


class IRPCResponse:
    __slots__ = ['err', 'ret']

    def __init__(self, ret=None, err=0):
        self.ret = ret
        self.err = err

    def __repr__(self):
        return f'{self.__class__.__name__}(ret={self.ret}, err={self.err})'


if __name__ == '__main__':
    class Test(IRPC, name='123'):
        @irpcmethod
        def test(self):
            print('ok')
            super().gg(123, 123)

        @irpcmethod(name='other')
        def test2(self):
            print('ok2')

    test = Test()
    test.test()
