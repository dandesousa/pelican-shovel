#!/usr/bin/env python

from common import *
from jinja2 import Environment, FileSystemLoader

POST_DIRECTORY=os.path.join(CONTENT_DIRECTORY, "posts")
TODAYS_POST_DIRECTORY=os.path.join(POST_DIRECTORY, NOW.strftime("%Y/%m"))

@task
def new(markup=DEFAULT_MARKUP,**kwargs):
  """Handles creation of a new post."""
  
  env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))
  if markup in MARKUP_MARKDOWN_LIST:
    template = env.get_template("post-markdown.j2")
    extension = MARKDOWN_EXTENSION
  else:
    sys.stderr.write("Unable to find template for markup type: '%s'\n" % (markup))
    sys.exit(1)
    
  try:
    if not os.path.exists(TODAYS_POST_DIRECTORY):
      os.makedirs(TODAYS_POST_DIRECTORY)
  except OSError as exc:
    sys.stderr.write("Unable to write directory '%s', error: '%s'\n" % (TODAYS_POST_DIRECTORY, str(exc)))
    sys.exit(2)

  tdict = dict()
  title=kwargs.get("title", "My Post")
  (slug, path) = new_slug_and_path_from_title(title, extension, TODAYS_POST_DIRECTORY)
  tdict["title"]=title
  tdict["date"]=NOW.strftime("%Y-%m-%d %H:%M")
  tdict["tags"]=kwargs.get("tags","")
  tdict["category"]=kwargs.get("category","")
  tdict["slug"]=slug
  tdict["author"]=pelicanconf.AUTHOR
  tdict["summary"]=""

  with open(path, "w") as f:
    f.write(template.render(**tdict))

  if EDITOR:
    subprocess.call([EDITOR, path])
  else:
    sys.stderr.write("Unable to open editor with command: `%s %s`\n" % ( EDITOR, path ))
  
  print "Post created at: %s" % (path)

@task
def list(**kwargs):
  """Lists posts according to user options"""

  files = []
  should_edit = 'edit' in kwargs
  if not len(kwargs):
    # list all posts
    files = find_files(POST_DIRECTORY)
  elif 'search' in kwargs:
    # case insensitive search
    import re
    pattern = kwargs['search']
    files = find_files(POST_DIRECTORY, lambda x: re.search(pattern, x, re.IGNORECASE))
  else:
    sys.stderr.write("Received unexpected argument combination, expecting 0 arguments or --search <pattern>\n")
    sys.exit(1)

  for f in files:
    print f

    if EDITOR and should_edit:
      subprocess.call([EDITOR, f])
    elif should_edit:
      sys.stderr.write("Unable to open editor with command: `%s %s`\n" % ( EDITOR, path ))
      sys.exit(1)

