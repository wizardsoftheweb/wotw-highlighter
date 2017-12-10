# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0613

from unittest import TestCase

from mock import patch

from wotw_highlighter import Block


class BlockTestCase(TestCase):

    def setUp(self):
        self.build_block()

    def wipe_block(self):
        del self.block_decorator

    def build_block(self, *args, **kwargs):
        update_patcher = patch.object(Block, 'update_options')
        update_patcher.start()
        move_patcher = patch.object(
            Block, 'move_to_working_directory')
        move_patcher.start()
        validate_patcher = patch.object(Block, 'validate')
        validate_patcher.start()
        self.block_decorator = Block(*args, **kwargs)
        validate_patcher.stop()
        move_patcher.stop()
        update_patcher.stop()
        self.addCleanup(self.wipe_block)
