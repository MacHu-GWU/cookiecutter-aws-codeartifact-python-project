``cookiecutter-aws-codeartifact-python-project``
==============================================================================


Overview
------------------------------------------------------------------------------
This is an AWS CodeArtifact Python library project template with CI/CD setup. You can easily generate a folder structure as a foundation,then plugin your business code, then go to production.

People love Python because of its active, high-quality open-source community. As an enterprise, you may want to publish "shared" Python libraries for internal use only. However, it might be painful to hire an engineering team to set up and maintain your enterprise Nexus Repository server. AWS CodeArtifact is a fully-managed service that makes it easy to securely store and share Python packages within your organization. This sample project is a reference implementation that includes all of the automation scripts and code structure setup for the enterprise. It also defines a software engineer development workflow that can be used as an internal standard for your enterprise. It is a good starting point for your enterprise to publish Python libraries for internal use only.


Disclaimer
------------------------------------------------------------------------------
All the best practices used in this repository are based on my career experience and personal opinion. I have completed over 90 public-facing Python open-source projects and 20 internal-facing Python shared libraries in the enterprise. This is the best practice I have been using for years. On average, it takes an enterprise weeks to set up one project like this with proper testing, CI/CD, and publishing strategy. This project template saves me effort in setting up the code structure, allows me to focus on the business logic, and greatly reduces the releasing cycle. Again, this is my personal best practice, so please use it at your own risk.


Usage
------------------------------------------------------------------------------
Enter the following command, it will use the latest template.

.. code-block:: bash

    pip install cookiecutter
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-codeartifact-python-project

Or, you can use a specific released version, you can find `full list of release at here <https://github.com/MacHu-GWU/cookiecutter-aws-codeartifact-python-project/releases>`_.

.. code-block:: bash

    # use specific version
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-codeartifact-python-project --checkout tags/${version}
    # for example (v5 is the latest as of 2023-04-28)
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-codeartifact-python-project --checkout tags/v1

Then fill in some information::

    package_name [my_package]: ...
    author_name [Firstname Lastname]: ...
    author_email [firstname.lastname@email.com]: ...
    ...

Then it will generate a Git repo folder structures like this:

- ``/bin/*.py``: binary executable scripts for automation, devops, CI/CD
- ``/${package_name}/...`` your python project source code
- ``/tests/...``: unit test
- ``/.coveragerc``: code coverage test config
- ``/Makefile``: the automation script CLI tools for local development
- ``/pyproject.toml`` and ``/poetry.lock``: determinative dependency management
- (Optional) ``/codebuild-config.json`` and ``/buildspec.yml``: the CI/CD integration with AWS CodeBuild, but you can use any other CI/CD platform (GitHub Actions, Jenkins, CircleCI, GitLab pipeline, BitBucket, Pipeline, etc ...), and just copy and paste the following shell scripts to your CI workflow definition file::

.. code-block:: bash

    - pip install twine --quiet --disable-pip-version-check
    pip install poetry==1.2.2 --quiet --disable-pip-version-check
    pip install -r requirements-automation.txt --quiet --disable-pip-version-check
    python ./bin/s99_1_install_phase.py
    ./.venv/bin/python ./bin/s99_2_pre_build_phase.py
    ./.venv/bin/python ./bin/s99_3_build_phase.py
    ./.venv/bin/python ./bin/s99_4_post_build_phase.py

We have an example project generated from this template `aws_codeartifact_python-project <./aws_codeartifact_python-project>`_. Please take a look at it.
