#!/usr/bin/env python
# -*- coding: utf-8 -*-

from automation.codeartifact import poetry_authorization
from automation.deps import poetry_lock

poetry_authorization()
poetry_lock()
