# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=unused-argument
# pylint: disable=attribute-defined-outside-init

from unittest import TestCase

from mock import call, MagicMock, patch
from pygments.formatters.html import HtmlFormatter
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


class HighlightUnitTests(BlockHighlighterTestCase):

    @patch(
        'wotw_highlighter.block_highlighter.highlight'
    )
    def test_highlight_call(self, mock_highlight):
        highlight_ret_val = 'your token string'
        mock_highlight.return_value = highlight_ret_val
        self.block_highlighter.blob = fake_blob = 'qqq'
        self.block_highlighter.lexer = mock_lexer = MagicMock(spec=Lexer)
        self.block_highlighter.formatter = mock_formatter = MagicMock(
            spec=HtmlFormatter
        )
        self.block_highlighter.highlight()
        self.assertEqual(
            self.block_highlighter.highlighted_blob,
            highlight_ret_val
        )
        mock_highlight.assert_called_once_with(
            fake_blob,
            mock_lexer,
            mock_formatter
        )


class AttachAndHighlightUnitTests(BlockHighlighterTestCase):

    def setUp(self):
        lexer_patcher = patch.object(BlockHighlighter, 'attach_lexer')
        self.mock_lexer = lexer_patcher.start()
        self.addCleanup(lexer_patcher.stop)
        formatter_patcher = patch.object(BlockHighlighter, 'attach_formatter')
        self.mock_formatter = formatter_patcher.start()
        self.addCleanup(formatter_patcher.stop)
        highlight_patcher = patch.object(BlockHighlighter, 'highlight')
        self.mock_highlight = highlight_patcher.start()
        self.addCleanup(highlight_patcher.stop)
        self.build_highlighter()

    def test_runner_method(self):
        mock_container = MagicMock()
        mock_container.attach_mock(self.mock_lexer, 'lexer')
        mock_container.attach_mock(self.mock_formatter, 'formatter')
        mock_container.attach_mock(self.mock_highlight, 'highlight')
        self.block_highlighter.attach_and_highlight()
        mock_container.assert_has_calls([
            call.lexer(),
            call.formatter(),
            call.highlight()
        ])
