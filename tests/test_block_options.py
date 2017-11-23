"""Collects tests for BlockOptions"""

from collections import defaultdict
import unittest
# from mock import MagicMock, patch

from wotw_highlighter import BlockOptions

class ConstructorUnitTests(unittest.TestCase):
    """Tests the constructor"""

    DEFAULT_VALUE = 'qqq'

    def test_consumed_options(self):
        """Ensures all valid options can be set"""
        for option in BlockOptions.USED_KWARGS:
            input_args = defaultdict()
            input_args[option] = self.DEFAULT_VALUE
            block_options = BlockOptions(**input_args)
            self.assertEqual(
                getattr(block_options, option),
                self.DEFAULT_VALUE
            )

    def test_ignored_args(self):
        """Ensures other options are ignored"""
        ignored_option = 'zzz'
        input_args = defaultdict()
        input_args[ignored_option] = self.DEFAULT_VALUE
        block_options = BlockOptions(**input_args)
        self.assertFalse(hasattr(block_options, ignored_option))
