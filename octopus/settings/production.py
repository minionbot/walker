# coding: utf-8
# Copyright © 2017  All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from __future__ import unicode_literals

import sys
import traceback
from split_settings.tools import optional, include
from .defaults import *

try:
    # include(settings_file, optional(settings_files), scope = locals())
    include(optional('online_*.py'), scope = locals())
    include('postprocess.py', scope = locals())
except ImportError:
    traceback.print_exc()
    sys.exit(1)
