#!venv/bin/python

settings = {
    'debug':    True,
    'host':     '127.0.0.1',
}

from airwombly import app
app.run(**settings)
