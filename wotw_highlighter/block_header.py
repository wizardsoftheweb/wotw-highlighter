"""This file provides a class to attach a header to a block"""

from wotw_highlighter.block_options import BlockOptions

class BlockHeader(BlockOptions):
    """This class compiles and renders a block's header (if any)"""
    def __init__(self, **kwargs):
        """The ctor simply loads options via BlockOptions"""
        super(BlockHeader, self).__init__(kwargs)
