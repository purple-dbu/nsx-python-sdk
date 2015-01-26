"""
Tests for `nsxsdk` module.
"""
import pytest
import vcr
import logging

import nsxsdk.utils
import nsxsdk.logicalswitch as logicalswitch
import nsxsdk.exceptions as nsxexceptions
import credentials

FIXTURES_PATH = "test/fixtures/cassettes/logicalswitch"

myvcr = vcr.VCR(
    cassette_library_dir=FIXTURES_PATH,
    record_mode='once',
    filter_headers=['authorization']
)


def load_dict(file):
    path = "%s/%s" % (FIXTURES_PATH, file)
    return eval(open(path).read())


class TestLogicalSwitch(object):

    @classmethod
    def setup_class(cls):
        pass

    @myvcr.use_cassette('create_ls.yaml')
    def test_create_ls(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        tz_id = lshelper.get_transport_zone_id("tz")
        ls_id = lshelper.create_logical_switch(tz_id, "test_ls")
        assert ls_id == "virtualwire-24"

    @myvcr.use_cassette('create_ls_wrong_tz.yaml')
    def test_create_ls_wrong_tz(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        tz_id = "vdnscope-3"
        lshelper = logicalswitch.LogicalSwitch(http_client)
        pytest.raises(
            nsxexceptions.ResourceNotFound,
            lshelper.create_logical_switch,
            tz_id,
            "test_ls1")

    @myvcr.use_cassette('delete_logical_switch.yaml')
    def test_delete_logical_switch(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        lshelper.delete_logical_switch("virtualwire-24")

    @myvcr.use_cassette('delete_logical_switch_not_found.yaml')
    def test_delete_logical_switch_not_found(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        pytest.raises(
            nsxexceptions.ResourceNotFound,
            lshelper.delete_logical_switch,
            "virtualwire-200")

    @myvcr.use_cassette('get_logical_switches.yaml')
    def test_get_logical_switches(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        logicalswitches = lshelper.get_logical_switches()
        assert logicalswitches == load_dict("logicalswitchesdict")

    @myvcr.use_cassette('get_logical_switches_tz.yaml')
    def test_get_logical_switches_by_tz(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        tz_id = "vdnscope-3"
        logicalswitches = lshelper.get_logical_switches(tz_id)
        assert logicalswitches == load_dict("logicalswitchestzdict")

    @myvcr.use_cassette('get_transport_zone_id.yaml')
    def test_get_transport_zone_id(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        tz_id = lshelper.get_transport_zone_id("tz")
        assert tz_id == "vdnscope-1"

    @myvcr.use_cassette('get_transport_zone_id.yaml')
    def test_get_transport_zone_not_found(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        pytest.raises(
            nsxexceptions.ResourceNotFound,
            lshelper.get_transport_zone_id,
            "TZ")

    @myvcr.use_cassette('get_transport_zone_id.yaml')
    def test_get_transport_zones(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        tz = lshelper.get_transport_zones()
        assert tz == load_dict("transportzonesdict")

    @myvcr.use_cassette('delete_transport_zone.yaml')
    def test_delete_transport_zone(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        lshelper.delete_transport_zone("vdnscope-2")

    @myvcr.use_cassette('delete_transport_zone_not_found.yaml')
    def test_delete_transport_zone_not_found(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        pytest.raises(
            nsxexceptions.ResourceNotFound,
            lshelper.delete_transport_zone,
            "vdnscope-10")

    @myvcr.use_cassette('delete_transport_zone_not_empty.yaml')
    def test_delete_transport_zone_not_empty(self):
        http_client = nsxsdk.utils.NSXClient(
            "pf-nsx-nsxm.rvichery.com:8443",
            credentials.login,
            credentials.password)
        lshelper = logicalswitch.LogicalSwitch(http_client)
        pytest.raises(
            nsxexceptions.IncorrectRequest,
            lshelper.delete_transport_zone,
            "vdnscope-3")

    @classmethod
    def teardown_class(cls):
        pass
