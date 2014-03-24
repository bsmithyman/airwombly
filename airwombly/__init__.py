import os
from flask import Flask
from airwombly.backend import BlogRepo

# Pull Git repository configuration from environment
gitkeys = ['LOCALREPO', 'REMOTEREPO']
gitconfig = {key: os.getenv(key) for key in gitkeys}
if not gitconfig[gitkeys[0]]:
    gitconfig[gitkeys[0]] = 'repo.git'

subdirs = {}
if os.path.isdir(gitconfig[gitkeys[0]]):
    br = BlogRepo(gitconfig[gitkeys[0]], gitconfig[gitkeys[1]])
    subdirs.update(br.getTrees())

# Check to see if static or template directories exist in the Git repo.
# If so, substitute those for the ones hard coded into the app.
kwargs = {}
if 'static' in subdirs:
    kwargs['static_folder'] = subdirs['static']
if 'templates' in subdirs:
    kwargs['template_folder'] = subdirs['templates']

app = Flask(__name__, **kwargs)

from airwombly import views
