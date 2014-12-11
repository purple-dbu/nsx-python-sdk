#!/usr/bin/env python
"""Module VMware NSX Logical Switches"""

import json

LS_PATH = "/api/2.0/vdn/"


class LogicalSwitchesSDK(object):

    """This class provides some functions to configure
    logical switches
    """

    def __init__(self, http_client):
        self.http_client = http_client

    def get_network_scope_id(self, scope_name):
        """Retrieve the ID of a network scope from its name

        :param str scope_name: The name of the network scope to get.

        :return: Id of the network scope
        :rtype: str

        """
        path = LS_PATH + "scopes"
        response = self.http_client.request("GET", path)
        jsondata = json.loads(response.text)
        scopes = jsondata['allScopes']
        for scope in scopes:
            if scope['name'] == scope_name:
                return scope['id']

    def add_logical_switch(self, scope_id, ls_name):
        """Create a new logical switch on the specified network scope.

        :param str scope_id: Id of the network scope (Transport Zone)
        :param str ls_name: Logical switch name

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = LS_PATH + "scopes/" + scope_id + "/virtualwires"
        ls_data = {}
        ls_data['name'] = ls_name
        ls_data['tenantId'] = "virtual wire tenant"
        data = json.dumps(ls_data)
        response = self.http_client.request("POST", path, data)
        return response

    def delete_logical_switch(self, ls_id):
        """Delete a logical switch

        :param str ls_id: Id of the logical switch that will be deleted

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = LS_PATH + "virtualwires/" + ls_id
        response = self.http_client.request("DELETE", path)
        return response
