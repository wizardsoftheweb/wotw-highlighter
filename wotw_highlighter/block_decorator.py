"""This file provides a class to decorate the base Pygments result"""

from re import sub

from wotw_highlighter.block_options import BlockOptions
from wotw_highlighter.block_header import BlockHeader


class BlockDecorator(BlockOptions):
    """This class decorates highlighted blobs"""

    header = None

    def validate(self):
        if not self.highlighted_blob:
            raise ValueError('Nothing to decorate')

    def remove_linenos(self):
        """Removes line numbers from a highlighted blob"""
        self.highlighted_blob = sub(
            r'<td[\s\S]*?linenos[\s\S]*?</td>',
            '',
            self.highlighted_blob
        )

    def compile_header(self):
        """Compiles a block header"""
        block_header = BlockHeader(**self.full_options())
        self.header = block_header.render_full_header()
