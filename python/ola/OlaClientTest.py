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
# OlaClientTest.py

import itertools
import unittest
from ola.OlaClient import *

"""Test cases for data structures of OlaClient."""

__author__ = 'bruce@lowekamp.net (Bruce Lowekamp)'


class OlaClientTest(unittest.TestCase):

  def allNotEqual(self, t):
    for pair in itertools.combinations(t, 2):
      self.assertNotEqual(pair[0], pair[1])

  def allHashNotEqual(self, t):
    h = map(hash, t)
    for pair in itertools.combinations(h, 2):
      self.assertNotEqual(pair[0], pair[1])
    
      
  def testPlugin(self):
    a = Plugin(1, 2, False, False)
    aeq = Plugin(1, 2, False, False)
    ane1 = Plugin(1, 2, True, False)
    ane2 = Plugin(1, 2, False, True)
    b = Plugin(2, 2, False, False)
    c = Plugin(2, 3, False, False)
    d = Plugin(2, 3, True, False)
    e = Plugin(2, 3, True, True)

    self.assertEqual(a, aeq)
    self.allNotEqual([a, ane1, ane2, b, c, d, e])
    self.allHashNotEqual([a, ane1, ane2, b, c, d, e])

    s = sorted([e, d, c, a, b])
    self.assertEqual([a, b, c, d, e], s)

    self.assertEqual(a.__lt__( "hello"), NotImplemented)
    self.assertNotEqual(a, "hello")

  def testDevice(self):
    a = Device(1, 2, 3, 4, [1, 2], [3, 4])
    aeq = Device(1, 2, 3, 4, [1, 2], [3, 4])
    ane1 = Device(1, 3, 3, 4, [1, 2], [3, 4])
    ane2 = Device(1, 2, 4, 4, [1, 2], [3, 4])
    ane3 = Device(1, 2, 3, 5, [1, 2], [3, 4])
    ane4 = Device(1, 2, 3, 4, [0, 1, 2], [3, 4])
    ane5 = Device(1, 2, 3, 4, [1, 2], [4])
    b = Device(2, 2, 3, 4, [1, 2], [3, 4])
    c = Device(2, 3, 3, 4, [1, 2], [3, 4])
    d = Device(2, 3, 4, 4, [1, 2], [3, 4])
    e = Device(2, 3, 4, 5, [1, 2], [3, 4])
    f = Device(2, 3, 4, 5, [2, 2], [3, 4])
    g = Device(2, 3, 4, 5, [2, 2], [4, 4])

    self.assertEqual(a, aeq)
    self.allNotEqual([a, ane1, ane2, ane3, ane4, ane5, b, c, d, e, f, g])

    s = sorted([g, f, e, d, a, b, c])
    self.assertEqual([a, b, c, d, e, f, g], s)

    self.assertEqual(a.__lt__( "hello"), NotImplemented)
    self.assertNotEqual(a, "hello")

  def testPort(self):
    a = Port(1, 2, 3, 4, False)
    aeq = Port(1, 2, 3, 4, False)
    ane1 = Port(1, 3, 3, 4, False)
    ane2 = Port(1, 2, 4, 4, False)
    ane3 = Port(1, 2, 3, 5, False)
    ane4 = Port(1, 2, 3, 4, True)
    b = Port(2, 2, 3, 4, False)
    c = Port(2, 3, 3, 4, False)
    d = Port(2, 3, 4, 4, False)
    e = Port(2, 3, 4, 5, False)
    f = Port(2, 3, 4, 5, True)

    self.assertEqual(a, aeq)
    self.allNotEqual([a, ane1, ane2, ane3, ane4, b, c, d, e, f])
    self.allHashNotEqual([a, ane1, ane2, ane3, ane4, b, c, d, e, f])

    s = sorted([f, e, d, c, b, a])
    self.assertEqual([a, b, c, d, e, f], s)

    self.assertEqual(a.__lt__( "hello"), NotImplemented)
    self.assertNotEqual(a, "hello")

  def testUniverse(self):
    # universe doesn't have hash and implements eq and < only on id
    a = Universe(1, 2, Universe.LTP, [1, 2], [3, 4])
    aeq = Universe(1, 2, Universe.HTP, [1, 2], [3, 4])
    b = Universe(2, 2, Universe.LTP, [1, 2], [3, 4])
    c = Universe(3, 2, Universe.HTP, [1, 2], [3, 4])

    self.assertEqual(a, aeq)
    self.allNotEqual([a, b, c])

    s = sorted([c, b, a])
    self.assertEqual([a, b, c], s)

    self.assertEqual(a.__lt__( "hello"), NotImplemented)
    self.assertNotEqual(a, "hello")

  def testRDMNack(self):
    a = RDMNack(1, "foo")
    aeq = RDMNack(1, "foo")
    ane1 = RDMNack(2, "foo")
    ane2 = RDMNack(1, "bar")
    b = RDMNack(2, "baz")

    self.assertEqual(a, aeq)
    self.allNotEqual([a, ane1, ane2, b])
    self.allHashNotEqual([a, ane1, ane2, b])

    s = sorted([ane2, ane1, a, b])
    self.assertEqual([ane2, a, b, ane1], s)

    self.assertEqual(a.__lt__( "hello"), NotImplemented)
    self.assertNotEqual(a, "hello")
    
    
if __name__ == '__main__':
  unittest.main()
