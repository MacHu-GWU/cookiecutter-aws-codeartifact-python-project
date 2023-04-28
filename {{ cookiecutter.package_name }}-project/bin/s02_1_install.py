#!/usr/bin/env python
# -*- coding: utf-8 -*-

from automation.codeartifact import poetry_authorization
from automation.deps import pip_install, poetry_install

# pip_install()
poetry_authorization()
poetry_install()
