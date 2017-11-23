"""This file provides a common class used to collect all of the block options"""

class BlockOptions(object):
    """
    BlockOptions collects all of the options needed to run any of the child
    classes so that its descendants can pull out only what they need.
    """
    def __init__(
            self,
            from_file='',
            alternate_title='',
            vcs_branch='',
            vcs_link='',
            linenos=True
        ):
        """The ctor simply assigns defaults"""
        self.from_file = from_file
        self.alternate_title = alternate_title
        self.vcs_branch = vcs_branch
        self.vcs_link = vcs_link
        self.linenos = linenos
