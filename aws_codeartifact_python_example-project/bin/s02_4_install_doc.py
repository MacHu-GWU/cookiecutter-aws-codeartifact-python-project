#!/usr/bin/env python
# -*- coding: utf-8 -*-

from automation.codeartifact import poetry_authorization
from automation.deps import pip_install_doc, poetry_install_doc

# pip_install_doc()
poetry_authorization()
poetry_install_doc()
