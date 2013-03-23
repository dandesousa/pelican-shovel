#!/usr/bin/env python

from common import *
from jinja2 import Environment, FileSystemLoader

POST_DIRECTORY=os.path.join(CONTENT_DIRECTORY, "posts", NOW.strftime("%Y/%m"))
MARKUP_MARKDOWN_LIST=["markdown", "mkd", "md"]
MARKDOWN_EXTENSION="md"

def slugify(title):
  return title.lower().replace(" ", "-")

def new_slug_and_path_from_title(title, ext, append=0):
  slugified = slugify(title)
  slug = slugified if not append else "%s-%s" % (slugified, append)
  file_name = "%s.%s" % ( slug, ext )
  path = os.path.join(POST_DIRECTORY, file_name)
  
  if os.path.exists(path):
    return new_slug_and_path_from_title(title, ext, append + 1)

  return (slug, path) 

def find_files(target_directory, filter_func=None):
  ret = []
  for root, dirs, files in os.walk(target_directory):
    ret += filter(filter_func,files)
  return ret

@task
def new(markup="md",**kwargs):
  """Handles creation of a new post."""
  
  env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))
  if markup in MARKUP_MARKDOWN_LIST:
    template = env.get_template("post-markdown.j2")
    extension = MARKDOWN_EXTENSION
  else:
    sys.stderr.write("Unable to find template for markup type: '%s'\n" % (markup))
    sys.exit(1)
    
  try:
    if not os.path.exists(POST_DIRECTORY):
      os.makedirs(POST_DIRECTORY)
  except OSError as exc:
    sys.stderr.write("Unable to write directory '%s', error: '%s'\n" % (POST_DIRECTORY, str(exc)))
    sys.exit(2)

  tdict = dict()
  title=kwargs.get("title", "My Post")
  (slug, path) = new_slug_and_path_from_title(title, extension)
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
