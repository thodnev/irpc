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

"""irpc.native.carriers test."""

import unittest
from irpc.native import carriers


class TestIRPCResponseAvailability(unittest.TestCase):
    """Test that IRPCResponse is available at all."""

    def test_availability(self):
        """Determine whether IRPCResponse class persists in carriers."""
        self.assertIn('IRPCResponse', dir(carriers))

    def test_callable(self):
        """Ensure IRPCResponse is at least callable."""
        self.assertTrue(callable(carriers.IRPCResponse))


class TestIRPCResponse(unittest.TestCase):
    """Test IRPCResponse core functionality."""

    @classmethod
    def setUpClass(testcls):
        testcls.Cls = carriers.IRPCResponse

    def test_instance(self):
        """Create empty IRPCResponse object and ensure isinstance works."""
        obj = self.Cls()
        self.assertIsInstance(obj, self.Cls)

    def test_create_nonempty(self):
        """Ensure IRPCResponse accepts ret, errcode and errdata arguments."""
        self.Cls(ret='some message')
        self.Cls(errcode=-1)
        self.Cls(errcode=-10, errdata=['error description', 'other'])

    def test_repr(self):
        """Verify __repr__ method of IRPCResponse."""
        name = 'IRPCResponse'
        # only ret -- normal non-error case
        obj = self.Cls(ret=['ret'])
        self.assertEqual(repr(obj), name + "(ret=['ret'])")
        # errors with code and optional data
        obj = self.Cls(errcode=-1024)
        self.assertEqual(repr(obj), name + "(errcode=-1024)")
        obj = self.Cls(errcode=-1024, errdata=(None, 1))
        self.assertEqual(repr(obj), name + "(errcode=-1024, errdata=(None, 1))")
        # only error data passed -- abnormal. code still needs to be present
        obj = self.Cls(errdata=(None, 1))
        self.assertEqual(repr(obj), name + "(errcode=0, errdata=(None, 1))")
        # everything -- abnormal, error and return at same time
        obj = self.Cls(ret=['ret'], errcode=-1024, errdata=(None, 1))
        self.assertEqual(repr(obj), name + "(ret=['ret'], errcode=-1024, errdata=(None, 1))")
        # ret and errdata -- abnormal. everything must be printed
        obj = self.Cls(ret=['ret'], errdata=(None, 1))
        self.assertEqual(repr(obj), name + "(ret=['ret'], errcode=0, errdata=(None, 1))")

    def test_errcode_inttype(self):
        """Ensure errcode accepts only integer values and error is thrown otherwise."""
        # we will also test against subclasses
        class IntSubclass(int):
            pass

        self.Cls(errcode=100)
        self.Cls(errcode=-100)
        self.Cls(errcode=IntSubclass(10))
        self.Cls(errcode=True)  # bool is a subclass of int
        self.Cls(errcode=3.0)  # ok since it is convertable

        with self.assertRaises(TypeError):
            self.Cls(errcode=None)

        with self.assertRaises(TypeError):
            self.Cls(errcode='str')

    def readback(self, obj: carriers.IRPCResponse) -> tuple:
        """Represent IRPCResponse contents as 3-tuple. Helper function."""
        return (obj.ret, obj.errcode, obj.errdata)

    def test_readable(self):
        """Ensure we can read back values passed when the object is created."""
        obj = self.Cls()
        self.assertEqual(self.readback(obj), (None, 0, None))
        obj = self.Cls(errdata=[123, 'msg'])
        self.assertEqual(self.readback(obj), (None, 0, [123, 'msg']))

    def test_nonwritable(self):
        """Ensure object is immutable and attribute writes will lead to errors."""
        obj = self.Cls(ret='test')
        # main attributes
        with self.assertRaises(AttributeError):
            obj.ret = 'other'
        with self.assertRaises(AttributeError):
            obj.errcode = -1
        with self.assertRaises(AttributeError):
            obj.errdata = 'smth'
        # and unlisted too
        with self.assertRaises(AttributeError):
            obj.nonexistent_attr = 'smth'
