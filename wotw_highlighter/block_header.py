"""This file provides a class to attach a header to a block"""

from wotw_highlighter.block_options import BlockOptions

class BlockHeader(BlockOptions):
    """This class compiles and renders a block's header (if any)"""
    def __init__(self, **kwargs):
        """The ctor simply loads options via BlockOptions"""
        super(BlockHeader, self).__init__(kwargs)

    @staticmethod
    def construct_code_tab(contents, active=False):
        """
        This convenience method wraps contents in the proper markup

        Parameters:
        contents: The contents of the tab
        active: Whether or not the tab should be marked as active
        """
        return (
            '<div class="code-tab%s">'
            '%s'
            '</div>'
            % (
                (
                    ' active'
                    if active
                    else ''
                ),
                contents
            )
        )
