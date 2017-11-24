# pylint: disable=w0201
"""This file collects tests for BlockHeader"""

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
        validate_patcher = patch.object(BlockHeader, 'validate')
        validate_patcher.start()
        self.header = BlockHeader(title='qqq.qqq')
        validate_patcher.stop()
        self.addCleanup(self.wipe_header)

    def construct_with_mock_statics(self):
        """Constructs a basic header with static methods mocked"""
        construct_patcher = patch.object(BlockHeader, 'construct_code_tab')
        self.mock_construct = construct_patcher.start()
        self.addCleanup(construct_patcher.stop)
        self.construct_header()


class ValidateUnittests(BlockHeaderTestCase):
    """Collects tests on validate"""

    def setUp(self):
        self.construct_header()

    def test_no_title_check(self):
        """Ensures an error is thrown when no title is used"""
        self.header.from_file = None
        self.header.title = None
        with self.assertRaises(ValueError):
            self.header.validate()

    def test_any_title_check(self):
        """Ensures an okay passes through"""
        self.assertIsNone(self.header.validate())


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
    """Collects tests on render_vcs_branch_tab"""

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
            BlockHeader.RENDER_AN_OPTION_NOT_INCLUDED
        )


class RenderTitleTabUnitTests(BlockHeaderTestCase):
    """Collects tests on render_title_tab"""

    def setUp(self):
        self.construct_with_mock_statics()

    def test_with_title(self):
        """Tests rendering with a title"""
        self.header.title = 'title'
        self.header.from_file = None
        self.header.render_title_tab()
        self.mock_construct.assert_called_once_with('title', True)

    def test_with_from_file(self):
        """Tests rendering with a from_file"""
        self.header.title = None
        self.header.from_file = 'from_file'
        self.header.render_title_tab()
        self.mock_construct.assert_called_once_with('from_file', True)


class RenderVcsLinkTabUnitTests(BlockHeaderTestCase):
    """Collects tests on render_vcs_link_tab"""

    def setUp(self):
        self.construct_with_mock_statics()

    def test_without_link(self):
        """Tests output without a link"""
        self.header.vcs_link = None
        self.assertEqual(
            self.header.render_vcs_link_tab(),
            BlockHeader.RENDER_AN_OPTION_NOT_INCLUDED
        )
        self.mock_construct.assert_not_called()

    def test_with_link(self):
        """Tests output with a link"""
        self.header.vcs_link = 'qqq'
        output = (
            '<a target="_blank" href="qqq">'
            'view source <i class="fa fa-external-link"></i>'
            '</a>'
        )
        self.header.render_vcs_link_tab()
        self.mock_construct.assert_called_once_with(output)


class RenderFullHeader(BlockHeaderTestCase):
    """Collects tests for render_full_header"""

    def setUp(self):
        branch_patcher = patch.object(
            BlockHeader,
            'render_vcs_branch_tab',
            return_value='mock_branch',
        )
        self.mock_branch = branch_patcher.start()
        self.addCleanup(branch_patcher.stop)
        link_patcher = patch.object(
            BlockHeader,
            'render_vcs_link_tab',
            return_value='mock_link',
        )
        self.mock_link = link_patcher.start()
        self.addCleanup(link_patcher.stop)
        title_patcher = patch.object(
            BlockHeader,
            'render_title_tab',
            return_value='mock_title',
        )
        self.mock_title = title_patcher.start()
        self.addCleanup(title_patcher.stop)
        self.construct_header()

    def test_full_render(self):
        """Tests the full render"""
        desired_output = (
            '<tr class="code-header">'
            '<td></td>'
            '<td class="code-header">'
            'mock_branch'
            'mock_title'
            'mock_link'
            '</td>'
            '</tr>'
        )
        output = self.header.render_full_header()
        self.assertEqual(output, desired_output)
