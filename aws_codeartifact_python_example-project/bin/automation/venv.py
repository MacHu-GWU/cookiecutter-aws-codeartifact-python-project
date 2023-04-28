# -*- coding: utf-8 -*-

"""
Virtualenv management.
"""

import sys
import shutil
import subprocess

from .pyproject import pyproject
from .paths import (
    dir_venv,
    bin_python,
    bin_pip,
    bin_pytest,
    bin_aws,
    path_poetry_lock,
)
from .runtime import IS_CI
from .helpers import sha256_of_bytes
from .logger import logger
from .emoji import Emoji


@logger.block(
    msg="Create Virtual Environment",
    start_emoji=Emoji.python,
    end_emoji=Emoji.python,
    pipe=Emoji.python,
)
def virtualenv_venv_create():
    """
    .. code-block:: bash

        $ virtualenv -p python${X}.${Y} ./.venv
    """
    if dir_venv.exists():
        logger.info(f"{dir_venv} already exists, do nothing.")
    else:
        subprocess.run(
            ["virtualenv", "-p", f"python{pyproject.python_version}", f"{dir_venv}"],
            check=True,
        )
        logger.info("done")


@logger.block(
    msg="Remove Virtual Environment",
    start_emoji=Emoji.python,
    end_emoji=Emoji.python,
    pipe=Emoji.python,
)
def venv_remove():
    """
    .. code-block:: bash

        $ rm -r ./.venv
    """
    if dir_venv.exists():
        subprocess.run(["rm", "-r", f"{dir_venv}"])
        logger.info(f"done! {dir_venv} is removed.")
    else:
        logger.info(f"{dir_venv} doesn't exists, do nothing.")
