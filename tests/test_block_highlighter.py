# pylint: disable=w0201
# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0613

from unittest import TestCase

from mock import patch
from pygments.lexer import Lexer
from pygments.lexers.python import PythonLexer
from pygments.util import ClassNotFound

from wotw_highlighter import BlockHighlighter


class BlockHighlighterTestCase(TestCase):

    def setUp(self):
        self.build_highlighter()

    def wipe_highlighter(self):
        """Nukes the constructed loader"""
        del self.block_highlighter

    def build_highlighter(self, *args, **kwargs):
        """Constructs a basic loader using only the defaults"""
        # if not kwargs:
        #     kwargs = self.DEFAULT_KWARGS
        move_patcher = patch.object(
            BlockHighlighter, 'move_to_working_directory')
        move_patcher.start()
        validate_patcher = patch.object(BlockHighlighter, 'validate')
        validate_patcher.start()
        self.block_highlighter = BlockHighlighter(*args, **kwargs)
        validate_patcher.stop()
        move_patcher.stop()
        self.addCleanup(self.wipe_highlighter)


class ValidateUnitTests(BlockHighlighterTestCase):

    def test_validate_without_blob(self):
        self.block_highlighter.blob = None
        self.block_highlighter.explicit_lexer_name = 'PythonLexer'
        with self.assertRaisesRegexp(ValueError, 'blob'):
            self.block_highlighter.validate()

    def test_validate_with_blob(self):
        self.block_highlighter.blob = 'blob'
        self.block_highlighter.explicit_lexer_name = 'PythonLexer'
        self.assertIsNone(self.block_highlighter.validate())

    def test_validate_existing_lexer(self):
        self.block_highlighter.blob = 'blob'
        self.block_highlighter.explicit_lexer_name = 'PythonLexer'
        self.assertIsNone(self.block_highlighter.validate())

    def test_validate_nonexistent_lexer(self):
        self.block_highlighter.blob = 'blob'
        self.block_highlighter.explicit_lexer_name = 'qqq'
        with self.assertRaisesRegexp(ValueError, 'lexer'):
            self.block_highlighter.validate()


class AttachLexerUnitTests(BlockHighlighterTestCase):

    def setUp(self):
        self.build_highlighter()
        self.block_highlighter.lexer = None
        self.block_highlighter.explicit_lexer_name = None
        self.blob_path = None
        self.blob = None

    def test_assign_an_explicit_lexer(self):
        self.block_highlighter.explicit_lexer_name = 'PythonLexer'
        self.assertIsNone(self.block_highlighter.lexer)
        self.block_highlighter.attach_lexer()
        self.assertIsInstance(self.block_highlighter.lexer, PythonLexer)

    def test_guess_from_found_filename(self):
        self.block_highlighter.blob_path = 'test.py'
        self.assertIsNone(self.block_highlighter.lexer)
        self.block_highlighter.attach_lexer()
        self.assertIsInstance(self.block_highlighter.lexer, Lexer)

    @patch(
        'wotw_highlighter.block_highlighter.lexers.get_lexer_for_filename',
        side_effect=ClassNotFound,
    )
    def test_guess_lexer(self, mock_lexer_call):
        self.block_highlighter.blob = (
            '''
            from os import getcwd
            __version__ = 2
            '''
        )
        self.assertIsNone(self.block_highlighter.lexer)
        self.block_highlighter.attach_lexer()
        self.assertIsInstance(self.block_highlighter.lexer, Lexer)


class AttachFormatterUnitTests(BlockHighlighterTestCase):

    @patch(
        'wotw_highlighter.block_highlighter.HtmlFormatter'
    )
    def test_formatter(self, mock_formatter):
        self.block_highlighter.attach_formatter()
        mock_formatter.assert_called_once_with(
            **BlockHighlighter.DEFAULT_HTMLFORMATTER_OPTIONS
        )
