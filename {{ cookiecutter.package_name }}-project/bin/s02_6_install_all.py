#!/usr/bin/env python
# -*- coding: utf-8 -*-

from automation.codeartifact import poetry_authorization
from automation.deps import pip_install_all, poetry_install_all

# pip_install_all()
poetry_authorization()
poetry_install_all()
