"""This file provides a class to build and run everything"""

from wotw_highlighter.block_options import BlockOptions
from wotw_highlighter.block_loader import BlockLoader

class Block(BlockOptions):
    """This class loads code, highlights, and returns a polished block"""

    def load(self):
        """Loads the block"""
        loaded_block = BlockLoader(**self.full_options())
        loaded_block.load()
        self.update_options(**loaded_block.full_options())
