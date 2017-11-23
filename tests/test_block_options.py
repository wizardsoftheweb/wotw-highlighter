"""Collects tests for BlockOptions"""

from collections import defaultdict
import unittest
# from mock import MagicMock, patch

from wotw_highlighter import BlockOptions

class ConstructorUnitTests(unittest.TestCase):
    """Tests the constructor"""

    DEFAULT_VALUE = 'qqq'

    def test_valid_options(self):
        """Ensures all valid options can be set"""
        options = [
            'alternate_title',
            'from_file',
            'vcs_branch',
            'vcs_link',
            'linenos',
        ]
        for option in options:
            input_args = defaultdict()
            input_args[option] = self.DEFAULT_VALUE
            block_options = BlockOptions(**input_args)
            self.assertEqual(
                getattr(block_options, option),
                self.DEFAULT_VALUE
            )
