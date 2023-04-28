# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager
from .runtime import IS_CI

if IS_CI:
    bsm = BotoSesManager()
else:
    bsm = BotoSesManager(profile_name="my_aws_profile")
