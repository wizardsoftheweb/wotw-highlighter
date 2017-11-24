"""This file provides a class to highlight code"""

# from pygments import highlight
# from pygments.lexers import get_lexer_for_filename, guess_lexer
# from pygments.formatters import HtmlFormatter


from pygments import lexers
from pygments.util import ClassNotFound

from wotw_highlighter.block_options import BlockOptions


class BlockHighlighter(BlockOptions):
    """
    This class provides a collection of methods to highlight blocks of code
    """

    lexer = None

    def validate(self):
        """Validates BlockHighlighter options"""
        if not self.blob:
            raise ValueError('No blob passed to highlighter')
        if (
                self.explicit_lexer_name
                and
                not hasattr(lexers, self.explicit_lexer_name)
        ):
            raise ValueError('The specified lexer (%s) could not be found')

    def attach_lexer(self):
        """
        Either assigns the explicitly named lexer or guesses the proper lexer
        """
        if self.explicit_lexer_name:
            self.lexer = getattr(
                lexers, self.explicit_lexer_name)(stripall=True)
        else:
            try:
                self.lexer = lexers.get_lexer_for_filename(
                    self.blob_path,
                    stripall=True,
                )
            except ClassNotFound:
                self.lexer = lexers.guess_lexer(
                    self.blob,
                    stripall=True,
                )
