airwombly
=========

The airwombly project is a minimalist blogging engine written in Python. Its design is based around three main concepts:

1. airwombly is PaaS-deployable with minimal configuration on the server side.
2. the authoritative copy of the site data is kept in a git repository and automatically sync'd to the frontend server through the use of commit hooks.
3. the content of the site is written in markdown and YAML, stored in a git repository and can therefore be ported easily.
