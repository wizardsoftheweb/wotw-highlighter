# pylint: disable=w0201
# pylint: disable=C0111
"""This file collects tests for Loader"""

from subprocess import CalledProcessError
from unittest import TestCase
from mock import patch

from wotw_highlighter import BlockLoader


class LoaderTestCase(TestCase):
    """Collects common items and defaults across test cases"""

    BLOB_WORKING_DIRECTORY = 'blob/working/directory'

    DEFAULT_KWARGS = {
        'blob_working_directory': BLOB_WORKING_DIRECTORY
    }

    def wipe_loader(self):
        """Nukes the constructed loader"""
        del self.block_loader

    def build_loader(self, **kwargs):
        """Constructs a basic loader using only the defaults"""
        if not kwargs:
            kwargs = self.DEFAULT_KWARGS
        move_patcher = patch.object(BlockLoader, 'move_to_working_directory')
        move_patcher.start()
        validate_patcher = patch.object(BlockLoader, 'validate')
        validate_patcher.start()
        self.block_loader = BlockLoader(**kwargs)
        validate_patcher.stop()
        move_patcher.stop()
        self.addCleanup(self.wipe_loader)


class ValidateGitDirectory(LoaderTestCase):

    def setUp(self):
        self.build_loader()

    @patch('wotw_highlighter.block_loader.check_call')
    def test_ref_name_that_exists(self, mock_call):  # pylint: disable=W0613
        self.assertIsNone(self.block_loader.validate_git_directory())

    @patch(
        'wotw_highlighter.block_loader.check_call',
        side_effect=CalledProcessError(cmd='', returncode=1)
    )
    def test_ref_name_that_doesnt_exist(self, mock_call):  # pylint: disable=W0613
        with self.assertRaises(ValueError):
            self.block_loader.validate_git_directory()


class ValidateGitRefNameUnitTests(LoaderTestCase):

    def setUp(self):
        self.build_loader()

    @patch('wotw_highlighter.block_loader.check_call')
    def test_ref_name_that_exists(self, mock_call):  # pylint: disable=W0613
        self.assertIsNone(self.block_loader.validate_git_ref_name())

    @patch(
        'wotw_highlighter.block_loader.check_call',
        side_effect=CalledProcessError(cmd='', returncode=1)
    )
    def test_ref_name_that_doesnt_exist(self, mock_call):  # pylint: disable=W0613
        with self.assertRaises(ValueError):
            self.block_loader.validate_git_ref_name()


class ValidateGitHashUnitTests(LoaderTestCase):

    def setUp(self):
        self.build_loader()

    @patch('wotw_highlighter.block_loader.check_call')
    def test_ref_name_that_exists(self, mock_call):  # pylint: disable=W0613
        self.assertIsNone(self.block_loader.validate_git_hash('some hash'))

    @patch(
        'wotw_highlighter.block_loader.check_call',
        side_effect=CalledProcessError(cmd='', returncode=1)
    )
    def test_ref_name_that_doesnt_exist(self, mock_call):  # pylint: disable=W0613
        with self.assertRaises(ValueError):
            self.block_loader.validate_git_hash('some hash')
