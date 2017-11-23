# pylint: disable=w0201
"""This file collects tests for BlockHeader"""

# from collections import defaultdict
import unittest
# from mock import MagicMock, patch

from wotw_highlighter import BlockHeader

class BlockHeaderTestCase(unittest.TestCase):
    """Collects common items and defaults across test cases"""

    def construct_header(self):
        """Constructs a basic header using only the defaults"""
        self.header = BlockHeader()

class ConstructorUnitTests(BlockHeaderTestCase):
    """Collects tests on the ctor"""

    def test_options(self):
        """TODO: better tests"""
        header = BlockHeader()
        self.assertTrue(header.linenos)
