# -*- coding: utf-8 -*-

"""
Parse the ``pyproject.toml`` file.
"""

import dataclasses
from pathlib import Path

import tomli

dir_project_root = Path(__file__).absolute().parent.parent.parent
path_pyproject_toml = dir_project_root / "pyproject.toml"


@dataclasses.dataclass
class PyProject:
    package_name: str = dataclasses.field()
    package_version: str = dataclasses.field()
    python_version: str = dataclasses.field()
    aws_profile: str = dataclasses.field()
    aws_codeartifact_domain: str = dataclasses.field()
    aws_codeartifact_repository: str = dataclasses.field()

    @classmethod
    def new(cls):
        toml_dict = tomli.loads(path_pyproject_toml.read_text())
        package_name = toml_dict["tool"]["poetry"]["name"]
        package_version = toml_dict["tool"]["poetry"]["version"]

        # good example: ^3.8.X
        _python_version = toml_dict["tool"]["poetry"]["dependencies"]["python"]
        _python_version_info = [
            token.strip()
            for token in (
                "".join(
                    [char if char.isdigit() else " " for char in _python_version]
                ).split()
            )
            if token.strip()
        ]
        python_version = f"{_python_version_info[0]}.{_python_version_info[1]}"
        aws_profile = toml_dict["tool"]["aws"]["aws_profile"]
        aws_codeartifact_domain = toml_dict["tool"]["aws"]["aws_codeartifact_domain"]
        aws_codeartifact_repository = toml_dict["tool"]["aws"][
            "aws_codeartifact_repository"
        ]
        return cls(
            package_name=package_name,
            package_version=package_version,
            python_version=python_version,
            aws_profile=aws_profile,
            aws_codeartifact_domain=aws_codeartifact_domain,
            aws_codeartifact_repository=aws_codeartifact_repository,
        )

    @property
    def normalized_package_name(self) -> str:
        return self.package_name.replace("_", "-")

    @property
    def poetry_secondary_source_name(self) -> str:
        return self.aws_codeartifact_repository.replace("-", "_")


pyproject = PyProject.new()
