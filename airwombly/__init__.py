import os
from flask import Flask

app = Flask(__name__)

keys = ['LOCALREPO', 'REMOTEREPO']
gitconfig = {key: os.getenv(key) for key in keys}

from airwombly import views
