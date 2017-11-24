# pylint: disable=w0201
# pylint: disable=C0111

from unittest import TestCase
# from mock import patch

from wotw_highlighter import BlockHighlighter


class BlockHighlighterTestCase(TestCase):

    def wipe_highlighter(self):
        del self.block_highlighter

    def build_highlighter(self):
        self.block_highlighter = BlockHighlighter()
