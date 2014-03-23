from flask import render_template, redirect, session, url_for, request, g, abort
from airwombly import app, backend, gitconfig
import json

@app.route('/')
def root ():
    return redirect(url_for('index'))

@app.route('/index')
def index ():
    br = backend.BlogRepo(gitconfig['LOCALREPO'], gitconfig['REMOTEREPO'])
    posts = br.getPosts().keys()

    return render_template('index.html', posts = posts, br = br)

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
            metadata, content = p.parsefile(posts[tag])
        except:
            abort(404)

        return render_template('post.html', metadata = metadata, content = content, br = br)

    else:
        abort(404)
