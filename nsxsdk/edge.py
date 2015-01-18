#!/usr/bin/env python
"""Module VMware NSX Edge"""

import json
import logging

import nsxsdk.utils as utils

EDGE_PATH = "/api/4.0/edges/"

log = logging.getLogger(__name__)


class Edge(object):

    """This class provides some functions to deploy and
    configure VMware NSX Edge
    """

    def __init__(self, http_client, edge_id=None):
        self.log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self.http_client = http_client
        if edge_id:
            self.edge_id = edge_id

    @staticmethod
    def _create_basic_configuration(edge_name, datacenter_id,
                                    resourcepool_id, datastore_id,
                                    log_level, host_id,
                                    vmfolder_id):
        """Create a basic edge configuration for both logical router
        and service gateway

            :param str edge_name: Name of the edge to be deployed
            :param str datacenter_id: Id of the datacenter where the
                edge appliance will be deployed
            :param str resourcepool_id: Id of the resourcepool where the edge
                appliance will be deployed
            :param str datastore_id: Id of the datastore where
                the edge appliance will be deployed
            :param str log_level: Edge appliance log level, default is info.
                Other possible values are emergency, alert, critical, error,
                warning, notice, debug.
            :param str host_id: Id of the host where the edge appliance
                will be deployed
            :param str vmfolder_id: Id of the folder where the edge appliance
                will be deployed

            :return: Edge basic configuration
        """
        edge_data = {}
        edge_data['datacenterMoid'] = datacenter_id
        edge_data['name'] = edge_name
        edge_data['vseLogLevel'] = log_level

        appliance_data = {}
        appliance_data['resourcePoolId'] = resourcepool_id
        appliance_data['datastoreId'] = datastore_id
        if host_id:
            appliance_data['hostId'] = host_id
        if vmfolder_id:
            appliance_data['vmFolderId'] = vmfolder_id
        edge_data['appliances']['appliances'].append(appliance_data)
        return edge_data

    def _is_distributed(self):
        """ Check if edge device is a logical router.

        :return: True if it is a logical router and False if
            it is a service gateway.
        :rtype: bool

        """
        path = EDGE_PATH + self.edge_id
        response = self.http_client.request(utils.HTTP_GET, path)
        data = json.loads(response.text)
        if data['type'] == "distributedRouter":
            return True
        return False

    def add_interface(self, interface_type, ip_addr, netmask,
                      network_id, mtu=1500):
        """Attach a new interface to an existing edge device (Service Gateway
        or Logical Router)

        :param str interface_type: Interface type, possible values are internal
            or uplink.
        :param str ip_addr: Interface IP address
        :param str netmask: Interface netmask
        :param str network_id: Id of the network (dvportgroup-id
            or virtualwire-id) on which the new interface need to be connected.
        :param int mtu: Interface MTU, default is 1500.

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        interface_data = {}
        interface_data['addressGroups'] = {}
        interface_data['addressGroups']['addressGroups'] = []
        interface_data['connectedToId'] = network_id
        interface_data['mtu'] = mtu
        interface_data['type'] = interface_type

        interface_addressgroup = {}
        interface_addressgroup['primaryAddress'] = ip_addr
        interface_addressgroup['netmask'] = netmask
        interface_data['addressGroups'][
            'addressGroups'].append(interface_addressgroup)

        path = EDGE_PATH + self.edge_id
        if self._is_distributed():
            path = path + "/interfaces/?action=patch"
        else:
            path = path + "/vnics/?action=patch"

        data = json.dumps(interface_data)
        response = self.http_client.request(utils.HTTP_POST, path, data)
        return response

    @staticmethod
    def get_edge_id(http_client, edge_name):
        """Retrieve the ID of a NSX Edge from its name

        :param NSXClient http_client: NSX client used to
            retrieve edge Id.
        :param str edge_name: The name of the edge to retrieve.

        :return: Id of the edge
        :rtype: str

        """
        path = EDGE_PATH
        response = http_client.request(utils.HTTP_GET, path)
        jsondata = json.loads(response.text)
        edges = jsondata['edgePage']['data']
        for edge in edges:
            if edge['name'] == edge_name:
                return edge['objectId']

    def get_id(self):
        """Return NSX Edge Id.

        :return: Id of the edge
        :rtype: str

        """
        if self.edge_id:
            return self.edge_id
        else:
            raise Exception

    def delete(self):
        """Delete a NSX Edge
 that will be deleted

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = EDGE_PATH + self.edge_id
        response = self.http_client.request(utils.HTTP_DELETE, path)
        return response

    def configure_global_routing(self, router_id,
                                 ecmp=False, log=False, log_level="info"):
        """Set NSX Edge global routing configuration.
 to be configured
        :param str router_id: Unique router id
        :param bool ecmp: enable ECMP feature if True,
            defaults to False.
        :param bool log: enable logging feature if True,
            defaults to False.
        :param str log_level: Routing feature log level, default is info. Other
            possible values are emergency, alert, critical, error, warning,
            notice, debug.

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + self.edge_id + "/routing/config/global"
        global_data = {}
        global_data['routerId'] = router_id
        if ecmp:
            global_data['ecmp'] = ecmp
        if log:
            global_data['logging'] = {}
            global_data['logging']['enabled'] = "true"
            global_data['logging']['logLevel'] = log_level
        data = json.dumps(global_data)
        response = self.http_client.request(utils.HTTP_PUT, path, data)
        return response

    def add_bgp_peer(self, peer_ip, peer_as, weight=None,
                     holddown_timer=None, keepalive_timer=None):
        """Add a bgp remote peer to an existing NSX Edge.
 to be reconfigured
        :param str peer_ip: BGP remote peer IP address
        :param int peer_as: BGP remote peer AS number
        :param int weight: weight apply to routes learned from this peer
        :param int holddown_timer: holddown timer of the BGP session
        :param int keepalive_timer: keepalive timer of the BGP session

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + self.edge_id + "/routing/config/bgp"
        response = self.http_client.request(utils.HTTP_GET, path)
        data = json.loads(response.text)
        peer_data = {}
        peer_data['ipAddress'] = peer_ip
        peer_data['remoteAS'] = str(peer_as)
        if weight is not None:
            peer_data['weight'] = str(weight)
        if holddown_timer is not None:
            peer_data['holdDownTimer'] = str(holddown_timer)
        if keepalive_timer is not None:
            peer_data['keepAliveTimer'] = str(keepalive_timer)
        data['bgpNeighbours']['bgpNeighbours'].append(peer_data)
        response = self.http_client.request(
            utils.HTTP_PUT,
            path,
            json.dumps(data))
        return response

    def configure_bgp(self, local_as, graceful_restart=False,
                      default_originate=False):
        """Configure BGP basic parameters such as Local AS, graceful restart
        and default originate.
 to be reconfigured
        :param int local_as: BGP local AS
        :param bool graceful_restart: enable graceful restart feature if True,
            defaults to False.
        :param bool default_originate: enable default originate
            feature if True, defaults to False.

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + self.edge_id + "/routing/config/bgp"
        bgp_data = {}
        bgp_data['enabled'] = "true"
        bgp_data['localAS'] = str(local_as)
        if graceful_restart:
            bgp_data['gracefulRestart'] = "true"
        if default_originate:
            bgp_data['defaultOriginate'] = "true"
        data = json.dumps(bgp_data)
        response = self.http_client.request(utils.HTTP_PUT, path, data)
        return response

    def configure_syslog(self, ip_address, protocol):
        """Configure edge to send log to remote syslog
 to be reconfigured
        :param str ip_address: IP address of the remote syslog
        :param str protocol: Syslog transport protocol ("udp" or "tcp")

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + self.edge_id + "/syslog/config"
        syslog_data = {}
        syslog_data['featureType'] = "syslog"
        syslog_data['enabled'] = "true"
        syslog_data['protocol'] = protocol
        syslog_data['serverAddresses'] = {}
        syslog_data['serverAddresses']['type'] = "IpAddressesDto"
        syslog_data['serverAddresses']['ipAddress'] = []
        syslog_data['serverAddresses']['ipAddress'].append(ip_address)
        data = json.dumps(syslog_data)
        response = self.http_client.request(utils.HTTP_PUT, path, data)
        return response

    def configure_ha(self):
        """Configure NSX Edge in HA mode.
 to be reconfigured

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + self.edge_id + "/highavailability/config"
        ha_data = {}
        ha_data['featureType'] = "highavailability_4.0"
        ha_data['enabled'] = "true"
        data = json.dumps(ha_data)
        response = self.http_client.request(utils.HTTP_PUT, path, data)
        return response


class LogicalRouter(Edge):

    def __init__(self, http_client):
        Edge.__init__(self, http_client)

    def create(self, edge_name, datacenter_id, resourcepool_id,
               datastore_id, mgmt_portgroup_id, mgmt_ipaddr,
               mgmt_netmask, log_level="info", host_id=None,
               vmfolder_id=None):
        """Deploy a NSX Edge Logical Router with a basic configuration

        :param str edge_name: Name of the edge to be deployed
        :param str datacenter_id: Id of the datacenter where the edge appliance
            will be deployed
        :param str resourcepool_id: Id of the resourcepool where the edge
            appliance will be deployed
        :param str datastore_id: Id of the datastore where the edge appliance
            will be deployed
        :param str mgmt_portgroup_id: Portgroup Id on which management
            interface will be connected
        :param str mgmt_ipaddr: Management interface IP address
        :param str mgmt_netmask: Management interface netmask
        :param str log_level: Edge appliance log level, default is info.
            Other possible values are emergency, alert, critical, error,
            warning, notice, debug.
        :param str host_id: Id of the host where the edge appliance
            will be deployed
        :param str vmfolder_id: Id of the folder where the edge appliance
            will be deployed

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH
        edge_data = Edge._create_basic_configuration(edge_name,
                                                     datacenter_id,
                                                     resourcepool_id,
                                                     datastore_id,
                                                     host_id,
                                                     vmfolder_id,
                                                     log_level)
        edge_data['type'] = "distributedRouter"
        edge_data['mgmtInterface'] = {}
        edge_data['mgmtInterface']['connectedToId'] = mgmt_portgroup_id
        edge_data['mgmtInterface']['addressGroups'] = {}
        edge_data['mgmtInterface']['addressGroups']['addressGroups'] = []
        mgmt_configuration = {}
        mgmt_configuration['primaryAddress'] = mgmt_ipaddr
        mgmt_configuration['subnetMask'] = mgmt_netmask
        edge_data['mgmtInterface']['addressGroups'][
            'addressGroups'].append(mgmt_configuration)
        data = json.dumps(edge_data)
        response = self.http_client.request(utils.HTTP_POST, path, data)
        return response

    def add_interface(self, interface_type, ip_addr, netmask,
                      network_id, mtu=1500):
        """Attach a new interface to an existing edge device

        :param str interface_type: Interface type, possible values are internal
            or uplink.
        :param str ip_addr: Interface IP address
        :param str netmask: Interface netmask
        :param str network_id: Id of the network (dvportgroup-id
            or virtualwire-id) on which the new interface need to be connected.
        :param int mtu: Interface MTU, default is 1500.

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        interface_data = {}
        interface_data['addressGroups'] = {}
        interface_data['addressGroups']['addressGroups'] = []
        interface_data['connectedToId'] = network_id
        interface_data['mtu'] = mtu
        interface_data['type'] = interface_type

        interface_addressgroup = {}
        interface_addressgroup['primaryAddress'] = ip_addr
        interface_addressgroup['netmask'] = netmask
        interface_data['addressGroups'][
            'addressGroups'].append(interface_addressgroup)

        path = EDGE_PATH + self.edge_id + "/interfaces/?action=patch"

        data = json.dumps(interface_data)
        response = self.http_client.request(utils.HTTP_POST, path, data)
        return response


class ServiceGateway(Edge):

    def __init__(self, http_client, edge_id=None):
        Edge.__init__(self, http_client, edge_id)

    def create(self, edge_name, appliance_size,
               datacenter_id, resourcepool_id,
               datastore_id, log_level="info", host_id=None,
               vmfolder_id=None):
        """Deploy a NSX Edge Service Gateway with a basic configuration

        :param str edge_name: Name of the edge to be deployed
        :param str appliance_size: Edge size, could be compact, large,
            quadlarge or xlarge
        :param str datacenter_id: Id of the datacenter where the edge appliance
            will be deployed
        :param str resourcepool_id: Id of the resourcepool where the edge
            appliance will be deployed
        :param str datastore_id: Id of the datastore where the edge appliance
            will be deployed
        :param str log_level: Edge appliance log level, default is info.
            Other possible values are emergency, alert, critical, error,
            warning, notice, debug.
        :param str host_id: Id of the host where the edge appliance
            will be deployed
        :param str vmfolder_id: Id of the folder where the edge appliance
            will be deployed

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH
        edge_data = Edge._create_basic_configuration(edge_name,
                                                     datacenter_id,
                                                     resourcepool_id,
                                                     datastore_id,
                                                     host_id,
                                                     vmfolder_id,
                                                     log_level)
        edge_data['appliances']['applianceSize'] = appliance_size
        data = json.dumps(edge_data)
        response = self.http_client.request(utils.HTTP_POST, path, data)
        return response

    def add_interface(self, interface_type, ip_addr, netmask,
                      network_id, mtu=1500):
        """Attach a new interface to an existing edge device

        :param str interface_type: Interface type, possible values are internal
            or uplink.
        :param str ip_addr: Interface IP address
        :param str netmask: Interface netmask
        :param str network_id: Id of the network (dvportgroup-id
            or virtualwire-id) on which the new interface need to be connected.
        :param int mtu: Interface MTU, default is 1500.

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        interface_data = {}
        interface_data['addressGroups'] = {}
        interface_data['addressGroups']['addressGroups'] = []
        interface_data['connectedToId'] = network_id
        interface_data['mtu'] = mtu
        interface_data['type'] = interface_type

        interface_addressgroup = {}
        interface_addressgroup['primaryAddress'] = ip_addr
        interface_addressgroup['netmask'] = netmask
        interface_data['addressGroups'][
            'addressGroups'].append(interface_addressgroup)

        path = EDGE_PATH + self.edge_id + "/vnics/?action=patch"

        data = json.dumps(interface_data)
        response = self.http_client.request(utils.HTTP_POST, path, data)
        return response
