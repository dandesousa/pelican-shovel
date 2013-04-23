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

# Format Definitions
MARKUP_MARKDOWN_LIST=["markdown", "mkd", "md"]
MARKDOWN_EXTENSION="md"

# User Options (TODO: Move this eventually)
DEFAULT_MARKUP="markdown"

'''Common Functions'''
def slugify(title):
  """Simple function that turns a title into a slug"""
  return title.lower().replace(" ", "-")

def new_slug_and_path_from_title(title, ext, directory, append=0):
  """Simple function that returns a slug and path to a non-existent file suitable for a new file"""
  slugified = slugify(title)
  slug = slugified if not append else "%s-%s" % (slugified, append)
  file_name = "%s.%s" % ( slug, ext )
  path = os.path.join(directory, file_name)
  
  if os.path.exists(path):
    return new_slug_and_path_from_title(title, ext, directory, append + 1)

  return (slug, path) 

def find_files(target_directory, filter_func=None):
  """Returns a list of all files under the given target directory."""
  ret = []
  for root, dirs, files in os.walk(target_directory):
    ret += [os.path.join(root, f) for f in filter(filter_func,files)]
  return ret


