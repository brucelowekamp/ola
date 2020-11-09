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
# RDMTest.py
# Copyright (C) 2019 Bruce Lowekamp

import binascii
import os
import socket
# import timeout_decorator
import unittest
from ola import PidStore
from ola.ClientWrapper import ClientWrapper
from ola.RDMAPI import RDMAPI
from ola.UID import UID


"""Test cases for RDM device commands."""

__author__ = 'bruce@lowekamp.net (Bruce Lowekamp)'

global pidStorePath


class RDMTest(unittest.TestCase):
  # @timeout_decorator.timeout(2)
  def testGetWithResponse(self):
    """uses client to send an RDM get with mocked olad.
    Regression test that confirms sent message is correct and
    sends fixed response message."""
    sockets = socket.socketpair()
    wrapper = ClientWrapper(sockets[0])
    pid_store = PidStore.GetStore(pidStorePath)
    client = wrapper.Client()
    rdm_api = RDMAPI(client, pid_store)

    class results:
      gotrequest = False
      gotresponse = False

    def DataCallback(self):
      # request and response for
      # ola_rdm_get.py -u 1 --uid 7a70:ffffff00 device_info
      # against olad dummy plugin
      # enable logging in rpc/StreamRpcChannel.py
      data = sockets[1].recv(4096)
      expected = binascii.unhexlify(
        "29000010080110001a0a52444d436f6d6d616e6422170801120908f0f4011500"
        "ffffff180020602a0030003800")
      self.assertEqual(data, expected,
                       msg="Regression check failed. If protocol change "
                       "was intended set expected to: " +
                       str(binascii.hexlify(data)))
      results.gotrequest = True
      response = binascii.unhexlify(
        "3f0000100802100022390800100018002213010000017fff0000000300050204"
        "00010000032860300038004a0908f0f4011500ffffff520908f0f40115ac1100"
        "02580a")
      sent_bytes = sockets[1].send(response)
      self.assertEqual(sent_bytes, len(response))

    def ResponseCallback(self, response, data, unpack_exception):
      results.gotresponse = True
      self.assertEqual(response.response_type, client.RDM_ACK)
      self.assertEqual(response.pid, 0x60)
      self.assertEqual(data["dmx_footprint"], 5)
      self.assertEqual(data["software_version"], 3)
      self.assertEqual(data["personality_count"], 4)
      self.assertEqual(data["device_model"], 1)
      self.assertEqual(data["current_personality"], 2)
      self.assertEqual(data["protocol_major"], 1)
      self.assertEqual(data["protocol_minor"], 0)
      self.assertEqual(data["product_category"], 32767)
      self.assertEqual(data["dmx_start_address"], 1)
      self.assertEqual(data["sub_device_count"], 0)
      self.assertEqual(data["sensor_count"], 3)
      wrapper.AddEvent(0, wrapper.Stop)

    wrapper._ss.AddReadDescriptor(sockets[1], lambda: DataCallback(self))

    uid = UID.FromString("7a70:ffffff00")
    pid = pid_store.GetName("DEVICE_INFO")
    rdm_api.Get(1, uid, 0, pid, lambda x, y, z: ResponseCallback(self, x, y, z))

    wrapper.Run()

    sockets[0].close()
    sockets[1].close()

    self.assertTrue(results.gotrequest)
    self.assertTrue(results.gotresponse)

  # @timeout_decorator.timeout(2)
  def testGetParamsWithResponse(self):
    """uses client to send an RDM get with mocked olad.
    Regression test that confirms sent message is correct and
    sends fixed response message."""
    sockets = socket.socketpair()
    wrapper = ClientWrapper(sockets[0])
    pid_store = PidStore.GetStore(pidStorePath)
    client = wrapper.Client()
    rdm_api = RDMAPI(client, pid_store)

    class results:
      gotrequest = False
      gotresponse = False

    def DataCallback(self):
      # request and response for
      # ola_rdm_get.py -u 1 --uid 7a70:ffffff00 parameter_description 17
      # against olad dummy plugin
      # enable logging in rpc/StreamRpcChannel.py
      data = sockets[1].recv(4096)
      expected = binascii.unhexlify(
        "2b000010080110001a0a52444d436f6d6d616e6422190801120908f0f4011500"
        "ffffff180020512a02001130003800")
      self.assertEqual(data, expected,
                       msg="Regression check failed. If protocol change "
                       "was intended set expected to: " +
                       str(binascii.hexlify(data)))
      results.gotrequest = True
      response = binascii.unhexlify(
        "2e000010080210002228080010021800220200062851300038004a0908f0f401"
        "1500ffffff520908f0f40115ac107de05811")
      sent_bytes = sockets[1].send(response)
      self.assertEqual(sent_bytes, len(response))

    def ResponseCallback(self, response, data, unpack_exception):
      results.gotresponse = True
      self.assertEqual(response.response_type, client.RDM_NACK_REASON)
      wrapper.AddEvent(0, wrapper.Stop)

    wrapper._ss.AddReadDescriptor(sockets[1], lambda: DataCallback(self))

    uid = UID.FromString("7a70:ffffff00")
    pid = pid_store.GetName("PARAMETER_DESCRIPTION")
    rdm_api.Get(1, uid, 0, pid,
                lambda x, y, z: ResponseCallback(self, x, y, z), args=["17"])

    wrapper.Run()

    sockets[0].close()
    sockets[1].close()

    self.assertTrue(results.gotrequest)
    self.assertTrue(results.gotresponse)


if __name__ == '__main__':
  pidStorePath = (os.environ.get('PIDSTOREDIR', "../data/rdm"))
  unittest.main()
