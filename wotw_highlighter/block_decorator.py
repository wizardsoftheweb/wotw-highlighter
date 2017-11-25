"""This file provides a class decorate the base Pygments result"""

from wotw_highlighter.block_options import BlockOptions


class BlockDecorator(BlockOptions):
    """This class decorates highlighted blobs"""

    def validate(self):
        if not self.highlighted_blob:
            raise ValueError('Nothing to decorate')
