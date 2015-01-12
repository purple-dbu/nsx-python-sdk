#!/usr/bin/env python
"""Module VMware NSX Logical Switches"""

import json
import nsxsdk.utils as utils

LS_PATH = "/api/2.0/vdn/"


class LogicalSwitch(object):

    """This class provides some functions to configure
    logical switches
    """

    def __init__(self, http_client, ls_id=None):
        self.http_client = http_client
        if ls_id:
            self.ls_id = ls_id

    @staticmethod
    def get_transport_zone_id(http_client, tz_name):
        """Retrieve Id of a transport zone from its name

        :param NSXClient http_client: NSX client used to
            retrieve transport zone Id.
        :param str tz_name: The name of the transport zone.

        :return: Id of the transport zone
        :rtype: str

        """
        path = LS_PATH + "scopes"
        response = http_client.request(utils.HTTP_GET, path)
        jsondata = json.loads(response.text)
        scopes = jsondata['allScopes']
        for scope in scopes:
            if scope['name'] == tz_name:
                return scope['id']

    def create(self, tz_id, ls_name, cplane_mode=None,
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
        response = self.http_client.request(utils.HTTP_POST, path, data)
        return response

    def delete(self):
        """Delete a logical switch

        :param str ls_id: Id of the logical switch that will be deleted

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = LS_PATH + "virtualwires/" + self.ls_id
        response = self.http_client.request(utils.HTTP_DELETE, path)
        return response
