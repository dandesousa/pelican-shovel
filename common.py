#!/usr/bin/env python

import os
import sys
import datetime as dt

from shovel import task

sys.path.append(os.getcwd())
import pelicanconf

CURRENT_DIRECTORY=os.getcwd()
CONTENT_DIRECTORY=os.path.join(CURRENT_DIRECTORY, "content")

NOW=dt.datetime.now()
POST_DIRECTORY=os.path.join(CONTENT_DIRECTORY, "posts", NOW.strftime("%Y/%m"))

