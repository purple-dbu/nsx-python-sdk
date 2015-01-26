#!/usr/bin/python

"""
Python script for creating a Logical Switch
"""

import sys
import logging

import nsxsdk.utils as utils
import nsxsdk.logicalswitch as ls


def main():
    ls_name = sys.argv[1]
    client = utils.NSXClient(
        "pf-nsx-nsxm.rvichery.com:8443",
        "admin",
        "xxxxx")
    lshelper = ls.LogicalSwitch(client)
    tz_id = "vdnscope-3"
    logicalswitches = lshelper.get_logical_switches()
    print logicalswitches

# Start program
if __name__ == "__main__":
    # logging.basicConfig(
    #    format='%(asctime)s - %(name)s %(message)s',
    #    level=logging.DEBUG)
    main()
