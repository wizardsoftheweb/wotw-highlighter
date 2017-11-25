"""This file provides a class to provide styling"""

from os.path import dirname, join

from wotw_highlighter.block_options import BlockOptions


class BlockStyler(BlockOptions):
    """This class provides styles for a highlighted_blob"""

    @staticmethod
    def dump_pygments_styles():
        """Dumps all the styles from Pygments"""
        with open(
            join(
                dirname(__file__),
                'data',
                'pygments-monokai.css'
            ),
            'r'
        ) as css_file:
            styles = css_file.read()
            return styles.strip()
