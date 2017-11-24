# pylint: disable=w0201
# pylint: disable=C0103
"""Collects tests for BlockOptions"""

from collections import defaultdict

import unittest

from mock import patch

from wotw_highlighter import BlockOptions


class BlockOptionsTestCase(unittest.TestCase):
    """Collects common items and defaults across test cases"""

    DEFAULT_VALUE = 'qqq'

    def tearDown(self):
        del self.block_options

    def patch_validate(self):
        """Patches the validate method"""
        self.validate_patch = patch.object(BlockOptions, 'validate')
        self.mock_validate = self.validate_patch.start()

    def schedule_patch_cleanup(self):
        """Defers removing the patch"""
        self.addCleanup(self.validate_patch.stop)

    def build_options(self, **kwargs):
        """
        Patches the method in the constructor, creates the instance, and removes
        the patch
        """
        self.patch_validate()
        self.block_options = BlockOptions(**kwargs)
        self.validate_patch.stop()

    def build_options_with_mock_validate(self, **kwargs):
        """
        Patches the method and creates the instance without removing the mock
        """
        self.patch_validate()
        self.block_options = BlockOptions(**kwargs)
        self.schedule_patch_cleanup()


class ConstructorUnitTests(BlockOptionsTestCase):
    """Tests the constructor"""

    def test_consumed_options(self):
        """Ensures all valid options can be set"""
        for option in BlockOptions.USED_KWARGS:
            input_args = defaultdict()
            input_args[option] = self.DEFAULT_VALUE
            self.build_options_with_mock_validate(**input_args)
            self.assertEqual(
                getattr(self.block_options, option),
                self.DEFAULT_VALUE
            )

    def test_ignored_args(self):
        """Ensures other options are ignored"""
        ignored_option = 'zzz'
        input_args = defaultdict()
        input_args[ignored_option] = self.DEFAULT_VALUE
        self.build_options_with_mock_validate(**input_args)
        self.assertFalse(hasattr(self.block_options, ignored_option))

    def test_validate(self):
        """Ensures the validate method is called"""
        self.build_options_with_mock_validate()
        self.assertEquals(self.mock_validate.call_count, 1)


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