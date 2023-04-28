# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

from .boto_ses import bsm
from .pyproject import pyproject
from .paths import dir_project_root, dir_dist, temp_current_dir
from .logger import logger
from .emoji import Emoji
from .runtime import IS_CI
from .comment import post_comment_reply
from .git import GIT_BRANCH_NAME, IS_RELEASE_BRANCH
from .codeartifact_rule import do_we_publish


def _get_repository_endpoint() -> str:
    """
    reference:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/client/get_authorization_token.html
    """
    res = bsm.codeartifact_client.get_repository_endpoint(
        domain=pyproject.aws_codeartifact_domain,
        repository=pyproject.aws_codeartifact_repository,
        format="pypi",
    )
    return res["repositoryEndpoint"]


def _get_authorization_token() -> str:
    """
    reference:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/client/get_authorization_token.html
    """
    res = bsm.codeartifact_client.get_authorization_token(
        domain=pyproject.aws_codeartifact_domain,
    )
    return res["authorizationToken"]


@logger.block(
    msg="Add AWS CodeArtifact as secondary source",
    start_emoji=Emoji.package,
    end_emoji=Emoji.package,
    pipe=Emoji.package,
)
def poetry_source_add_codeartifact():
    """
    Run:

    .. code-block:: bash

        poetry source add --secondary ${source_name} "https://${domain_name}-${aws_account_id}.d.codeartifact.${aws_region}.amazonaws.com/pypi/${repository_name}/simple/"
    """
    endpoint = _get_repository_endpoint()
    args = [
        "poetry",
        "source",
        "add",
        "--secondary",
        pyproject.poetry_secondary_source_name,
        f"{endpoint}simple/",
    ]
    subprocess.run(args, check=True)


def poetry_authorization():
    """
    Set environment variables to allow Poetry to authenticate with CodeArtifact.
    """
    token = _get_authorization_token()
    source_name = pyproject.poetry_secondary_source_name.upper()
    os.environ[f"POETRY_HTTP_BASIC_{source_name}_USERNAME"] = "aws"
    os.environ[f"POETRY_HTTP_BASIC_{source_name}_PASSWORD"] = token


def _twine_authorization():
    """
    Run

    .. code-block:: bash

        aws codeartifact login --tool twine \
            --domain ${domain_name} \
            --domain-owner ${aws_account_id} \
            --repository ${repo_name} \
            --profile ${aws_profile}

    Reference:

    - `Configure and use twine with CodeArtifact <https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-twine.html>`_
    - `AWS CodeArtifact CLI <https://docs.aws.amazon.com/cli/latest/reference/codeartifact/index.html>`_
    """
    args = [
        "aws",
        "codeartifact",
        "login",
        "--tool",
        "twine",
        "--domain",
        pyproject.aws_codeartifact_domain,
        "--domain-owner",
        bsm.aws_account_id,
        "--repository",
        pyproject.aws_codeartifact_repository,
    ]
    if IS_CI is False:
        if pyproject.aws_profile:
            args.extend(["--profile", pyproject.aws_profile])

    subprocess.run(args, check=True)


def _twine_upload():
    """
    Upload Python package to CodeArtifact.

    Run

    .. code-block:: bash

        twine upload dist/* --repository codeartifact
    """
    console_url = (
        f"https://{bsm.aws_region}.console.aws.amazon.com/codesuite/codeartifact/d"
        f"/{bsm.aws_account_id}/{pyproject.aws_codeartifact_domain}/r"
        f"/{pyproject.aws_codeartifact_repository}/p/pypi/"
        f"{pyproject.normalized_package_name}/versions?region={bsm.aws_region}"
    )
    print(f"preview in AWS CodeArtifact console: {console_url}")
    _twine_authorization()
    args = ["twine", "upload", f"{dir_dist}/*", "--repository", "codeartifact"]
    with temp_current_dir(dir_project_root):
        subprocess.run(args, check=True)


def _poetry_build():
    shutil.rmtree(dir_dist, ignore_errors=True)
    args = [
        "poetry",
        "build",
    ]
    with temp_current_dir(dir_project_root):
        subprocess.run(args, check=True)


@logger.block(
    msg="Publish to AWS CodeArtifact",
    start_emoji=Emoji.package,
    end_emoji=Emoji.package,
    pipe=Emoji.package,
)
def publish_to_codeartifact(
    check: bool = True,
):
    """
    Publish your Python package to AWS CodeArtifact
    """
    try:
        res = bsm.codeartifact_client.describe_package_version(
            domain=pyproject.aws_codeartifact_domain,
            repository=pyproject.aws_codeartifact_repository,
            format="pypi",
            package=pyproject.normalized_package_name,
            packageVersion=pyproject.package_version,
        )
        message = (
            f"{Emoji.failed} {Emoji.package} package "
            f"{pyproject.normalized_package_name} = {pyproject.package_version} already exists!"
        )
        post_comment_reply(message=message, is_ci=IS_CI)
        raise Exception("package version already exists!")
    except Exception as e:
        if "does not exist" in str(e):
            pass
        else:
            raise e

    if check:
        if (
            do_we_publish(
                is_ci_runtime=IS_CI,
                branch_name=GIT_BRANCH_NAME,
                is_release_branch=IS_RELEASE_BRANCH,
            )
            is False
        ):
            return

    try:
        _poetry_build()
        _twine_upload()
        _post_comment_reply(succeeded=True, is_ci=IS_CI)
    except Exception as e:
        _post_comment_reply(succeeded=False, is_ci=IS_CI)
        raise e


def _post_comment_reply(
    succeeded: bool,
    is_ci: bool,
):
    """
    Post a comment reply to the CodeCommit PR thread when publish to
    AWS CodeArtifact is succeeded or failed.

    :param succeeded: we use this flag to generate the message
    :param is_ci: we only post reply from CI build job
    """
    console_url = (
        f"https://{bsm.aws_region}.console.aws.amazon.com/codesuite/codeartifact/d"
        f"/{bsm.aws_account_id}/{pyproject.aws_codeartifact_domain}/r"
        f"/{pyproject.aws_codeartifact_repository}/p/pypi/"
        f"{pyproject.package_name.replace('_', '-')}/versions?region={bsm.aws_region}"
    )
    if succeeded:
        lines = [
            f"{Emoji.succeeded} {Emoji.package} **publish to code artifact succeeded**",
            "" f"- preview in [AWS CodeArtifact console]({console_url})",
        ]
        message = "\n".join(lines)
    else:
        message = (
            f"{Emoji.failed} {Emoji.package} **publish to code artifact failed**"
        )
    post_comment_reply(message=message, is_ci=is_ci)
