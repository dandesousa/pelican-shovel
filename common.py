#!/usr/bin/env python

#
# SETTINGS
#
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
import collections
MarkupDescription=collections.namedtuple("MarkupDescription", ["name", "extension"])

# Descriptions
MARKDOWN_DESCRIPTION = MarkupDescription("markdown", "md")

# Supported Descriptions
SUPPORTED_FORMATS = {
    'markdown' : MARKDOWN_DESCRIPTION,
    'mkd' : MARKDOWN_DESCRIPTION,
    'md' : MARKDOWN_DESCRIPTION
}

# User Options (TODO: Move this eventually)
DEFAULT_MARKUP="markdown"


#
# HELPER FUNCTIONS
#
FileInformation=collections.namedtuple("FileInformation", ["template", "extension"])

def get_file_render_information(template_base_str,markup):
  markup_definition = SUPPORTED_FORMATS.get(markup, DEFAULT_MARKUP)
  _template_name = "%s-%s.j2" % (template_base_str, markup_definition.name)
  return FileInformation(_template_name, markup_definition.extension)

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


#
# TASKS
#

from jinja2 import Environment, FileSystemLoader

def create_new_pelican_file(file_info,directory,kwargs):
  """Creates a new pelican file at the given location with a slugified name using the template.
  """
  env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))
  template = env.get_template(file_info.template)

  try:
    if not os.path.exists(directory):
      os.makedirs(directory)
  except OSError as exc:
    sys.stderr.write("Unable to create non-existent directory '%s', error: '%s'\n" % (directory, str(exc)))
    sys.exit(2)

  tdict = dict()
  title = kwargs.get("title", "My New Entry")
  tdict["title"] = title
  
  (slug, path) = new_slug_and_path_from_title(title, file_info.extension, directory)
  if kwargs.get("hidden", False):
    tdict["status"] = "hidden"
  tdict["date"] = NOW.strftime("%Y-%m-%d %H:%M")
  tdict["author"] = pelicanconf.AUTHOR

  # post fields
  tdict["tags"] = kwargs.get("tags", "")
  tdict["category"] = kwargs.get("category", "")
  tdict["slug"] = slug 
  tdict["summary"] = ""

  with open(path, "w") as f:
    f.write(template.render(**tdict))

  if EDITOR:
    subprocess.call([EDITOR, path])
  else:
    sys.stderr.write("Unable to open editor with command: `%s %s`\n" % ( EDITOR, path ))

  print "Create file at: %s" % (path)

def list_pelican_files(directory, kwargs):
  files = []
  should_edit = 'edit' in kwargs
  if not len(kwargs):
    files = find_files(directory)
  elif 'search' in kwargs:
    # case insensitive search
    import re 
    pattern = kwargs['search']
    files = find_files(directory, lambda x: re.search(pattern, x, re.IGNORECASE))
  else:
    sys.stderr.write("Received unexpected argument combination, expecting 0 arguments or --search <pattern>\n")
    sys.exit(1)

  for f in files:
    print f

    if EDITOR and should_edit:
      subprocess.call([EDITOR, f])
    elif should_edit:
      sys.stderr.write("Unable to open editor with command: '%s %s'\n" % ( EDITOR, path ))
      sys.exit(1)
