
Nodepool is the underlying process within Zuul that handles the provisioning of compute resources for CI jobs. Primarily, Nodepool managed OpenStack virtual machines but does have the ability, through a driver interface, to support alternate compute sources. This repo is a proof of concept showcasing a Nodepool driver written to support management of bare metal hosts via the Packet Host API.

More information about the Nodeppol driver interface:

https://specs.openstack.org/openstack-infra/infra-specs/specs/nodepool-drivers.html 

More information about the Packet Host Python library and the underlying Packet Host REST API:

https://pypi.org/project/packet-python/
https://www.packet.com/developers/api/

A Packet Host API key (account) is required and must be configured in the nodepool.yaml file. All the attributes of the Packet bare metal cloud should be defined in nodepool.yaml. There is no need to provide a clouds.yaml file.