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

class ConstructCodeTabUnitTests(BlockHeaderTestCase):
    """Collects tests on construct_code_tab"""

    def setUp(self):
        self.construct_header()
        self.contents = 'qqq'

    def test_contents_assignment(self):
        """Ensures contents is inserted correctly"""
        output = '<div class="code-tab">qqq</div>'
        self.assertEqual(
            self.header.construct_code_tab(self.contents),
            output,
        )

    def test_active_assignment(self):
        """Ensure active is properly assigned"""
        output = '<div class="code-tab active">qqq</div>'
        self.assertEqual(
            self.header.construct_code_tab(self.contents, True),
            output,
        )
