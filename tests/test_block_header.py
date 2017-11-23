# pylint: disable=w0201
"""This file collects tests for BlockHeader"""

# from collections import defaultdict
import unittest
from mock import patch

from wotw_highlighter import BlockHeader

class BlockHeaderTestCase(unittest.TestCase):
    """Collects common items and defaults across test cases"""

    def wipe_header(self):
        """Nukes the constructed header"""
        del self.header

    def construct_header(self):
        """Constructs a basic header using only the defaults"""
        self.header = BlockHeader()
        self.addCleanup(self.wipe_header)

    def construct_with_mock_statics(self):
        """Constructs a basic header with static methods mocked"""
        construct_patcher = patch.object(BlockHeader, 'construct_code_tab')
        self.mock_construct = construct_patcher.start()
        self.addCleanup(construct_patcher.stop)
        self.construct_header()

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

class RenderVcsBranchTabUnitTestss(BlockHeaderTestCase):
    """Collects tests on render_vcs_branch"""

    def setUp(self):
        self.construct_with_mock_statics()
        self.branch = 'qqq'

    def test_with_branch(self):
        """Tests rendering with a branch"""
        self.header.vcs_branch = self.branch
        self.header.render_vcs_branch_tab()
        self.mock_construct.assert_called_with(self.branch)

    def test_without_branch(self):
        """Tests rendering without a branch"""
        self.assertEqual(
            self.header.render_vcs_branch_tab(),
            ''
        )
