# pylint: disable=w0201
# pylint: disable=C0111

from unittest import TestCase
from mock import patch

from wotw_highlighter import BlockHighlighter


class BlockHighlighterTestCase(TestCase):

    def setUp(self):
        self.build_highlighter()

    def wipe_highlighter(self):
        """Nukes the constructed loader"""
        del self.block_highlighter

    def build_highlighter(self, *args, **kwargs):
        """Constructs a basic loader using only the defaults"""
        # if not kwargs:
        #     kwargs = self.DEFAULT_KWARGS
        move_patcher = patch.object(
            BlockHighlighter, 'move_to_working_directory')
        move_patcher.start()
        validate_patcher = patch.object(BlockHighlighter, 'validate')
        validate_patcher.start()
        self.block_highlighter = BlockHighlighter(*args, **kwargs)
        validate_patcher.stop()
        move_patcher.stop()
        self.addCleanup(self.wipe_highlighter)


class ValidateUnitTests(BlockHighlighterTestCase):

    def test_validate_without_blob(self):
        self.block_highlighter.blob = None
        with self.assertRaises(ValueError):
            self.block_highlighter.validate()

    def test_validate_with_blob(self):
        self.block_highlighter.blob = 'blob'
        self.assertIsNone(self.block_highlighter.validate())
