# -*- coding: utf-8 -*-

from {{ cookiecutter.package_name }}.core import hello


def test_hello():
    assert hello("alice") == "Hello alice"


if __name__ == "__main__":
    from {{ cookiecutter.package_name }}.tests import run_cov_test

    run_cov_test(__file__, "{{ cookiecutter.package_name }}.core", preview=False)
