# pylint: disable=w0201
# pylint: disable=C0111
"""This file collects tests for Loader"""

from subprocess import CalledProcessError
from unittest import TestCase
from mock import call, patch

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

    def build_loader(self, *args, **kwargs):
        """Constructs a basic loader using only the defaults"""
        if not kwargs:
            kwargs = self.DEFAULT_KWARGS
        move_patcher = patch.object(BlockLoader, 'move_to_working_directory')
        move_patcher.start()
        validate_patcher = patch.object(BlockLoader, 'validate')
        validate_patcher.start()
        self.block_loader = BlockLoader(*args, **kwargs)
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


class ValidateUnitTests(LoaderTestCase):

    def setUp(self):
        ref_name_patcher = patch.object(BlockLoader, 'validate_git_ref_name')
        self.mock_ref_name = ref_name_patcher.start()
        self.addCleanup(ref_name_patcher.stop)
        hash_patcher = patch.object(BlockLoader, 'validate_git_hash')
        self.mock_hash = hash_patcher.start()
        self.addCleanup(hash_patcher.stop)
        directory_patcher = patch.object(BlockLoader, 'validate_git_directory')
        self.mock_directory = directory_patcher.start()
        self.addCleanup(directory_patcher.stop)
        self.build_loader()
        self.block_loader.blob_path = 'qqq'

    def test_everything_empty_fails(self):
        self.block_loader.blob_path = None
        self.block_loader.git_ref_name = None
        self.block_loader.git_ref_hash = None
        self.block_loader.git_blob_hash = None
        with self.assertRaisesRegexp(
            ValueError,
            'Must specify an input string, file, or git ref'
        ):
            self.block_loader.validate()

    def test_ref_only(self):
        self.block_loader.blob_path = None
        self.block_loader.git_ref_name = 'qqq'
        self.block_loader.git_ref_hash = None
        self.block_loader.git_blob_hash = None
        with self.assertRaisesRegexp(
            ValueError,
            'Cannot specify a ref name or hash'
        ):
            self.block_loader.validate()

    def test_git_directory(self):
        self.block_loader.git_ref_name = 'git_ref_name'
        self.block_loader.validate()
        self.mock_directory.assert_called_once_with()

    def test_git_ref_name(self):
        self.block_loader.git_ref_name = 'git_ref_name'
        self.block_loader.validate()
        self.mock_ref_name.assert_called_once_with()

    def test_git_hash(self):
        self.block_loader.git_ref_hash = 'git_ref_hash'
        self.block_loader.git_blob_hash = 'git_blob_hash'
        self.block_loader.validate()
        self.mock_hash.assert_has_calls([
            call('git_ref_hash'),
            call('git_blob_hash')
        ])
