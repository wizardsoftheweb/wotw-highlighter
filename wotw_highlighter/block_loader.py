"""This file provides a class to load code"""
from os import devnull
from subprocess import CalledProcessError, check_call

from wotw_highlighter.block_options import BlockOptions


class BlockLoader(BlockOptions):
    """
    This class provides a collection of methods to load a file from either a
    local or git tree
    """

    DEV_NULL = open(devnull, 'w+')

    working_directory = 'blob_working_directory'
