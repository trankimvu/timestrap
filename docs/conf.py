from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify


# Add markdown parser
source_parsers = {
    '.md': CommonMarkParser,
}

# The suffix(es) of source filenames.
source_suffix = '.md'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Timestrap'
copyright = "2017, Timestrap's Contributors"
author = "Timestrap's Contributors"

# The short X.Y version.
version = '1.0'
# The full version, including alpha/beta/rc tags.
release = '1.0-alpha'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# The theme to use for HTML and HTML Help pages.
html_theme = 'default'

# Output file base name for HTML help builder.
htmlhelp_basename = 'Timestrapdoc'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Timestrap.tex', 'Timestrap Documentation',
     "Timestrap's Contributors", 'manual'),
]

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'timestrap', 'Timestrap Documentation',
     [author], 1)
]

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Timestrap', 'Timestrap Documentation',
     author, 'Timestrap', 'Time tracking and invoicing you can host anywhere. Full export support in multiple formats and easily extensible.',  # noqa: E501
     'Miscellaneous'),
]

# Setup AutoStructify to enable Auto Toc Tree
github_doc_root = 'https://github.com/overshard/timestrap/tree/master/docs/'


def setup(app):
    app.add_config_value('recommonmark_config', {
        'url_resolver': lambda url: github_doc_root + url,
        'auto_toc_tree_section': 'Contents',
    }, True)
    app.add_transform(AutoStructify)