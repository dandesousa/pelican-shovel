#!/usr/bin/env python

from common import *

POST_DIRECTORY=os.path.join(CONTENT_DIRECTORY, "posts")
TODAYS_POST_DIRECTORY=os.path.join(POST_DIRECTORY, NOW.strftime("%Y/%m"))

def create(**kwargs):
    """Creates a brand new pelican post under content/posts.

    arguments
        --title: The title of the post and value used for slugifying the post
        --tags: Tags to add to the post when created (ex. --tags programming,tech)
        --category: Category or categories to use for the post (ex. --category Programming)
        --markup: The markup language to use (default: markdown)
    """
    markup = kwargs.get("markup", DEFAULT_MARKUP)
    file_information = get_file_render_information("post", markup)
    create_new_pelican_file(file_information, TODAYS_POST_DIRECTORY, kwargs)


def list(pattern):
    """Searches for and lists posts under content/posts.

    arguments
        <pattern>: The pattern to use when searching for posts, this is a case insensitive regular expression
        --edit: If assert, will also open your git editor with the posts found

    """
    list_pelican_files(POST_DIRECTORY, search=pattern)


def edit(pattern, **kwargs):
    """Works like list but opens the post in your git editor.

    This is a shortcut method for editing a post.

    arguments:
        <pattern>: required pattern to use when searching for posts to edit
    """
    list_pelican_files(POST_DIRECTORY, edit=True, search=pattern)
