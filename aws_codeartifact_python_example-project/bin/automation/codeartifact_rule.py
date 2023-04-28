# -*- coding: utf-8 -*-

from .logger import logger
from .emoji import Emoji


def _do_we_publish(
    branch_name: str,
    is_release_branch: bool,
) -> bool:
    """
    In CI, we only run unit test when it is a branch that may cause
    application code change.

    we don't run unit test in prod environment because unit test may
    change the state of the cloud resources, and it should be already
    thoroughly tested in int environment.
    """
    if is_release_branch:
        return True
    else:
        logger.info(
            f"{Emoji.red_circle} don't publish to CodeArtifact, we only publish from "
            f"a 'release' branch in CI, we are now on {branch_name!r} branch."
        )
        return False


def do_we_publish(
    is_ci_runtime: bool,
    branch_name: str,
    is_release_branch: bool,
) -> bool:
    """
    Check if we should run unit test or coverage test.
    """
    if is_ci_runtime:
        return _do_we_publish(
            branch_name=branch_name,
            is_release_branch=is_release_branch,
        )
    else:  # always don't allow publish to codeartifact from Local
        logger.info(
            f"{Emoji.red_circle} don't publish to CodeArtifact from local laptop."
        )
        return False
