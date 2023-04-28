{{ cookiecutter.package_name }}
==============================================================================


1. Overview
------------------------------------------------------------------------------
People love Python because of its active, high-quality open-source community. As an enterprise, you may want to publish "shared" Python libraries for internal use only. However, it might be painful to hire an engineering team to set up and maintain your enterprise Nexus Repository server. AWS CodeArtifact is a fully-managed service that makes it easy to securely store and share Python packages within your organization. This sample project is a reference implementation that includes all of the automation scripts and code structure setup for the enterprise. It also defines a software engineer development workflow that can be used as an internal standard for your enterprise. It is a good starting point for your enterprise to publish Python libraries for internal use only.

Disclaimer:

    All the best practices used in this repository are based on my career experience and personal opinion. I have completed over 90 public-facing Python open-source projects and 20 internal-facing Python shared libraries in the enterprise. This is the best practice I have been using for years. On average, it takes an enterprise weeks to set up one project like this with proper testing, CI/CD, and publishing strategy. This project template saves me effort in setting up the code structure, allows me to focus on the business logic, and greatly reduces the releasing cycle. Again, this is my personal best practice, so please use it at your own risk.

Concepts:

- **Python library project**: Similar to a pip-installable `open-source project <https://pypi.org/project/pandas/>`_, but only accessible within the enterprise. It should not be used directly but instead should be imported and used. The dependencies in this type of project typically have a wider range and may support multiple Python versions and even operating systems. It should be fully tested, with no less than 95% code coverage, and come with documentation, a changelog, and a stable public API. **This sample project is a Python library project**.
- **Python application project**: This is the backend implementation of an enterprise application that serves production traffic. The dependencies in this type of project are determinative and immutable to ensure the stability of the application. For example, it may only support specific Python versions and have all dependencies' versions fixed.
- Python repository: Similar to PyPI, it is a system that stores all the libraries you want to install from the pip install command. PyPI is the public-facing repository. For private libraries, enterprises usually use `Nexus Repository <https://www.sonatype.com/products/sonatype-nexus-repository>`_ or `AWS CodeArtifact <https://aws.amazon.com/codeartifact/>`_. You have to set up a cluster, install Nexus, and manage it yourself. AWS CodeArtifact is a fully managed service. You only need to create a domain and a repository, and then you can start using it.


2. How AWS Artifacts works with Python tools
------------------------------------------------------------------------------
First, let's understand how it works.


2.1 Publish to AWS CodeArtifact
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`Twine <https://twine.readthedocs.io/en/stable/>`_ is the Python official tool for publishing Python packages to PyPI and other repositories. You can use `AWS CLI <https://aws.amazon.com/cli/>`_ to authenticate twine to AWS CodeArtifacts. The following command will create a new profile named ``codeartifact`` in ``${HOME}/.pypirc`` and add the authentication information to it.

.. code-block:: bash

    aws codeartifact login --tool twine \
        --domain ${codeartifact_domain_name} \
        --domain-owner ${aws_account_id} \
        --repository ${codeartifact_repository_name} \
        --profile ${optional_aws_profile_name}

The content of ``${HOME}/.pypirc`` will look like this::

    [distutils]
    index-servers =
        pypi
        codeartifact

    [codeartifact]
    repository = https://${codeartifact_domain_name}-${aws_account_id}.d.codeartifact.{{ cookiecutter.aws_region }}.amazonaws.com/pypi/${codeartifact_repository_name}/
    username = aws
    password = 1a2b3c4d****

Then, you can use the following command to build the distribution package and upload to your private repository:

