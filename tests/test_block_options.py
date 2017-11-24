# pylint: disable=w0201
# pylint: disable=C0103
# pylint: disable=C0111
"""Collects tests for BlockOptions"""

from collections import defaultdict
from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_highlighter import BlockOptions


class BlockOptionsTestCase(TestCase):
    """Collects common items and defaults across test cases"""

    DEFAULT_VALUE = 'qqq'

    LAUNCH_DIRECTORY = 'launch/directory'

    def tearDown(self):
        del self.block_options

    def patch_ctor_methods(self):
        """Patches the validate method"""
        self.validate_patch = patch.object(BlockOptions, 'validate')
        self.mock_validate = self.validate_patch.start()
        self.move_patch = patch.object(
            BlockOptions,
            'move_to_working_directory'
        )
        self.mock_move = self.move_patch.start()

    def schedule_ctor_patch_cleanup(self):
        """Defers removing the patch"""
        self.addCleanup(self.validate_patch.stop)
        self.addCleanup(self.move_patch.stop)

    def construct_options(self, *args, **kwargs):
        getcwd_patch = patch(
            'wotw_highlighter.block_options.getcwd',
            return_value=self.LAUNCH_DIRECTORY
        )
        getcwd_patch.start()
        self.block_options = BlockOptions(*args, **kwargs)
        getcwd_patch.stop()

    def build_options(self, *args, **kwargs):
        """
        Patches the method in the constructor, creates the instance, and removes
        the patch
        """
        self.patch_ctor_methods()
        self.construct_options(*args, **kwargs)
        self.validate_patch.stop()
        self.move_patch.stop()

    def build_options_retain_mocks(self, *args, **kwargs):
        """
        Patches the method and creates the instance without removing the mock
        """
        self.patch_ctor_methods()
        self.construct_options(*args, **kwargs)
        self.schedule_ctor_patch_cleanup()


class ConstructorUnitTests(BlockOptionsTestCase):
    """Tests the constructor"""

    def test_consumed_options(self):
        """Ensures all valid options can be set"""
        for option in BlockOptions.USED_KWARGS:
            input_args = defaultdict()
            input_args[option] = self.DEFAULT_VALUE
            self.build_options_retain_mocks(**input_args)
            self.assertEqual(
                getattr(self.block_options, option),
                self.DEFAULT_VALUE
            )

    def test_ignored_args(self):
        """Ensures other options are ignored"""
        ignored_option = 'zzz'
        input_args = defaultdict()
        input_args[ignored_option] = self.DEFAULT_VALUE
        self.build_options_retain_mocks(**input_args)
        self.assertFalse(hasattr(self.block_options, ignored_option))

    def test_move_then_validate(self):
        """Ensures the validate method is called"""
        mock_holder = MagicMock()
        self.patch_ctor_methods()
        mock_holder.attach_mock(self.mock_move, 'move')
        mock_holder.attach_mock(self.mock_validate, 'validate')
        self.construct_options()
        self.schedule_ctor_patch_cleanup()
        mock_holder.assert_has_calls([
            call.move(),
            call.validate()
        ])

    def test_setting_raw(self):
        raw_args = 'raw is war'
        self.build_options_retain_mocks(raw_args)
        self.assertEqual(self.block_options.raw, raw_args)


class MoveToWorkingDirectoryUnitTests(BlockOptionsTestCase):

    def setUp(self):
        chdir_patch = patch('wotw_highlighter.block_options.chdir')
        self.mock_chdir = chdir_patch.start()
        self.addCleanup(chdir_patch.stop)
        self.build_options()

    def test_proper_directory_applied(self):
        self.block_options.return_to_launch_directory()
        self.mock_chdir.assert_called_once_with(self.LAUNCH_DIRECTORY)


class ValidateUnitTests(BlockOptionsTestCase):
    """Tests the empty validate method"""

    def test_nothing_happens_with_base(self):
        """Ensures nothing happens"""
        self.build_options()
        self.assertIsNone(self.block_options.validate())


class FullOptionsUnitTests(BlockOptionsTestCase):
    """Tests full_options"""

    def setUp(self):
        self.build_options()

    def test_contains_all_options(self):
        """Ensure it returns all the important options"""
        returned_options = self.block_options.full_options()
        for key in BlockOptions.USED_KWARGS:
            self.assertTrue(returned_options.has_key(key))

    def test_returns_proper_options(self):
        """Ensure it returns the proper values"""
        self.assertIsNone(self.block_options.title)
        self.block_options.title = self.DEFAULT_VALUE
        returned_options = self.block_options.full_options()
        self.assertEqual(returned_options['title'], self.DEFAULT_VALUE)


class ReturnToOriginalDirectoryUnitTests(BlockOptionsTestCase):

    def setUp(self):
        chdir_patch = patch('wotw_highlighter.block_options.chdir')
        self.mock_chdir = chdir_patch.start()
        self.addCleanup(chdir_patch.stop)
        self.build_options()

    def test_proper_directory_applied(self):
        self.block_options.return_to_launch_directory()
        self.mock_chdir.assert_called_once_with(self.LAUNCH_DIRECTORY)
