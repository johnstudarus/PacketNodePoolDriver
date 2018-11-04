# Copyright (C) 2018 JHL Consulting LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from pprint import pprint

import logging

import packet

from nodepool import zk

from nodepool.driver.utils import NodeLauncher
from nodepool.driver import NodeRequestHandler

class PacketNodeRequestHandler(NodeRequestHandler):

    log = logging.getLogger("nodepool.driver.packet.PacketNodeRequestHandler")

    def __init__(self, pw, request):
        super().__init__(pw, request)

    def launch(self, node):
        label = self.pool.labels[node.type[0]]

        manager = packet.Manager(self.provider.auth_token)

        try:
          device = manager.create_device(project_id = self.provider.project_id,
                                         hostname = node.id,
                                         plan = label.plan,
                                         facility = self.provider.facility,
                                         operating_system = label.operating_system)
        except packet.baseapi.Error as e:
          self.log.info("Node id %s failed %s", e.args[0])
          node.state = zk.FAILED
          self.zk.storeNode(node)
          return

        node.external_id = device.id
        node.state = zk.READY
        self.zk.storeNode(node)
        self.log.info("Node id %s is ready", node.id)

    @property
    def alive_thread_count(self):
        return 0

    def imagesAvailable(self):
        manager = packet.Manager(self.provider.auth_token)

        # start off hoping all is well
        found_plan = False

        # TODO - replace with plan from configuration file
        target_plan = "baremetal_1"

        list_plans = manager.list_plans()

        for plan_i in list_plans:
          plan = str(plan_i)
          if target_plan == plan:
              found_plan = True

#        target_operating_system = "ubuntu_14_04"
#        found_operating_system = False
#
#        for operating_system_i in manager.list_operating_systems():
#          operating_system = str(operating_system_i)
#          if operating_system == target_operating_system:
#              found_operating_system = True
#
        # TEMP TODO
        found_operating_system = True

        return found_plan and found_operating_system

    def launchesComplete(self):
        # possible Packet states include 'queued', 'provisioning'
        areLaunchesComplete = True
        
        for node in self.nodeset:
          manager = packet.Manager(self.provider.auth_token)
          try:
            device = manager.get_device(node.external_id)
            if len(device.ip_addresses) >= 2:
              node.public_ipv4 = device.ip_addresses[0]['address']
              node.public_ipv6 = device.ip_addresses[1]['address']
              node.private_ipv4 = device.ip_addresses[2]['address']
            else:
              areLaunchesComplete = False
            self.zk.storeNode(node)
          except packet.baseapi.Error as e:
            # if we can't find it then the launch is completed (even if it failed)
            self.log.info(e.args[0])


          # todo - could be failed as well...
          if device.state != "active":
            areLaunchesComplete = False

          self.log.info("device %s state %s", node.external_id, device.state)
          
        return areLaunchesComplete
