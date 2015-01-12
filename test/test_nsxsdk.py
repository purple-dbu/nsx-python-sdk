"""
Tests for `nsxsdk` module.
"""
import pytest
import vcr
import logging

import nsxsdk
import credentials


class TestNsxsdk(object):

    @classmethod
    def setup_class(cls):
        pass

    @vcr.use_cassette('fixtures/nsx_cassettes/edges.yaml')
    def test_get_edge_id(self):
        http_client = nsxsdk.utils.NSXClient(
            "nsxm.rvichery.com",
            credentials.login,
            credentials.password)
        response = nsxsdk.edge.Edge.get_edge_id(http_client, "NSX_Edge_Test")
        assert response == "edge-2"

    @classmethod
    def teardown_class(cls):
        pass
