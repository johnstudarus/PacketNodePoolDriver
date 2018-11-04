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

from nodepool.driver import Driver
from nodepool.driver.packet.config import PacketProviderConfig
from nodepool.driver.packet.provider import PacketProvider


class PacketDriver(Driver):
#    def __init__(self):
#        super().__init__()
#        self.reset()

    def getProviderConfig(self, provider):
        return PacketProviderConfig(self, provider)

    def getProvider(self, provider_config, use_taskmanager):
        return PacketProvider(provider_config, use_taskmanager)

class PacketProviderNotification(object):
    def nodeDeletedNotification(self, node):
# delete 
        pass

