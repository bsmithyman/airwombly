import os
from flask import Flask

# Pull Git repository configuration from environment
gitkeys = ['LOCALREPO', 'REMOTEREPO']
gitconfig = {key: os.getenv(key) for key in gitkeys}
subdir = lambda x: '{0}/{1}'.format(gitconfig['LOCALREPO'], x)


# Check to see if static or template directories exist in the Git repo.
# If so, substitute those for the ones hard coded into the app.
kwargs = {}
if os.path.isdir(subdir('static')):
    kwargs['static_folder'] = subdir('static')
if os.path.isdir(subdir('templates')):
    kwargs['template_folder'] = subdir('templates')

app = Flask(__name__, **kwargs)

from airwombly import views
