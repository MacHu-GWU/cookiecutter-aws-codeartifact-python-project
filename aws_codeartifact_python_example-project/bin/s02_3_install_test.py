#!/usr/bin/env python
# -*- coding: utf-8 -*-

from automation.codeartifact import poetry_authorization
from automation.deps import pip_install_test, poetry_install_test

# pip_install_test()
poetry_authorization()
poetry_install_test()
