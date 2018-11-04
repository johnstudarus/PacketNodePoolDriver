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

import logging

import packet

from nodepool.driver import ProviderConfig
from nodepool.driver import ConfigValue
from nodepool.driver import ConfigPool



class PacketProviderConfig(ProviderConfig):

    log = logging.getLogger("nodepool.driver.packet.PacketProviderConfig")

    def __init__(self, driver, provider):
        self.__pools = {}
        super().__init__(provider)

    def getSupportedLabels(self, pool_name=None):
# TODO - pull from Packet API
        labels = set()
        for pool in self.pools.values():
            if not pool_name or (pool.name == pool_name):
                labels.update(pool.labels.keys())
        return labels

    def getSchema(self):
        '''
        Return a voluptuous schema for config validation
        '''
        pass

    def load(self, config):
        '''
        Update this config object from the supplied parsed config
        '''
        # Packet Facility
        self.facility = self.provider.get('facility')
        self.auth_token = self.provider.get('auth_token')
        self.project_id = self.provider.get('project_id')

        for pool in self.provider.get('pools', []):
            pp = ProviderPool()
            pp.name = pool['name']
            pp.provider = self
            self.pools[pp.name] = pp

            for label in pool.get('labels', []):
                pl = ProviderLabel()
                pl.name = label['name']
                pl.pool = pp
                pp.labels[pl.name] = pl
                pl.plan = label.get('plan', None)
                pl.operating_system = label.get('operating_system', None)

                top_label = config.labels[pl.name]
                top_label.pools.append(pp)

    def manage_images(self):
        '''
        Return True if provider manages external images, False otherwise.
        '''
        self.log.info("manage_images")
        return False

    @property
    def pools(self):
        return self.__pools


class ProviderPool(ConfigPool):
    def __init__(self):
        self.name = None
        self.provider = None
        super().__init__()

    def __eq__(self, other):
        print ("ProviderPool compage")
        if isinstance(other, ProviderPool):
            return (super().__eq__(other) and
                    other.name == self.name)
        return False

    def __repr__(self):
        return "<ProviderPool %s>" % self.name

class ProviderLabel(ConfigValue):
    def __init__(self):
        self.name = None
        self.diskimage = None
        self.flavor_name = None
        self.key_name = None
        self.pool = None

    def __eq__(self, other):
        print ("ProviderLabel compage")
        if isinstance(other, ProviderLabel):
            return (other.flavor_name == self.flavor_name and
                    other.diskimage == self.diskimage and
                    other.key_name == self.key_name and
                    other.name == self.name)
        return False

    def __repr__(self):
        return "<ProviderLabel %s>" % self.name


