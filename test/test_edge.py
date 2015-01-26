"""
Tests for `nsxsdk` module.
"""
import pytest
import vcr
import logging

import nsxsdk
from . import credentials

myvcr = vcr.VCR(
    cassette_library_dir='test/fixtures/cassettes/edge',
    record_mode='once',
    filter_headers=['authorization']
)


class TestEdge(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass
