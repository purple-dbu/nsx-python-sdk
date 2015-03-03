#!/usr/bin/env python
"""Module VMware NSX Logical Switches"""

import json
import logging

import nsxsdk.utils as utils
import nsxsdk.exceptions as exceptions

LS_PATH = "/api/2.0/vdn/"

LOGGER = logging.getLogger(__name__)


class LogicalSwitch(object):

    """This class provides some functions to configure
    logical switches
    """

    def __init__(self, http_client, ls_id=None):
        self.logger = logging.getLogger(
            __name__ +
            "." +
            self.__class__.__name__)
        self.http_client = http_client
        if ls_id:
            self.ls_id = ls_id

    def get_transport_zones(self):
        """Retrieve all transport zones

        :return: List of transport zones
        :rtype: dict

        """
        path = LS_PATH + "scopes"
        response = self.http_client.request(utils.HTTP_GET, path)
        jsondata = json.loads(response.text)
        transportzones = jsondata['allScopes']
        return transportzones

    def get_transport_zone_id(self, tz_name):
        """Retrieve Id of a transport zone from its name

        :param str tz_name: The name of the transport zone.

        :return: Id of the transport zone
        :rtype: str

        :raises nsxsdk.exceptions.ResourceNotFound: If transport
            zone "tz_name" does not exist.

        """
        transportzones = self.get_transport_zones()
        for transportzone in transportzones:
            if transportzone['name'] == tz_name:
                return transportzone['id']
        raise exceptions.ResourceNotFound(tz_name)

    def delete_transport_zone(self, tz_id):
        """Delete a transport zone

        :param str tz_id: Id of the transport zone that will be deleted

        """
        path = LS_PATH + "scopes/" + tz_id
        self.http_client.request(utils.HTTP_DELETE, path)

    def create_logical_switch(self, tz_id, ls_name, cplane_mode=None,
                              tenant_id="default"):
        """Create a new logical switch on the specified transport zone.

        :param str tz_id: Id of the transport zone
        :param str ls_name: Logical switch name
        :param str cplane_mode: Default is Transport Zone control plane mode
        :param str tenant_id: Logical Switch tenant id/name

        :return: Id of the logical switch
        :rtype: str

        """
        path = LS_PATH + "scopes/" + tz_id + "/virtualwires"
        ls_data = {}
        ls_data['name'] = ls_name
        ls_data['tenantId'] = tenant_id
        if cplane_mode:
            ls_data['controlPlaneMode'] = cplane_mode
        data = json.dumps(ls_data)
        response = self.http_client.request(utils.HTTP_POST, path, data)
        return response.text

    def delete_logical_switch(self, ls_id):
        """Delete a logical switch.

        :param str ls_id: Id of the logical switch that will be deleted

        """
        path = LS_PATH + "virtualwires/" + ls_id
        self.http_client.request(utils.HTTP_DELETE, path)

    def get_logical_switches(self, tz_id=None):
        """Retrieve all logical switches or retrieve all logical switches
        on the specified transport zone.

        :param str tz_id: (Optional) Id of the Transport Zone

        :return: List of logical switches
        :rtype: dict

        """
        if tz_id:
            path = LS_PATH + "scopes/" + tz_id + "/virtualwires"
        else:
            path = LS_PATH + "virtualwires"
        response = self.http_client.request(utils.HTTP_GET, path)
        jsondata = json.loads(response.text)
        logicalswitches = jsondata['dataPage']['data']
        return logicalswitches
