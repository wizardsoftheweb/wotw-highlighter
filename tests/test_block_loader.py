# pylint: disable=w0201
# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0613
"""This file collects tests for Loader"""

from subprocess import CalledProcessError
from unittest import TestCase
from mock import call, MagicMock, patch

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


class LoadFromFileUnitTests(LoaderTestCase):

    FILE_CONTENTS = 'qqq'

    def setUp(self):
        self.build_loader()

    @patch(
        'wotw_highlighter.block_loader.open',
        return_value=MagicMock(
            read=MagicMock(return_value=FILE_CONTENTS)
        )
    )
    def test_existing_file(self, mock_open):  # pylint: disable=W0613
        self.block_loader.load_from_file()
        self.assertEqual(self.block_loader.blob, self.FILE_CONTENTS)

    @patch(
        'wotw_highlighter.block_loader.open',
        side_effect=IOError,
    )
    def test_nonexistant_file(self, mock_open):  # pylint: disable=W0613
        with self.assertRaises(IOError):
            self.block_loader.load_from_file()


class DiscoverBlobHashUnitTests(LoaderTestCase):

    GIT_HASH = 'qqq'

    def setUp(self):
        self.build_loader()
        self.block_loader.git_ref_name = None
        self.block_loader.git_ref_hash = None
        self.block_loader.git_blob_hash = None
        self.block_loader.blob_path = None

    @patch(
        'wotw_highlighter.block_loader.check_output',
    )
    def test_with_blob_hash(self, mock_check_output):
        self.block_loader.git_blob_hash = self.GIT_HASH
        self.block_loader.discover_blob_hash()
        self.assertFalse(mock_check_output.called)
        self.assertEqual(self.block_loader.git_blob_hash, self.GIT_HASH)

    @patch(
        'wotw_highlighter.block_loader.check_output',
        return_value='mode type %s' % (GIT_HASH)
    )
    def test_with_ref_name_and_blob_path(self, mock_check_output):
        self.block_loader.git_ref_name = 'git_ref_name'
        self.block_loader.blob_path = 'blob_path'
        self.block_loader.discover_blob_hash()
        mock_check_output.assert_called_once_with(
            ['git', 'ls-tree', 'git_ref_name', 'blob_path'],
        )
        self.assertEqual(self.block_loader.git_blob_hash, self.GIT_HASH)

    @patch(
        'wotw_highlighter.block_loader.check_output',
        return_value='mode type %s' % (GIT_HASH)
    )
    def test_with_ref_hash_and_blob_path(self, mock_check_output):
        self.block_loader.git_ref_hash = 'git_ref_hash'
        self.block_loader.blob_path = 'blob_path'
        self.block_loader.discover_blob_hash()
        mock_check_output.assert_called_once_with(
            ['git', 'ls-tree', 'git_ref_hash', 'blob_path'],
        )
        self.assertEqual(self.block_loader.git_blob_hash, self.GIT_HASH)

    @patch(
        'wotw_highlighter.block_loader.check_output',
        side_effect=CalledProcessError(cmd='', returncode=1)
    )
    def test_failed_process(self, mock_check_output):
        self.block_loader.git_ref_hash = 'git_ref_hash'
        self.block_loader.blob_path = 'blob_path'
        with self.assertRaisesRegexp(ValueError, 'Ref.*?does not contain'):
            self.block_loader.discover_blob_hash()

    @patch(
        'wotw_highlighter.block_loader.check_output',
        return_value='',
    )
    def test_empty_ls_tree(self, mock_check_output):
        self.block_loader.git_ref_hash = 'git_ref_hash'
        self.block_loader.blob_path = 'blob_path'
        with self.assertRaisesRegexp(ValueError, 'Ref.*?does not contain'):
            self.block_loader.discover_blob_hash()


class LoadFromGitUnitTests(LoaderTestCase):

    BLOB_HASH = 'qqq'
    BLOB_CONTENTS = 'raw is war'

    def set_hash_side_effect(self):
        self.block_loader.git_blob_hash = self.BLOB_HASH

    def setUp(self):
        discover_patcher = patch.object(
            BlockLoader,
            'discover_blob_hash',
            side_effect=self.set_hash_side_effect,
        )
        self.mock_discover = discover_patcher.start()
        self.addCleanup(discover_patcher.stop)
        self.build_loader()
        self.block_loader.git_blob_hash = None

    @patch(
        'wotw_highlighter.block_loader.check_output',
    )
    def test_blob_hash_discovery(self, mock_check_output):
        self.assertIsNone(self.block_loader.git_blob_hash)
        self.block_loader.load_from_git()
        self.assertEqual(self.block_loader.git_blob_hash, self.BLOB_HASH)

    @patch(
        'wotw_highlighter.block_loader.check_output',
        return_value=BLOB_CONTENTS,
    )
    def test_blob_assignment(self, mock_check_output):
        self.assertIsNone(self.block_loader.blob)
        self.block_loader.load_from_git()
        self.assertEqual(self.block_loader.blob, self.BLOB_CONTENTS)


