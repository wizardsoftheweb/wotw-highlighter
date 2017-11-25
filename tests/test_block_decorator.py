# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0613

from unittest import TestCase

from mock import patch

from wotw_highlighter import BlockDecorator


class BlockDecoratorTestCase(TestCase):

    def setUp(self):
        self.build_decorator()

    def wipe_decorator(self):
        del self.block_decorator

    def build_decorator(self, *args, **kwargs):
        move_patcher = patch.object(
            BlockDecorator, 'move_to_working_directory')
        move_patcher.start()
        validate_patcher = patch.object(BlockDecorator, 'validate')
        validate_patcher.start()
        self.block_decorator = BlockDecorator(*args, **kwargs)
        validate_patcher.stop()
        move_patcher.stop()
        self.addCleanup(self.wipe_decorator)


class ValidateUnitTests(BlockDecoratorTestCase):

    def test_without_highlighted_code(self):
        self.block_decorator.highlighted_blob = None
        with self.assertRaisesRegexp(ValueError, 'Nothing to decorate'):
            self.block_decorator.validate()

    def test_with_highlighted_code(self):
        self.block_decorator.highlighted_blob = 'qqq'
        self.assertIsNone(self.block_decorator.validate())
