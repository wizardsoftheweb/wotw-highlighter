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

    def validate_git_directory(self):
        """Ensures the blob_working_directory is a git repo"""
        try:
            check_call(
                ['git', 'status'],
                stdout=self.DEV_NULL,
                stderr=self.DEV_NULL,
            )
        except CalledProcessError:
            raise ValueError(
                "'%s' is not a git repo"
                % (
                    self.blob_working_directory,
                )
            )

    def validate_git_ref_name(self):
        """Ensures the provided ref name exists"""
        try:
            check_call(
                ['git', 'rev-parse', '--verify', self.git_ref_name],
                stdout=self.DEV_NULL,
                stderr=self.DEV_NULL,
            )
        except CalledProcessError:
            raise ValueError(
                "'%s' is not a valid git ref in %s"
                % (
                    self.git_ref_name,
                    self.blob_working_directory,
                )
            )

    def validate_git_hash(self, git_hash):
        """Ensures the provided hash exists"""
        try:
            check_call(
                ['git', 'rev-parse', '--verify', git_hash],
                stdout=self.DEV_NULL,
                stderr=self.DEV_NULL,
            )
        except CalledProcessError:
            raise ValueError(
                "'%s' is not a valid git hash in %s"
                % (
                    git_hash,
                    self.blob_working_directory,
                )
            )
