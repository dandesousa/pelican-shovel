#!/usr/bin/env python
# encoding: utf-8

import sys
from shovel import task

VALID_POST_NAMES = ("post", "posts", "POSTS", "POST")
VALID_PAGE_NAMES = ("page", "pages", "PAGES", "PAGE")
VALID_NAMES = VALID_POST_NAMES + VALID_PAGE_NAMES


@task
def create(name, **kwargs):
    """Creates a new post or page.

    Positional Arguments:
        :param name: the type of entry you'd like to create {'post', 'page'}

    Keyworded Arguments (not supported for all names):
        :param markup: The markup language to use (default: markdown)
        :param title: the title of the post or page
        :param tags: tags to add to the post when created
        :param category: The category or categories to use for the post
    """
    if name in VALID_POST_NAMES:
        from post import create as create_post
        create_post(**kwargs)
    elif name in VALID_PAGE_NAMES:
        from page import create as create_page
        create_page(**kwargs)
    else:
        sys.stderr.write("Expected argument 1 to be one of ({}), but got: '{}' instead.\n".format(', '.join(VALID_NAMES), name))


@task
def list(name, pattern=""):
    """lists an existing post or page,

    Positional Arguments:
        :param name: the type of entry you'd like to list {'post', 'page'}
        :param pattern: the pattern as a regular expression to search for in the file path.
    """
    if name in VALID_POST_NAMES:
        from post import list as list_post
        list_post(pattern)
    elif name in VALID_PAGE_NAMES:
        from page import list as list_page
        list_page(pattern)
    else:
        sys.stderr.write("Expected argument 1 to be one of ({}), but got: '{}' instead.\n".format(', '.join(VALID_NAMES), name))


@task
def edit(name, pattern=""):
    """Edits an existing post or page,

    Positional Arguments:
        :param name: the type of entry you'd like to edit {'post', 'page'}
        :param pattern: the pattern as a regular expression to search for in the file path.
    """
    if name in VALID_POST_NAMES:
        from post import edit as edit_post
        edit_post(pattern)
    elif name in VALID_PAGE_NAMES:
        from page import edit as edit_page
        edit_page(pattern)
    else:
        sys.stderr.write("Expected argument 1 to be one of ({}), but got: '{}' instead.\n".format(', '.join(VALID_NAMES), name))


@task
def remove(name, pattern="", force=False):
    """Permanently deletes the post / page you specified.

    Positional Arguments:
        :param name: the type of entry you'd like to edit {'post', 'page'}
        :param pattern: the pattern as a regular expression to search for in the file path.

    Keyworded Arguments:
        :param force: forces deletion of the file without prompting the user (use with caution).
    """
    if name in VALID_POST_NAMES:
        from post import remove as remove_post
        remove_post(pattern, force=force)
    elif name in VALID_PAGE_NAMES:
        from page import remove as remove_page
        remove_page(pattern, force=force)
    else:
        sys.stderr.write("Expected argument 1 to be one of ({}), but got: '{}' instead.\n".format(', '.join(VALID_NAMES), name))
