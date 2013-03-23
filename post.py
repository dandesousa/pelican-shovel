#!/usr/bin/env python

from common import *

def slugify(title):
  slug_name = title.lower().replace(" ", "-")
  return slug_name

@task
def new(**kwargs):
  '''Handles creation of a new post.


'''
  try:
    os.makedirs(POST_DIRECTORY)
  except OSError as exc:
    pass # TODO: Handle specific error conditions

  POST_TEMPLATE='''
Title: %(title)s
Date: %(date)s
Tags: %(tags)s
Category: %(category)s
Slug: %(slug)s
Author: %(author)s
Summary: %(summary)s
'''

  title=kwargs.get("title", "My Post")
  tags=kwargs.get("tags","")
  category=kwargs.get("category","")
  author=pelicanconf.AUTHOR
  summary=""
  tmpl_dict = dict(title=title, 
                   date=NOW.strftime("%Y-%m-%d %M:%d"),
                   tags=tags, 
                   category=category, 
                   slug=slugify(title),
                   author=author,
                   summary=summary)

  print POST_TEMPLATE % tmpl_dict
