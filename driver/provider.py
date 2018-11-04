# Copyright (C) 2018 JHL Consulting LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import threading
import time
import uuid

import packet


from nodepool import exceptions
from nodepool.nodeutils import iterate_timeout
from nodepool.driver import Provider

from nodepool.driver.packet import handler


class PacketProvider(Provider):
    log = logging.getLogger("nodepool.driver.packet.PacketProvier")

    def __init__(self, provider, use_taskmanager):
        self.provider = provider
        self.use_task_manager = use_taskmanager

    def labelReady(self, name):
#
# TODO
#
# On Packet, a label is ready if:
#   facility exists
#   plan exists
#   operating_system exists
#
# No checking for quota/capacity is performed
# No checking tht the specific plan exists at the specific facility
#
        return True

    def cleanupNode(self, server_id):
        manager = packet.Manager(self.provider.auth_token)
        try:
          device = manager.get_device(server_id)
          device.delete()
        except packet.baseapi.Error as e:  
            if e.args[0] == 'Error 404: Not found':
                return 
            if e.args[0] == 'Error 422: Cannot delete a device while it is provisioning':
                return 
            if e.args[0] == 'Error 403: You are not authorized to view this device':
                return 
            else:
                raise e


    def getRequestHandler(self, poolworker, request):
        return handler.PacketNodeRequestHandler(poolworker, request)

    def getRequestHandler(self, poolworker, request):
        return handler.PacketNodeRequestHandler(poolworker, request)

    def cleanupLeakedResources(self):
        """Clean up any leaked resources

        This is called periodically to give the provider a chance to
        clean up any resources which make have leaked.
        """
        pass

    def join(self):
        """Wait for provider to finish

        On shutdown, this is called after
        :py:meth:`~nodepool.driver.Provider.stop` and should return
        when the provider has completed all tasks.  This may not be
        called on reconfiguration (so drivers should not rely on this
        always being called after stop).

        """
        pass

    def listNodes(self):
#        manager = packet.Manager(self.provider.auth_token)
#        return manager.list_devices(project_id=self.provider.project_id)
        pass

    def start(self, zk_conn):
        """Start this provider

        :param ZooKeeper zk_conn: A ZooKeeper connection object.

        This is called after each configuration change to allow the driver
        to perform initialization tasks and start background threads. The
        ZooKeeper connection object is provided if the Provider needs to
        interact with it.

        """
        pass

    def waitForNodeCleanup(self, server_id, timeout=600):
        """Wait for a node to be cleaned up

        When called, this will be called after
        :py:meth:`~nodepool.driver.Provider.cleanupNode`.

        This method should return after the node has been deleted or
        returned to the pool.

        :param str node_id: The id of the node
        """
        manager = packet.Manager(self.provider.auth_token)

        try:
          for count in iterate_timeout(timeout,
                                       packet.baseapi.Error,
                                       "server %s deletion" % server_id):
              self.cleanupNode(server_id)
              device = manager.get_device(server_id)
        except packet.baseapi.Error as e:  
          if e.args[0] == 'Error 404: Not found':
              return 
          if e.args[0] == 'Error 403: You are not authorized to view this device':
              return 
          else:
              raise e

    def stop(self):
        """Stop this provider

        Before shutdown or reconfiguration, this is called to signal
        to the driver that it will no longer be used.  It should not
        begin any new tasks, but may allow currently running tasks to
        continue.

        """
        pass
