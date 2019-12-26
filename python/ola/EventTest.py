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
# EventTest.py

import datetime
import sys
import timeout_decorator
import unittest
from ola.ClientWrapper import ClientWrapper
from ola.ClientWrapper import _Event


"""Test cases for the Event and Event loop of ClientWrapper class."""

__author__ = 'bruce@lowekamp.net (Bruce Lowekamp)'


class EventTest(unittest.TestCase):

  def testEventCmp(self):
    a = _Event(0.5, None)
    b = _Event(1, None)
    b2 = _Event (1, None)
    b2._run_at = b._run_at # tests rely on timestamps being actually equal
    b3 = _Event (1, 2)
    b3._run_at = b._run_at
    
    self.assertEqual(b, b2)
    self.assertNotEqual(b, b3)
    self.assertTrue(a != b)
    self.assertFalse(b != b2)
    self.assertTrue(b == b2)
    self.assertTrue(a < b)
    self.assertTrue(a <= b)
    self.assertTrue(b > a)
    self.assertTrue(b >= a)

    self.assertFalse(a == b2)
    self.assertFalse(b < a)
    self.assertFalse(b <= a)
    self.assertFalse(a > b)
    self.assertFalse(a >= b)

    # these depend on hash(None) < hash(2)
    self.assertTrue (b < b3)
    self.assertFalse(b > b3)

    s = "teststring"
    self.assertNotEqual(a, s)
    self.assertEqual(a.__lt__(s), NotImplemented)

  def testEventHash(self):
    a = _Event(0.5, None)
    b = _Event(1, None)
    b2 = _Event (1, None)
    b2._run_at = b._run_at
    b3 = _Event (1, 2)
    b3._run_at = b._run_at

    self.assertEqual(hash(a), hash(a))
    self.assertNotEqual(hash(a), hash(b))
    self.assertEqual(hash(b), hash(b2))
    self.assertNotEqual(hash(b), hash(b3))


  @timeout_decorator.timeout(2)
  def testBasic(self):
    wrapper = ClientWrapper()
    class results:
      a_called = False
      b_called = False

    def a():
      results.a_called = True
      
    def b():
      results.b_called = True
      wrapper.Stop()
      
    wrapper.AddEvent(0, a)
    wrapper.AddEvent(0, b)
    self.assertFalse(results.a_called)
    wrapper.Run()
    self.assertTrue(results.a_called)
    self.assertTrue(results.b_called)


  @timeout_decorator.timeout(2)
  def testEventLoop(self):
    wrapper = ClientWrapper()
    class results:
      a_called = False
      b_called = False
      c_called = False
      d_called = False
      
    def a():
      self.a_time = datetime.datetime.now()
      self.assertFalse(results.a_called)
      self.assertFalse(results.b_called)
      self.assertFalse(results.c_called)
      self.assertFalse(results.d_called)
      results.a_called = True
      
    def b():
      self.b_time = datetime.datetime.now()
      self.assertTrue(results.a_called)
      self.assertFalse(results.b_called)
      self.assertFalse(results.c_called)
      self.assertFalse(results.d_called)
      results.b_called = True

    def c():
      self.c_time = datetime.datetime.now()
      self.assertTrue(results.a_called)
      self.assertTrue(results.b_called)
      self.assertFalse(results.c_called)
      self.assertFalse(results.d_called)
      results.c_called = True

    def d():
      self.d_time = datetime.datetime.now()
      self.assertTrue(results.a_called)
      self.assertTrue(results.b_called)
      self.assertTrue(results.c_called)
      self.assertFalse(results.d_called)
      results.d_called = True
      wrapper.AddEvent(0, wrapper.Stop)


    self.start = datetime.datetime.now()
    wrapper.AddEvent(0, a)
    wrapper.AddEvent(15, d)
    wrapper.AddEvent(datetime.timedelta(milliseconds=5), b)
    wrapper.AddEvent(10, c)

    self.assertFalse(results.a_called)
    self.assertFalse(results.b_called)
    self.assertFalse(results.c_called)
    self.assertFalse(results.d_called)

    self.start = datetime.datetime.now()
    wrapper.Run()
    
    self.assertTrue(results.a_called)
    self.assertTrue(self.a_time - self.start < datetime.timedelta(milliseconds=5))
    self.assertTrue(results.b_called)
    self.assertTrue(self.b_time - self.start >= datetime.timedelta(milliseconds=5))
    self.assertTrue(results.c_called)
    self.assertTrue(self.c_time - self.start >= datetime.timedelta(milliseconds=10))
    self.assertTrue(results.d_called)
    self.assertTrue(self.d_time - self.start >= datetime.timedelta(milliseconds=15))



if __name__ == '__main__':
  unittest.main()
