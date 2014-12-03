#!/usr/bin/env python
"""Module VMware NSX Edge"""

import json

EDGE_PATH = "/api/4.0/edges/"


class EdgeSDK(object):

    """This class provides some functions to deploy and
    configure VMware NSX Edge
    """

    def __init__(self, http_client):
        self.http_client = http_client

    def delete_edge(self, edge_id):
        """Delete a NSX Edge

        :param str edge_id: Id of the edge that will be deleted

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = EDGE_PATH + edge_id
        response = self.http_client.request("DELETE", path)
        return response

    def get_edge_id(self, edge_name):
        """Retrieve the ID of a NSX Edge from its name

        :param str edge_name: The name of the edge to get.

        :return: Id of the edge
        :rtype: str

        """
        path = EDGE_PATH
        response = self.http_client.request("GET", path)
        jsondata = json.loads(response.text)
        edges = jsondata['edgePage']['data']
        for edge in edges:
            if edge['name'] == edge_name:
                return edge['objectId']

    def configure_global_routing(self, edge_id, router_id,
                                 ecmp=False, log=False):
        """Set NSX Edge global routing configuration.

        :param str edge_id: Id of the edge to be configured
        :param str router_id: Unique router id
        :param bool ecmp: enable ECMP feature if True,
            defaults to False.
        :param bool log: enable logging feature if True,
            defaults to False.

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + edge_id + "/routing/config/global"
        global_data = {}
        global_data['routerId'] = router_id
        if ecmp:
            global_data['ecmp'] = ecmp
        if log:
            global_data['logging'] = {}
            global_data['logging']['enabled'] = "true"
            global_data['logging']['logLevel'] = "info"
        data = json.dumps(global_data)
        response = self.http_client.request("PUT", path, data)
        return response

    def add_bgp_peer(self, edge_id, peer_ip, peer_as, weight=None,
                     holddown_timer=None, keepalive_timer=None):
        """Add a bgp remote peer to an existing NSX Edge.

        :param str edge_id: Id of the edge to be reconfigured
        :param str peer_ip: BGP remote peer IP address
        :param int peer_as: BGP remote peer AS number
        :param int weight: weight apply to routes learned from this peer
        :param int holddown_timer: holddown timer of the BGP session
        :param int keepalive_timer: keepalive timer of the BGP session

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + edge_id + "/routing/config/bgp"
        response = self.http_client.request("GET", path)
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
        response = self.http_client.request("PUT", path, json.dumps(data))
        return response

    def configure_bgp(self, edge_id, local_as, graceful_restart=False,
                      default_originate=False):
        """Configure BGP basic parameters such as Local AS, graceful restart
        and default originate.

        :param str edge_id: Id of the edge to be reconfigured
        :param int local_as: BGP local AS
        :param bool graceful_restart: enable graceful restart feature if True,
            defaults to False.
        :param bool default_originate: enable default originate
            feature if True, defaults to False.

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + edge_id + "/routing/config/bgp"
        bgp_data = {}
        bgp_data['enabled'] = "true"
        bgp_data['localAS'] = str(local_as)
        if graceful_restart:
            bgp_data['gracefulRestart'] = "true"
        if default_originate:
            bgp_data['defaultOriginate'] = "true"
        data = json.dumps(bgp_data)
        response = self.http_client.request("PUT", path, data)
        return response

    def configure_syslog(self, edge_id, ip_address, protocol):
        """Configure edge to send log to remote syslog

        :param str edge_id: Id of the edge to be reconfigured
        :param str ip_address: IP address of the remote syslog
        :param str protocol: Syslog transport protocol ("udp" or "tcp")

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + edge_id + "/syslog/config"
        syslog_data = {}
        syslog_data['featureType'] = "syslog"
        syslog_data['enabled'] = "true"
        syslog_data['protocol'] = protocol
        syslog_data['serverAddresses'] = {}
        syslog_data['serverAddresses']['type'] = "IpAddressesDto"
        syslog_data['serverAddresses']['ipAddress'] = []
        syslog_data['serverAddresses']['ipAddress'].append(ip_address)
        data = json.dumps(syslog_data)
        response = self.http_client.request("PUT", path, data)
        return response

    def deploy_edge(self, edge_name):
        """Deploy a NSX Edge with a basic configuration

        :param str edge_name: Name of the edge to be deployed

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH
        edge_data = {}
        edge_data['datacenterMoid'] = "datacenter-2"
        edge_data['name'] = edge_name
        edge_data['vseLogLevel'] = "emergency"
        edge_data['appliances'] = {}
        edge_data['appliances']['applianceSize'] = "large"
        edge_data['appliances']['appliances'] = []
        appliance_data = {}
        appliance_data['resourcePoolId'] = "domain-c9"
        appliance_data['datastoreId'] = "datastore-24"
        appliance_data['hostId'] = "host-32"
        appliance_data['vmFolderId'] = "group-v3"
        edge_data['appliances']['appliances'].append(appliance_data)
        data = json.dumps(edge_data)
        response = self.http_client.request("POST", path, data)
        return response

    def configure_ha(self, edge_id):
        """Configure NSX Edge in HA mode.

        :param str edge_id: Id of the edge to be reconfigured

        :return: response to the HTTP request
        :rtype: request.Response

        """
        path = EDGE_PATH + edge_id + "/highavailability/config"
        ha_data = {}
        ha_data['featureType'] = "highavailability_4.0"
        ha_data['enabled'] = "true"
        data = json.dumps(ha_data)
        response = self.http_client.request("PUT", path, data)
        return response
