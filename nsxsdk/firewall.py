#!/usr/bin/env python
"""Module VMware NSX Distributed Firewall"""

import json

DFW_PATH = "/api/4.0/firewall/"


class FirewallSDK(object):

    """This class provides some functions to configure
    the distributed firewall
    """

    def __init__(self, http_client):
        self.http_client = http_client

    def get_firewall_section_id(self, section_name):
        """Retrieve the ID of a firewall section from its name

        :param str section_name: The name of the firewall section to get.

        :return: Id of the firewall section
        :rtype: str

        """
        path = DFW_PATH + "globalroot-0/config"
        response = self.http_client.request("GET", path)
        jsondata = json.loads(response.text)
        sections = jsondata['layer3Sections']['layer3Sections']
        for section in sections:
            if section['name'] == section_name:
                return section['id']

    def add_firewall_section(self, section_name):
        """Retrieve the ID of a firewall section from its name

        :param str section_name: Name of the new section

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = DFW_PATH + "globalroot-0/config/layer3sections"
        section_data = {}
        section_data['name'] = section_name
        section_data['rules'] = []
        data = json.dumps(section_data)
        response = self.http_client.request("POST", path, data)
        return response

    def delete_firewall_section(self, section_id):
        """Delete a firewall section

        :param int section_id: Id of the firewall section that will be deleted

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = DFW_PATH + "globalroot-0/config/layer3sections/" + \
            str(section_id)
        response = self.http_client.request("DELETE", path)
        return response

    def add_firewall_rule(self, section_id, source_ip,
                          destination_ip, action):
        """Add a firewall rule in an existing section

        :param int section_id: Id of the section
        :param str source_ip: Source IP address
        :param str destination_ip: Destination IP address
        :param str action: Firewall rule's action ("allow", "deny" or "reject")

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = DFW_PATH + "globalroot-0/config/layer3sections/" + \
            str(section_id)
        response = self.http_client.request("GET", path)
        headers = {'If-Match': response.headers['ETag']}

        path = DFW_PATH + "globalroot-0/config/layer3sections/" + \
            str(section_id) + "/rules"
        rule_data = {}
        rule_data['action'] = action
        rule_data['appliedToList'] = {}
        rule_data['appliedToList']['appliedToList'] = []
        rule_data['sources'] = {}
        rule_data['sources']['sourceList'] = []
        rule_data['sources']['excluded'] = "false"
        rule_data['destinations'] = {}
        rule_data['destinations']['excluded'] = "false"
        rule_data['destinations']['destinationList'] = []
        rule_data['services'] = {}
        rule_data['services']['serviceList'] = []
        rule_data['type'] = "LAYER3"

        appliedto_data = {}
        appliedto_data['name'] = "DISTRIBUTED_FIREWALL"
        appliedto_data['value'] = "DISTRIBUTED_FIREWALL"
        appliedto_data['type'] = "DISTRIBUTED_FIREWALL"
        rule_data['appliedToList']['appliedToList'].append(appliedto_data)

        source_data = {}
        source_data['value'] = source_ip
        source_data['type'] = "Ipv4Address"
        source_data['isValid'] = "true"
        rule_data['sources']['sourceList'].append(source_data)

        destination_data = {}
        destination_data['value'] = destination_ip
        destination_data['type'] = "Ipv4Address"
        destination_data['isValid'] = "true"
        rule_data['destinations']['destinationList'].append(destination_data)

        data = json.dumps(rule_data)
        response = self.http_client.request("POST", path, data, headers)
        return response
