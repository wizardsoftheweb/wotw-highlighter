# pylint: disable=w0201
# pylint: disable=C0111
"""This file collects tests for BlockHeader"""

from unittest import TestCase
from mock import patch

from wotw_highlighter import BlockHeader


class BlockHeaderTestCase(TestCase):
    """Collects common items and defaults across test cases"""

    def wipe_header(self):
        """Nukes the constructed header"""
        del self.block_header

    def build_header(self):
        """Constructs a basic header using only the defaults"""
        validate_patcher = patch.object(BlockHeader, 'validate')
        validate_patcher.start()
        self.block_header = BlockHeader(title='qqq.qqq')
        validate_patcher.stop()
        self.addCleanup(self.wipe_header)

    def build_header_with_mock_statics(self):
        """Constructs a basic header with static methods mocked"""
        construct_patcher = patch.object(BlockHeader, 'construct_code_tab')
        self.mock_construct = construct_patcher.start()
        self.addCleanup(construct_patcher.stop)
        self.build_header()


class ValidateUnittests(BlockHeaderTestCase):
    """Collects tests on validate"""

    def setUp(self):
        self.build_header()

    def test_no_title_check(self):
        """Ensures an error is thrown when no title is used"""
        self.block_header.blob_path = None
        self.block_header.title = None
        with self.assertRaises(ValueError):
            self.block_header.validate()

    def test_any_title_check(self):
        """Ensures an okay passes through"""
        self.assertIsNone(self.block_header.validate())


class ConstructCodeTabUnitTests(BlockHeaderTestCase):
    """Collects tests on construct_code_tab"""

    def setUp(self):
        self.build_header()
        self.contents = 'qqq'

    def test_contents_assignment(self):
        """Ensures contents is inserted correctly"""
        output = '<div class="code-tab">qqq</div>'
        self.assertEqual(
            self.block_header.construct_code_tab(self.contents),
            output,
        )

    def test_active_assignment(self):
        """Ensure active is properly assigned"""
        output = '<div class="code-tab active">qqq</div>'
        self.assertEqual(
            self.block_header.construct_code_tab(self.contents, True),
            output,
        )


class RenderVcsBranchTabUnitTestss(BlockHeaderTestCase):
    """Collects tests on render_git_ref_name_tab"""

    def setUp(self):
        self.build_header_with_mock_statics()
        self.branch = 'qqq'

    def test_with_branch(self):
        """Tests rendering with a branch"""
        self.block_header.git_ref_name = self.branch
        self.block_header.render_git_ref_name_tab()
        self.mock_construct.assert_called_with(self.branch)

    def test_without_branch(self):
        """Tests rendering without a branch"""
        self.assertEqual(
            self.block_header.render_git_ref_name_tab(),
            BlockHeader.RENDER_AN_OPTION_NOT_INCLUDED
        )


class RenderTitleTabUnitTests(BlockHeaderTestCase):
    """Collects tests on render_title_tab"""

    def setUp(self):
        self.build_header_with_mock_statics()

    def test_with_title(self):
        """Tests rendering with a title"""
        self.block_header.title = 'title'
        self.block_header.blob_path = None
        self.block_header.render_title_tab()
        self.mock_construct.assert_called_once_with('title', True)

    def test_with_blob_path(self):
        """Tests rendering with a blob_path"""
        self.block_header.title = None
        self.block_header.blob_path = 'blob_path'
        self.block_header.render_title_tab()
        self.mock_construct.assert_called_once_with('blob_path', True)


class RenderVcsLinkTabUnitTests(BlockHeaderTestCase):
    """Collects tests on render_external_source_link_tab"""

    def setUp(self):
        self.build_header_with_mock_statics()

    def test_without_link(self):
        """Tests output without a link"""
        self.block_header.external_source_link = None
        self.assertEqual(
            self.block_header.render_external_source_link_tab(),
            BlockHeader.RENDER_AN_OPTION_NOT_INCLUDED
        )
        self.mock_construct.assert_not_called()

    def test_with_link(self):
        """Tests output with a link"""
        self.block_header.external_source_link = 'qqq'
        output = (
            '<a target="_blank" href="qqq">'
            'view source <i class="fa fa-external-link"></i>'
            '</a>'
        )
        self.block_header.render_external_source_link_tab()
        self.mock_construct.assert_called_once_with(output)


class RenderFullHeader(BlockHeaderTestCase):
    """Collects tests for render_full_header"""

    def setUp(self):
        branch_patcher = patch.object(
            BlockHeader,
            'render_git_ref_name_tab',
            return_value='mock_branch',
        )
        self.mock_branch = branch_patcher.start()
        self.addCleanup(branch_patcher.stop)
        link_patcher = patch.object(
            BlockHeader,
            'render_external_source_link_tab',
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
        self.build_header()

    def test_full_render(self):
        """Tests the full render"""
        desired_output = (
            '<tr class="code-header">'
            '<td></td>'
            '<td class="code-header">'
            'mock_title'
            'mock_branch'
            'mock_link'
            '</td>'
            '</tr>'
        )
        output = self.block_header.render_full_header()
        self.assertEqual(output, desired_output)


class StrUnitTests(BlockHeaderTestCase):
    """Collects tests on __str__"""

    def setUp(self):
        full_patcher = patch.object(
            BlockHeader,
            'render_full_header',
        )
        self.mock_full = full_patcher.start()
        self.addCleanup(full_patcher.stop)
        self.build_header()

    def test_to_string(self):
        """Ensure the test calls the full render method"""
        self.block_header.__str__()
        self.assertEqual(self.mock_full.call_count, 1)
