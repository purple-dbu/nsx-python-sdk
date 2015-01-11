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

    def get_transport_zone_id(self, tz_name):
        """Retrieve Id of a transport zone from its name

        :param str tz_name: The name of the transport zone.

        :return: Id of the transport zone
        :rtype: str

        """
        path = LS_PATH + "scopes"
        response = self.http_client.request("GET", path)
        jsondata = json.loads(response.text)
        scopes = jsondata['allScopes']
        for scope in scopes:
            if scope['name'] == tz_name:
                return scope['id']

    def create_logical_switch(self, tz_id, ls_name, cplane_mode=None,
                              tenant_id="default"):
        """Create a new logical switch in the specified transport zone.

        :param str tz_id: Id of the transport zone
        :param str ls_name: Logical switch name

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = LS_PATH + "scopes/" + tz_id + "/virtualwires"
        ls_data = {}
        ls_data['name'] = ls_name
        ls_data['tenantId'] = tenant_id
        if cplane_mode:
            ls_data['controlPlaneMode'] = cplane_mode
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
