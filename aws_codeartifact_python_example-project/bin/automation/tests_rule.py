# -*- coding: utf-8 -*-

from .logger import logger
from .emoji import Emoji


def _do_we_run_unit_test_in_ci(
    branch_name: str,
    is_master_branch: bool,
    is_dev_branch: bool,
    is_feature_branch: bool,
) -> bool:
    """
    In CI, we only run unit test when it is a branch that may cause
    application code change.

    we don't run unit test in prod environment because unit test may
    change the state of the cloud resources, and it should be already
    thoroughly tested in int environment.
    """
    if is_master_branch or is_dev_branch or is_feature_branch:
        return True
    else:
        logger.info(
            f"{Emoji.red_circle} don't run unit test, we only run unit test on a "
            f"'master', 'dev', 'feature' branch in CI, "
            f"we are now on {branch_name!r} branch"
        )
        return False


def do_we_run_unit_test(
    is_ci_runtime: bool,
    branch_name: str,
    is_master_branch: bool,
    is_dev_branch: bool,
    is_feature_branch: bool,
) -> bool:
    """
    Check if we should run unit test or coverage test.
    """
    if is_ci_runtime:
        return _do_we_run_unit_test_in_ci(
            branch_name=branch_name,
            is_master_branch=is_master_branch,
            is_dev_branch=is_dev_branch,
            is_feature_branch=is_feature_branch,
        )
    else:  # always run unit test on Local
        return True
