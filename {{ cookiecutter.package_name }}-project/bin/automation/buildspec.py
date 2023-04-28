# -*- coding: utf-8 -*-

# helpers
from .logger import logger
from .emoji import Emoji

# actions
from .venv import (
    virtualenv_venv_create,
)
from .deps import (
    poetry_export,
    pip_install,
    pip_install_dev,
    pip_install_test,
    pip_install_automation,
)
from .tests import (
    run_cov_test,
)


@logger.block(
    msg="Install Phase",
    start_emoji=f"{Emoji.start} {Emoji.pre_build_phase}",
    end_emoji=Emoji.pre_build_phase,
    pipe=Emoji.pre_build_phase,
)
def install_phase():
    with logger.nested():
        virtualenv_venv_create()
        poetry_export()
        pip_install()
        pip_install_dev()
        pip_install_test()
        pip_install_automation()


@logger.block(
    msg="Pre Build Phase",
    start_emoji=f"{Emoji.start} {Emoji.pre_build_phase}",
    end_emoji=Emoji.pre_build_phase,
    pipe=Emoji.pre_build_phase,
)
def pre_build_phase():
    from .runtime import print_runtime_info
    from .git import print_git_info

    print_runtime_info()
    print_git_info()

    with logger.nested():
        run_cov_test()


@logger.block(
    msg="Build Phase",
    start_emoji=f"{Emoji.start} {Emoji.build_phase}",
    end_emoji=Emoji.build_phase,
    pipe=Emoji.build_phase,
)
def build_phase():
    pass


@logger.block(
    msg="Post Phase",
    start_emoji=f"{Emoji.start} {Emoji.post_build_phase}",
    end_emoji=Emoji.post_build_phase,
    pipe=Emoji.post_build_phase,
)
def post_build_phase():
    from .codeartifact import publish_to_codeartifact

    publish_to_codeartifact()
