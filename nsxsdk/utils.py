#!/usr/bin/env python
"""Utils module for NSX SDK"""

import requests
import logging
import json

import nsxsdk.exceptions as exceptions

HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_DELETE = "DELETE"

LOGGER = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings()


class NSXClient(object):

    """NSXClient have the following properties:

    Attributes:
        base_url: A string representing the base url.
        login: A string representing login.
        password: A string representing password
        session: Session parameters for REST API calls
    """

    def __init__(self, hostname, login, password):
        self.logger = logging.getLogger(
            __name__ +
            "." +
            self.__class__.__name__)
        self.base_url = "https://" + hostname
        self.login = login
        self.password = password
        self.session = self._initialize_session()
        self.logger.info("NSXClient created")
        self.logger.debug(
            "url=%s login=%s password=%s",
            self.base_url,
            self.login,
            self.password)

    def _initialize_session(self):
        """Initialize HTTP session with a basic configuration to consume
        JSON REST API:
            - Disable SSL verification
            - Set HTTP headers to application/json
            - Set authorization header

        Returns:
            Session: initiazed session

        """
        session = requests.Session()
        session.auth = (self.login, self.password)
        session.verify = False
        session.headers.update({'Accept': 'application/json'})
        session.headers.update({'Content-type': 'application/json'})
        return session

    def request(self, method, path, body=None, headers=None):
        """Generic method to consume REST API Webservices

        :param method: HTTP method
        :param path: API resource path
        :param body: HTTP request body
        :param headers: Extra headers

        :return: return description
        :rtype: the return type description

        """
        url = self.base_url + path
        self.logger.info("Request: %s %s", method, url)
        if headers:
            self.logger.debug("Request headers: %s", headers)
        if body:
            self.logger.debug("Request body: %s", body)
        response = None
        try:
            response = self.session.request(
                method,
                url,
                data=body,
                headers=headers)
            response.raise_for_status()
            self.logger.info(
                "Response: %s %s",
                response.status_code,
                response.reason)
            return response
        except requests.exceptions.RequestException as exception:
            self.logger.critical("%s %s - %s", method, url, exception)
            if response.status_code == 404:
                raise exceptions.ResourceNotFound(url)
            if response.status_code == 400:
                responsedata = json.loads(response.text)
                raise exceptions.IncorrectRequest(responsedata['details'])
        finally:
            if response is not None:
                self.logger.debug("Response headers: %s", response.headers)
                self.logger.debug("Response body: %s", response.text)
