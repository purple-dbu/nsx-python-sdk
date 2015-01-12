#!/usr/bin/env python
"""Module VMware NSX Security Group"""

import nsxsdk.utils as utils

SG_PATH = "/api/2.0/services/securitygroup/"


class SecurityGroup(object):

    """This class provides some functions to interact with Security Groups
    """

    def __init__(self, http_client, securitygroup_id=None):
        self.http_client = http_client
        if securitygroup_id:
            self.securitygroup_id = securitygroup_id

    def delete_member(self, member_id):
        """Remove a member from an existing security group.

        :param str member_id: Id of the member to remove

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = SG_PATH + self.securitygroup_id + "/members/" + member_id
        response = self.http_client.request(utils.HTTP_DELETE, path)
        return response

    def add_member(self, member_id):
        """Add a member in an existing security group.

        :param str member_id: Id of the member to add

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = SG_PATH + self.securitygroup_id + "/members/" + member_id
        response = self.http_client.request(utils.HTTP_PUT, path)
        return response

    def delete(self, force=False):
        """Delete a security group.

        :param bool force: Force security group deletion, default is False.

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = SG_PATH + self.securitygroup_id + "?force=" + str(force)
        response = self.http_client.request(utils.HTTP_DELETE, path)
        return response

    def get_members(self):
        """Retrieve members of an existing security group.

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        path = SG_PATH + self.securitygroup_id
        response = self.http_client.request(utils.HTTP_GET, path)
        return response

    def get_id(self):
        """Return Security Group ID.

        :return: response to the HTTP request
        :rtype: requests.Response

        """
        if self.securitygroup_id:
            return self.securitygroup_id
        else:
            raise Exception
