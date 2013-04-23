#!/usr/bin/env python

from common import *
from jinja2 import Environment, FileSystemLoader

PAGE_DIRECTORY=os.path.join(CONTENT_DIRECTORY, "pages")

@task
def new(markup="md",**kwargs):
  """Handles creation of a new page."""
  
  env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))
  if markup in MARKUP_MARKDOWN_LIST:
    template = env.get_template("page-markdown.j2")
    extension = MARKDOWN_EXTENSION
  else:
    sys.stderr.write("Unable to find template for markup type: '%s'\n" % (markup))
    sys.exit(1)
    
  try:
    if not os.path.exists(PAGE_DIRECTORY):
      os.makedirs(PAGE_DIRECTORY)
  except OSError as exc:
    sys.stderr.write("Unable to write directory '%s', error: '%s'\n" % (PAGE_DIRECTORY, str(exc)))
    sys.exit(2)

  tdict = dict()
  title=kwargs.get("title", "My Page")
  (slug, path) = new_slug_and_path_from_title(title, extension, PAGE_DIRECTORY)
  if kwargs.get("hidden", False):
    tdict["status"]="hidden"
  tdict["title"]=title
  tdict["date"]=NOW.strftime("%Y-%m-%d %H:%M")
  tdict["author"]=pelicanconf.AUTHOR

  with open(path, "w") as f:
    f.write(template.render(**tdict))

  if EDITOR:
    subprocess.call([EDITOR, path])
  else:
    sys.stderr.write("Unable to open editor with command: `%s %s`\n" % ( EDITOR, path ))
  
  print "Page created at: %s" % (path)

@task
def list(**kwargs):
  """Lists page according to user options"""

  files = []
  should_edit = 'edit' in kwargs
  if not len(kwargs):
    # list all pages
    files = find_files(PAGE_DIRECTORY)
  elif 'search' in kwargs:
    # case insensitive search
    import re
    pattern = kwargs['search']
    files = find_files(PAGE_DIRECTORY, lambda x: re.search(pattern, x, re.IGNORECASE))
  else:
    sys.stderr.write("Received unexpected argument combination, expecting 0 arguments or --search <pattern>\n")
    sys.exit(1)

  for f in files:
    print f
    
    if should_edit:
      if EDITOR:
        subprocess.call([EDITOR, f])
      else:
        sys.stderr.write("Unable to open editor with command: `%s %s`\n" % ( EDITOR, path ))
        sys.exit(1)

