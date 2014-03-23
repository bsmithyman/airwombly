from flask import render_template, redirect, session, url_for, request, g, abort
from airwombly import app, backend, gitconfig
import json

@app.route('/')
def root ():
    br = backend.BlogRepo(gitconfig['LOCALREPO'], gitconfig['REMOTEREPO'])
    posts = br.getPosts()

    resp = '''
    <html><head><title>Test</title></head>
    <body>
    {}
    </body>
    </html>'''.format(''.join(['<a href="/post/{0}">{0}</a><br />'.format(tag) for tag in posts.keys()]))
    return resp

@app.route('/webhook', methods = ['POST'])
def webhook ():
    try:
        data = json.loads(request.data)
    except:
        pass

    br = backend.BlogRepo(gitconfig['LOCALREPO'], gitconfig['REMOTEREPO'])
    br.origin.pull()
    return str(br.repo.head.commit.hexsha)

@app.route('/post/<tag>')
def post (tag):
    br = backend.BlogRepo(gitconfig['LOCALREPO'], gitconfig['REMOTEREPO'])
    p = backend.Parser()
    posts = br.getPosts()

    if tag in posts:
        try:
            metadata, html = p.parsefile(posts[tag])
        except:
            pass

        return html

    else:
        abort(404)
