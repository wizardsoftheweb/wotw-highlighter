# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0613

from unittest import TestCase

from mock import call, MagicMock, patch

from wotw_highlighter import Block


class BlockTestCase(TestCase):

    PARENT_OPTIONS = {
        'common': 'same',
        'shared': 'parent'
    }

    CHILD_OPTIONS = {
        'common': 'same',
        'shared': 'child'
    }

    def setUp(self):
        self.build_block()

    def wipe_block(self):
        del self.block

    def build_block(self, *args, **kwargs):
        update_patcher = patch.object(Block, 'update_options')
        self.mock_update = update_patcher.start()
        self.addCleanup(update_patcher.stop)
        full_options_patcher = patch.object(
            Block,
            'full_options',
            return_value=self.PARENT_OPTIONS
        )
        self.mock_full_options = full_options_patcher.start()
        self.addCleanup(full_options_patcher.stop)
        move_patcher = patch.object(
            Block,
            'move_to_working_directory'
        )
        move_patcher.start()
        validate_patcher = patch.object(Block, 'validate')
        validate_patcher.start()
        self.block = Block(*args, **kwargs)
        validate_patcher.stop()
        move_patcher.stop()
        self.mock_update.reset_mock()
        self.mock_full_options.reset_mock()
        self.addCleanup(self.wipe_block)


class LoadUnitTests(BlockTestCase):

    @patch(
        'wotw_highlighter.block.BlockLoader'
    )
    def test_load(self, mock_loader):
        mock_loader.return_value = MagicMock(
            load=MagicMock(),
            full_options=MagicMock(
                return_value=BlockTestCase.CHILD_OPTIONS
            )
        )
        self.block.load()
        mock_loader.assert_has_calls([
            call(**BlockTestCase.PARENT_OPTIONS),
            call().load(),
            call().full_options()
        ])
        self.mock_update.assert_called_once_with(**BlockTestCase.CHILD_OPTIONS)


class HighlightUnitTests(BlockTestCase):

    @patch(
        'wotw_highlighter.block.BlockHighlighter'
    )
    def test_highlight(self, mock_highlighter):
        mock_highlighter.return_value = MagicMock(
            full_options=MagicMock(
                return_value=BlockTestCase.CHILD_OPTIONS
            )
        )
        self.block.highlight()
        mock_highlighter.assert_has_calls([
            call(**BlockTestCase.PARENT_OPTIONS),
            call().attach_lexer(),
            call().attach_formatter(),
            call().highlight(),
            call().full_options()
        ])
        self.mock_update.assert_called_once_with(**BlockTestCase.CHILD_OPTIONS)


class StyleUnitTests(BlockTestCase):

    @patch(
        'wotw_highlighter.block.BlockStyler'
    )
    def test_style(self, mock_styler):
        mock_styler.return_value = MagicMock(
            full_options=MagicMock(
                return_value=BlockTestCase.CHILD_OPTIONS
            )
        )
        self.block.style()
        mock_styler.assert_has_calls([
            call(**BlockTestCase.PARENT_OPTIONS),
            call().set_styles(),
            call().full_options()
        ])
        self.mock_update.assert_called_once_with(**BlockTestCase.CHILD_OPTIONS)


class DecorateUnitTests(BlockTestCase):

    @patch(
        'wotw_highlighter.block.BlockDecorator'
    )
    def test_decorate(self, mock_decorator):
        mock_decorator.return_value = MagicMock(
            full_options=MagicMock(
                return_value=BlockTestCase.CHILD_OPTIONS
            )
        )
        self.block.decorate()
        mock_decorator.assert_has_calls([
            call(**BlockTestCase.PARENT_OPTIONS),
            call().decorate(),
            call().full_options()
        ])
        self.mock_update.assert_called_once_with(**BlockTestCase.CHILD_OPTIONS)


class CompileUnitTests(BlockTestCase):

    @patch.object(Block, 'load')
    @patch.object(Block, 'highlight')
    @patch.object(Block, 'style')
    @patch.object(Block, 'decorate')
    def test_compile(self, mock_decorate, mock_style, mock_highlight, mock_load):
        runner = MagicMock()
        runner.attach_mock(mock_load, 'load')
        runner.attach_mock(mock_highlight, 'highlight')
        runner.attach_mock(mock_style, 'style')
        runner.attach_mock(mock_decorate, 'decorate')
        self.block.compile()
        runner.assert_has_calls([
            call.load(),
            call.highlight(),
            call.style(),
            call.decorate()
        ])
