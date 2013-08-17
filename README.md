pelican-shovel
==============

pelican-shovel (PS) helps you organize your pelican site, by creating posts and pages and allowing them to be easily found and managed.

This project is in the initial stage and under development.

Requirements
-------------

pelican-shovel requires [shovel](https://github.com/seomoz/shovel), a rake-like tool for python.

```
pip install shovel
```

It works best if you install the latest from source, though. Clone it and run `setup.py install`.

you should also install jinja2 templates, which is also required for page / post generation.

```
pip install jinja2
```

## Usage


PS makes it easy to create new posts and pages. You can get started by adding it as a submodule or copying to your pelican site:

```
git submodule add git@github.com:dandesousa/pelican-shovel.git shovel
```

You then have access to all the PS tasks:

### Help

Following the shovel syntax you can get help information by typing:

```
# Prints short description of each command in PS
shovel help
```

Get detailed information about a command by drilling in:

```
# Prints the help docs for the command
shovel help post.new
```

### Creation

```
shovel post.new --title "It's a wonderful day in the neighborhood!" 
# page created, editor opens
```

New posts are written and we even have an option to open your editor (we use your git editor) as you create pages. If you don't want your editor to open by default:

```
shovel post.new --title "My Post" --quiet
```

You can do the same for pages:

```
shovel page.new --title "My Page" --quiet
```

### Listing

You can also see posts you already created:

```
# lists all the posts you made -- maybe not so useful
shovel post.list 
```

You can filter them with the search parameter

```
# case insensitive regex search
shovel post.list 2013

# equivalent search syntax
shovel post.list --search 2013
```

searches for all posts with 2013 in the file path.

### Edits

Edits work much like lists.

```
# edits all posts with 'programming' in the path, opens them in your editor
shovel post.edit programming
```

As a bonus you can also edit posts this way:

```
# finds all posts with "programming" in the path, opens them in your editor
shovel post.list --search programming --edit
```

## Future 

More tasks will be coming in the future:
  * Querying metadata for your posts
  * Support for other markups besides markdown
  * Removing posts, moving posts
  * Changing metadata
  * Better Docs

## Contributing

Feel free to fork and contribute if you like the project. Suggestions are always appreciated.
