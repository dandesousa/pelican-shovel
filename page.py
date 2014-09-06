#!/usr/bin/env python

import os
from common import *

PAGE_DIRECTORY=os.path.join(CONTENT_DIRECTORY, "pages")


def create(**kwargs):
    """Creates a brand new pelican page under content/pages.

    arguments
        --title: The title of the page and value used for slugifying the page
        --markup: The markup language to use (default: markdown)
    """
    markup = kwargs.get("markup", DEFAULT_MARKUP)
    file_information = get_file_render_information("page", markup)
    create_new_pelican_file(file_information, PAGE_DIRECTORY, kwargs)


def list(pattern):
    """Searches for and lists pages under content/pages.

    arguments
        <pattern>: The pattern to use when searching for pages, this is a case insensitive regular expression
    """
    list_pelican_files(PAGE_DIRECTORY, search=pattern)


def edit(pattern):
    """Works like list but opens the page in your git editor.

    This is a shortcut method for editing a page.

    arguments:
        <pattern>: required pattern to use when searching for pages to edit
    """
    list_pelican_files(PAGE_DIRECTORY, edit=True, search=pattern)
