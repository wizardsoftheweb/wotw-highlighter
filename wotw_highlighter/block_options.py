"""This file provides a common class used to collect all of the block options"""


class BlockOptions(object):
    """
    BlockOptions collects all of the options needed to run any of the child
    classes so that its descendants can pull out only what they need.
    """

    USED_KWARGS = [
        'from_file',
        'linenos',
        'no_header',
        'title',
        'vcs_branch',
        'vcs_link'
    ]

    from_file = None
    linenos = True
    no_header = False
    title = None
    vcs_branch = None
    vcs_link = None

    def __init__(self, **kwargs):
        """The ctor simply assigns defaults

        Possible parameters:
        from_file = None
            A filename to load/parse/etc
        linenos = True
            Whether or not to generate line numbers
        no_header = False
            Skip header generation on files/named blobs
        title=None
            The title to use for highlighted blobs or instead of the filename
        vcs_branch = None
            Branch/Reference from VCS
        vcs_link = None
            Link to the file in VCS
        """
        for option in self.USED_KWARGS:
            if option in kwargs:
                setattr(self, option, kwargs.get(option))
        self.validate()

    def validate(self):  # pylint: disable=R0201
        """Overriden by children to validate options"""
        return

    def full_options(self):
        """Compiles a dict with all option values"""
        options = dict()
        for option in self.USED_KWARGS:
            options[option] = getattr(self, option)
        return options
