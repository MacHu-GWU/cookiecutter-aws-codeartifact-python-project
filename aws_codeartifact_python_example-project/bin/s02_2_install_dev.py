#!/usr/bin/env python
# -*- coding: utf-8 -*-

from automation.codeartifact import poetry_authorization
from automation.deps import pip_install_dev, poetry_install_dev

# pip_install_dev()
poetry_authorization()
poetry_install_dev()