.. code-block:: bash

    # build distribution package and put them in dist/ folder
    poetry build

    # upload everything in the dist/ folder to AWS CodeArtifact
    twine upload dist/* --repository codeartifact


2.2 Install Libraries from AWS CodeArtifact
------------------------------------------------------------------------------
By default, pip or other Python package manager tools follow a priority to search for a package. Usually, the first priority is the public PyPI, and the second priority is the private repository. If a package is not found in the public PyPI, then it will search in the AWS CodeArtifact. However, you have to configure the package manager tool to add the AWS CodeArtifact as the secondary source and set up the credential. In this tutorial, we use ``poetry`` as the package manager tool.

Firstly, you can use the following Python code to get the repository endpoint. The endpoint follows this convention ``https://${codeartifact_domain_name}-${aws_account_id}.d.codeartifact.${aws_region}.amazonaws.com/pypi/${codeartifact_repository_name}/``.

.. code-block:: python

    import boto3

    codeartifact_client = boto3.client("codeartifact")
    res = codeartifact_client.get_repository_endpoint(
        domain="aws codeartifact domain name here",
        repository="aws codeartifact repository name here",
        format="pypi",
    )
    repository_endpoint = res["repositoryEndpoint"]
    print(repository_endpoint)

Secondly, you can use the following command to add AWS CodeArtifact as the secondary source. Note that you have to append ``simple/`` to the end of the domain URL. Although AWS CodeArtifact does not support the ``/simple/`` API endpoint, it supports the ``/simple/<project>/`` endpoint. The ``${custom_secondary_source_name}`` is just a user-friendly name for the secondary source. You can use any name you want, but you cannot use ``-`` (hyphen) and should only use ``_`` (underscore). This name is important because you will use it later for authentication.

.. code-block:: bash

    poetry source add --secondary ${custom_secondary_source_name} "https://${codeartifact_domain_name}-${aws_account_id}.d.codeartifact.${aws_region}.amazonaws.com/pypi/${codeartifact_repository_name}/simple/"

Then, you can set environment variables to allow Poetry to authenticate with AWS CodeArtifact. ``POETRY_HTTP_BASIC_${custom_secondary_source_name_in_upper_case}_USERNAME`` and ``POETRY_HTTP_BASIC_${custom_secondary_source_name_in_upper_case}_PASSWORD`` store the username and password pair. The ``${custom_secondary_source_name_in_upper_case}`` part must match the Poetry secondary source name. For example, if ``${custom_secondary_source_name}`` is ``hello_world``, then the environment variable names should be ``POETRY_HTTP_BASIC_HELLO_WORLD_USERNAME`` and ``POETRY_HTTP_BASIC_HELLO_WORLD_PASSWORD``. The username is always ``aws``, and the password is from the ``aws codeartifact get-authorization-token ...`` command. Note that credentials might be saved in your shell history, so the following command is more secure as it passes the token directly as an environment variable.

    export POETRY_HTTP_BASIC_${custom_secondary_source_name_in_upper_case}_USERNAME=aws
    export POETRY_HTTP_BASIC_${custom_secondary_source_name_in_upper_case}_PASSWORD=$(aws codeartifact get-authorization-token --domain ${codeartifact_domain_name} --query 'authorizationToken' --output text --profile ${aws_cli_profile_name)

From now, you can use ``poetry lock``, ``poetry install`` as usual.

Reference:

- `Configure and use pip with CodeArtifact <https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-pip.html>`_: this is AWS official document for how to use twine with CodeArtifact.
- `Configure and use twine with CodeArtifact <https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-twine.html>`_: this is AWS official document for how to use twine with CodeArtifact.
- `Poetry and Python Repositories <https://python-poetry.org/docs/repositories/>`_: this is a good reference for how to use poetry with private repositories.


3. Git Branching Strategy
------------------------------------------------------------------------------
As a developer or an engineering group, it is great to have a standard, automated development workflow that is properly documented (which is what we have here) so that everyone can follow and move rapidly. Below is the diagram of the trunk-based workflow used in this project:

.. raw:: html
    :file: ./git-branching-strategy.drawio.html

Firstly you have to install some dependencies for CLI automation. You only need to do this once when you got a new laptop:

.. code-block:: bash

    pip install twine --quiet --disable-pip-version-check
    pip install poetry==1.2.2 --quiet --disable-pip-version-check
    pip install -r requirements-automation.txt --quiet --disable-pip-version-check

Secondly you have to add AWS CodeArtifact as the secondary source to poetry. You only need to do this once for each Python library project like this:

.. code-block:: bash

    poetry-add-source

Then you can create a virtual environment and start doing development:

.. code-block:: bash

    # create virtualenv environment
    make venv-create

    # (optional) resolve determinative dependencies using poetry
    # you have to redo this everytime you changed the dependencies in pyproject.toml file
    make poetry-lock

    # install dependencies
    make install-all

    # (optional) you can use the following command to install only necessary dependencies as well
    # Install main dependencies and Package itself
    make install
    # Install Development Dependencies
    make install-dev
    # Install Test Dependencies
    make install-test
    # Install Document Dependencies
    make install-doc
    # Install Dependencies for Automation Script
    make install-automation

Once you finished your development, you should run the following command to run code coverage test:

.. code-block:: bash

    make cov

Then you can create a pull request to merge your code to the ``main`` branch.

When you are ready to release a new version, you can create a ``release`` branch and create a pull request to merge your code to the ``main``. From this point, you only update document, release note and version number in the ``release`` branch. And the CI should automatically build and release the package to AWS CodeArtifact.
