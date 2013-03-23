#!/usr/bin/env python

import os
import sys
import datetime as dt

from shovel import task

sys.path.append(os.getcwd())
import pelicanconf

CURRENT_DIRECTORY=os.getcwd()
CONTENT_DIRECTORY=os.path.join(CURRENT_DIRECTORY, "content")
TEMPLATES_DIRECTORY=os.path.join(CURRENT_DIRECTORY, "shovel", "templates")

NOW=dt.datetime.now()

import subprocess
EDITOR=subprocess.check_output(["git", "config", "--get", "core.editor"]).strip()
