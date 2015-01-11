#!/usr/bin/env python
"""Utils module for NSX SDK"""

import requests
import json
import sys


class HTTPClient(object):

    """HTTPClient have the following properties:

    Attributes:
        base_url: A string representing the base url.
        login: A string representing login.
        password: A string representing password
        session: Session parameters for REST API calls
    """

    def __init__(self, hostname, login, password):
        self.base_url = "https://" + hostname
        self.login = login
        self.password = password
        self.session = self._initialize_session()

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
        print "Method: " + method + ", URL: " + url

        if body is not None:
            print json.dumps(
                json.loads(body),
                sort_keys=True,
                indent=4,
                separators=(
                    ',',
                    ': '))

        try:
            response = self.session.request(
                method,
                url,
                data=body,
                headers=headers)
            print "Status code: " + str(response.status_code)
            return response
        except requests.exceptions.HTTPError as exception:
            print "HTTPError: " + exception
            sys.exit(1)
        except requests.exceptions.RequestException as exception:
            print exception
            sys.exit(1)
