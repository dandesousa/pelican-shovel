#!/usr/bin/env python

import os
from common import *

PAGE_DIRECTORY=os.path.join(CONTENT_DIRECTORY, "pages")

@task
def new(**kwargs):
  """Handles creation of a new page."""
  file_information = get_file_render_information("page", "markdown")
  create_new_pelican_file(file_information, PAGE_DIRECTORY, kwargs)
 
@task
def list(**kwargs):
  """Lists page according to user options"""
  list_pelican_files(PAGE_DIRECTORY, kwargs)
  
