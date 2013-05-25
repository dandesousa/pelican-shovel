#!/usr/bin/env python

from common import *

POST_DIRECTORY=os.path.join(CONTENT_DIRECTORY, "posts")
TODAYS_POST_DIRECTORY=os.path.join(POST_DIRECTORY, NOW.strftime("%Y/%m"))

@task
def new(**kwargs):
  """Handles creation of a new post."""
  file_information = get_file_render_information("post", "markdown")
  create_new_pelican_file(file_information, TODAYS_POST_DIRECTORY, kwargs)

@task
def list(**kwargs):
  """Lists posts according to user options"""
  list_pelican_files(POST_DIRECTORY, kwargs)
