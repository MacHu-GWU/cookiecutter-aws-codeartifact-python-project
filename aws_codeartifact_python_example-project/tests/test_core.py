# -*- coding: utf-8 -*-

from aws_codeartifact_python_example.core import hello


def test_hello():
    assert hello("alice") == "Hello alice"


if __name__ == "__main__":
    from aws_codeartifact_python_example.tests import run_cov_test

    run_cov_test(__file__, "aws_codeartifact_python_example.core", preview=False)
