"""This file provides a class to build and run everything"""

from wotw_highlighter.block_options import BlockOptions
from wotw_highlighter.block_loader import BlockLoader
from wotw_highlighter.block_highlighter import BlockHighlighter


class Block(BlockOptions):
    """This class loads code, highlights, and returns a polished block"""

    def load(self):
        """Loads the block"""
        loaded_block = BlockLoader(**self.full_options())
        loaded_block.load()
        self.update_options(**loaded_block.full_options())

    def highlight(self):
        """Highlights the block"""
        highlighted_block = BlockHighlighter(**self.full_options())
        highlighted_block.attach_lexer()
        highlighted_block.attach_formatter()
        highlighted_block.highlight()
        self.update_options(**highlighted_block.full_options())
