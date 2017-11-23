"""This file provides a class to attach a header to a block"""

from wotw_highlighter.block_options import BlockOptions

class BlockHeader(BlockOptions):
    """This class compiles and renders a block's header (if any)"""

    RENDER_AN_OPTION_NOT_INCLUDED = ''

    ERROR_NEED_FROM_FILE_OR_TITLE = ValueError('''\
from_file and alternate_title cannot both be empty when generating a header\
''')

    def validate(self):
        """Overrides super validate"""
        if self.from_file is None and self.title is None:
            raise self.ERROR_NEED_FROM_FILE_OR_TITLE

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

    def render_vcs_branch_tab(self):
        """Renders the VCS branch tab"""
        if self.vcs_branch:
            return self.construct_code_tab(self.vcs_branch)
        return self.RENDER_AN_OPTION_NOT_INCLUDED

    def render_title_tab(self):
        """Renders the blob title"""
        title = (
            self.title
            if self.title
            else self.from_file
        )
        return self.construct_code_tab(title, True)

    def render_vcs_link_tab(self):
        """Renders the VCS link tab"""
        if self.vcs_link:
            tab_body = (
                '<a target="_blank" href="%s">'
                'view source <i class="fa fa-external-link"></i>'
                '</a>'
                % (self.vcs_link)
            )
            return self.construct_code_tab(tab_body)
        return self.RENDER_AN_OPTION_NOT_INCLUDED