class ParseRawAsOptionsUnitTests(LoaderTestCase):

    REF = 'qqq'
    PATH = 'path/to/file'

    def setUp(self):
        self.build_loader()
        self.block_loader.git_ref_name = None
        self.block_loader.git_ref_hash = None
        self.block_loader.git_blob_hash = None
        self.block_loader.blob_path = None
        self.block_loader.raw = None

    def test_with_different_ref_hash(self):
        self.block_loader.raw = '%s:%s' % (self.REF, self.PATH)
        self.block_loader.git_ref_hash = 'not-%s' % (self.REF)
        with self.assertRaisesRegexp(ValueError, 'Parsing the positional args'):
            self.block_loader.parse_raw_as_options()

    def test_with_same_ref_hash(self):
        self.block_loader.raw = '%s:%s' % (self.REF, self.PATH)
        self.block_loader.git_ref_hash = self.REF
        self.block_loader.parse_raw_as_options()
        self.assertEqual(self.block_loader.git_ref_hash, self.REF)

    def test_with_different_ref_name(self):
        self.block_loader.raw = '%s:%s' % (self.REF, self.PATH)
        self.block_loader.git_ref_name = 'not-%s' % (self.REF)
        with self.assertRaisesRegexp(ValueError, 'Parsing the positional args'):
            self.block_loader.parse_raw_as_options()

    def test_with_same_ref_name(self):
        self.block_loader.raw = '%s:%s' % (self.REF, self.PATH)
        self.block_loader.git_ref_name = self.REF
        self.block_loader.parse_raw_as_options()
        self.assertEqual(self.block_loader.git_ref_name, self.REF)

    def test_with_different_blob_path(self):
        self.block_loader.raw = '%s:%s' % (self.REF, self.PATH)
        self.block_loader.blob_path = 'not-%s' % (self.PATH)
        with self.assertRaisesRegexp(ValueError, 'Parsing the positional args'):
            self.block_loader.parse_raw_as_options()

    def test_with_same_blob_path(self):
        self.block_loader.raw = '%s:%s' % (self.REF, self.PATH)
        self.block_loader.blob_path = self.PATH
        self.block_loader.parse_raw_as_options()
        self.assertEqual(self.block_loader.blob_path, self.PATH)

    def test_with_newline_in_raw(self):
        raw_code = (
            '''raw is
            war\
            '''
        )
        self.block_loader.raw = raw_code
        self.assertIsNone(self.block_loader.blob)
        self.block_loader.parse_raw_as_options()
        self.assertEqual(self.block_loader.blob, raw_code)


class LoadUnitTests(LoaderTestCase):

    RAW_INPUT = 'raw is war'
    BLOB_CONTENT = 'blob_content'

    def set_blob_side_effect(self):
        self.block_loader.blob = self.BLOB_CONTENT

    def setUp(self):
        parse_patcher = patch.object(BlockLoader, 'parse_raw_as_options')
        self.mock_parse = parse_patcher.start()
        self.addCleanup(parse_patcher.stop)
        load_git_patcher = patch.object(BlockLoader, 'load_from_git')
        self.mock_load_git = load_git_patcher.start()
        self.addCleanup(load_git_patcher.stop)
        load_file_patcher = patch.object(BlockLoader, 'load_from_file')
        self.mock_load_file = load_file_patcher.start()
        self.addCleanup(load_file_patcher.stop)
        self.build_loader()
        self.block_loader.blob = None

    def test_parse_raw_is_blob(self):
        self.block_loader.blob = self.RAW_INPUT
        self.mock_load_git.side_effect = IOError
        output = self.block_loader.load()
        self.assertEqual(output, self.RAW_INPUT)
        self.mock_parse.assert_called_once_with()
        self.assertFalse(self.mock_load_git.called)
        self.assertFalse(self.mock_load_file.called)

    def test_load_git_successful(self):
        self.block_loader.git_blob_hash = self.RAW_INPUT
        self.mock_load_git.side_effect = self.set_blob_side_effect
        self.mock_load_file.side_effect = IOError
        self.assertNotEqual(self.block_loader.blob, self.BLOB_CONTENT)
        output = self.block_loader.load()
        self.assertEqual(output, self.BLOB_CONTENT)
        self.mock_parse.assert_called_once_with()
        self.mock_load_git.assert_called_once_with()
        self.assertFalse(self.mock_load_file.called)

    def test_load_file_successful(self):
        self.block_loader.git_blob_hash = self.RAW_INPUT
        self.mock_load_git.side_effect = ValueError
        self.mock_load_file.side_effect = self.set_blob_side_effect
        self.assertNotEqual(self.block_loader.blob, self.BLOB_CONTENT)
        output = self.block_loader.load()
        self.assertEqual(output, self.BLOB_CONTENT)
        self.mock_parse.assert_called_once_with()
        self.mock_load_git.assert_called_once_with()
        self.mock_load_file.assert_called_once_with()

    def test_loads_failed(self):
        self.block_loader.raw = self.RAW_INPUT
        self.block_loader.git_blob_hash = self.RAW_INPUT
        self.mock_load_git.side_effect = ValueError
        self.mock_load_file.side_effect = ValueError
        self.assertNotEqual(self.block_loader.blob, self.RAW_INPUT)
        output = self.block_loader.load()
        self.assertEqual(output, self.RAW_INPUT)
        self.mock_parse.assert_called_once_with()
        self.mock_load_git.assert_called_once_with()
        self.mock_load_file.assert_called_once_with()

    def test_everything_failed(self):
        self.block_loader.raw = None
        self.mock_load_git.side_effect = ValueError
        self.mock_load_file.side_effect = ValueError
        with self.assertRaisesRegexp(ValueError, 'Unable'):
            self.block_loader.load()
        self.mock_parse.assert_called_once_with()
        self.assertFalse(self.mock_load_git.called)
        self.mock_load_file.assert_called_once_with()
