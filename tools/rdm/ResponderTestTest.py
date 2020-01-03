#!/usr/bin/env python
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# ResponderTestTest.py

import unittest
from ResponderTest import TestFixture

"""Test cases for sorting TestFixtures."""

__author__ = 'bruce@lowekamp.net (Bruce Lowekamp)'

# classes for testing sort by class name
class ATestFixture(TestFixture):
  pass

class ZTestFixture(TestFixture):
  pass

class TestFixtureTest(unittest.TestCase):

  def testCmp(self):
    base = TestFixture({}, 2, 123, None)
    base2 = TestFixture({}, 2, 123, None)

    a = ATestFixture({}, 2, 123, None)
    a2 = ATestFixture({}, 2, 123, None)
    z = ZTestFixture({}, 2, 123, None)
    
    self.assertEqual(base, base2)
    self.assertNotEqual(base, a)
    self.assertTrue(a < base)
    self.assertTrue(z > base)
    self.assertTrue(a <= base)
    self.assertTrue(base2 <= base)
    self.assertTrue(z >= base)
    self.assertTrue(base >= base)
    self.assertNotEqual(a, z)
    self.assertTrue(a < z)
    self.assertEqual(a, a2)
    self.assertTrue(z > a)
    
if __name__ == '__main__':
  unittest.main()
