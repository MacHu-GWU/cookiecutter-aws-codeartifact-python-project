# -*- coding: utf-8 -*-

"""
This module implements the Git branch strategy related automation.

- main branch:
    - name pattern: exactly equal to ``main`` or ``master``
- dev branch:
    - name pattern: starts with ``dev``
- feature branch:
    - name pattern: starts with ``feat`` or ``feature``
- release branch:
    - name pattern: starts with ``rls`` or ``release``
"""

import os
import subprocess

from .paths import dir_project_root, temp_current_dir
from .runtime import IS_LOCAL, IS_CI
from .logger import logger


def get_git_branch_from_git_cli() -> str:
    """
    Use ``git`` CLI to get the current git branch.

    Run:

    .. code-block:: bash

        git branch --show-current
    """
    try:
        with temp_current_dir(dir_project_root):
            args = ["git", "branch", "--show-current"]
            res = subprocess.run(args, capture_output=True, check=True)
            branch = res.stdout.decode("utf-8").strip()
            return branch
    except Exception as e:
        logger.error(f"failed to get git branch from git CLI: {e}")
        return "unknown"


def get_git_commit_id_from_git_cli() -> str:
    """
    Use ``git`` CIL to get current git commit id.

    Run:

    .. code-block:: bash

        git rev-parse HEAD
    """
    try:
        with temp_current_dir(dir_project_root):
            args = ["git", "rev-parse", "HEAD"]
            res = subprocess.run(
                args,
                capture_output=True,
                check=True,
            )
            commit_id = res.stdout.decode("utf-8").strip()
            return commit_id
    except Exception as e:
        logger.error(f"failed to get git commit id from git CLI: {e}")
        return "unknown"


def get_commit_message_by_commit_id(commit_id: str) -> str:
    """
    Get the first line of commit message.

    Run:

    .. code-block:: bash

        git log --format=%B -n 1 ${commit_id}
    """
    args = ["git", "log", "--format=%B", "-n", "1", commit_id]
    response = subprocess.run(args, capture_output=True)
    message = response.stdout.decode("utf-8")
    message = message.strip().split("\n")[0].replace("'", "").replace('"', "").strip()
    return message


def is_master_branch(git_branch: str) -> bool:
    return git_branch.lower() in ["master", "main"]


def is_dev_branch(git_branch: str) -> bool:
    return git_branch.lower().startswith("dev")


def is_feature_branch(git_branch: str) -> bool:
    git_branch = git_branch.lower()
    return git_branch.startswith("feat") or git_branch.startswith("feature")


def is_release_branch(git_branch: str) -> bool:
    git_branch = git_branch.lower()
    return git_branch.startswith("rls") or git_branch.startswith("release")


if IS_LOCAL:
    GIT_COMMIT_ID: str = get_git_commit_id_from_git_cli()
    GIT_COMMIT_MESSAGE: str = ""
    GIT_BRANCH_NAME: str = get_git_branch_from_git_cli()
    PR_FROM_BRANCH_NAME: str = ""
    PR_TO_BRANCH_NAME: str = ""
    GIT_EVENT: str = ""
elif IS_CI:
    GIT_COMMIT_ID: str = os.environ.get("CI_DATA_COMMIT_ID", "")
    GIT_COMMIT_MESSAGE: str = os.environ.get("CI_DATA_COMMIT_MESSAGE", "")
    GIT_BRANCH_NAME: str = os.environ.get("CI_DATA_BRANCH_NAME", "")
    PR_FROM_BRANCH_NAME: str = os.environ.get("CI_DATA_PR_FROM_BRANCH", "")
    PR_TO_BRANCH_NAME: str = os.environ.get("CI_DATA_PR_TO_BRANCH", "")
    GIT_EVENT: str = os.environ.get("CI_DATA_EVENT_TYPE", "")
else:
    raise NotImplementedError


def print_git_info():
    logger.info(f"Current git branch is ⤵️ {GIT_BRANCH_NAME!r}")
    logger.info(f"Current git commit is ✅ {GIT_COMMIT_ID!r}")


IS_MASTER_BRANCH: bool = is_master_branch(GIT_BRANCH_NAME)
IS_DEV_BRANCH: bool = is_dev_branch(GIT_BRANCH_NAME)
IS_FEATURE_BRANCH: bool = is_feature_branch(GIT_BRANCH_NAME)
IS_RELEASE_BRANCH: bool = is_release_branch(GIT_BRANCH_NAME)

IS_PR_MERGE_EVENT: bool = GIT_EVENT == "pr_merged"
IS_PR_TARGET_MASTER_BRANCH: bool = is_master_branch(PR_TO_BRANCH_NAME)
