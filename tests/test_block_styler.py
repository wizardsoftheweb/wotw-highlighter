# pylint: disable=w0201
# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0613
# pylint: disable=no-self-use

# from subprocess import CalledProcessError
from unittest import TestCase
from mock import MagicMock, patch

from wotw_highlighter import BlockStyler


class BlockStylerTestCase(TestCase):
    """Collects common items and defaults across test cases"""

    def setUp(self):
        self.build_styler()

    def wipe_styler(self):
        """Nukes the constructed styler"""
        del self.block_styler

    def build_styler(self, *args, **kwargs):
        """Constructs a basic styler using only the defaults"""
        move_patcher = patch.object(BlockStyler, 'move_to_working_directory')
        move_patcher.start()
        validate_patcher = patch.object(BlockStyler, 'validate')
        validate_patcher.start()
        self.block_styler = BlockStyler(*args, **kwargs)
        validate_patcher.stop()
        move_patcher.stop()
        self.addCleanup(self.wipe_styler)


class DumpPygmentsStyles(BlockStylerTestCase):
    FILE_CONTENTS = 'qqq'

    @patch(
        'wotw_highlighter.block_styler.open',
        return_value=MagicMock(
            __enter__=MagicMock(
                return_value=MagicMock(
                    read=MagicMock(return_value=FILE_CONTENTS)
                )
            )
        )
    )
    @patch(
        'wotw_highlighter.block_styler.dirname',
        return_value=''
    )
    def test_pygments_dump(self, mock_dirname, mock_open):  # pylint: disable=W0613
        self.assertEqual(
            BlockStyler.dump_pygments_styles(),
            self.FILE_CONTENTS
        )
        mock_open.assert_called_once_with('data/pygments-monokai.css', 'r')


class DumpAdditionalStyles(BlockStylerTestCase):
    FILE_CONTENTS = 'qqq'

    @patch(
        'wotw_highlighter.block_styler.open',
        return_value=MagicMock(
            __enter__=MagicMock(
                return_value=MagicMock(
                    read=MagicMock(return_value=FILE_CONTENTS)
                )
            )
        )
    )
    @patch(
        'wotw_highlighter.block_styler.dirname',
        return_value=''
    )
    def test_additions_dump(self, mock_dirname, mock_open):  # pylint: disable=W0613
        self.assertEqual(
            BlockStyler.dump_additional_styles(),
            self.FILE_CONTENTS
        )
        mock_open.assert_called_once_with(
            'data/pygments-monokai-additions.css', 'r')


class DumpStyles(BlockStylerTestCase):
    FILE_CONTENTS = 'qqq'

    @patch.object(BlockStyler, 'dump_additional_styles')
    @patch.object(BlockStyler, 'dump_pygments_styles')
    def test_full_dump(self, mock_pygment, mock_additional):  # pylint: disable=W0613
        BlockStyler.dump_styles()
        mock_pygment.assert_called_once_with()
        mock_additional.assert_called_once_with()
