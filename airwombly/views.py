from flask import render_template, redirect, session, url_for, request, g, abort
from airwombly import app, backend, gitconfig
import json

def getBR ():
    return backend.BlogRepo(gitconfig['LOCALREPO'], gitconfig['REMOTEREPO'])

@app.route('/', methods = ['GET'])
def root ():
    br = getBR()
    posts = br.getPosts().keys()

    return render_template('index.html', posts = posts, br = br)

@app.route('/', methods = ['POST'])
def webhook ():
    try:
        data = json.loads(request.data)
    except:
        pass

    br = getBR()
    br.origin.pull()
    return str(br.repo.head.commit.hexsha)

@app.route('/<tag>')
def page (tag):
    br = getBR()
    p = backend.Parser()
    pages = br.getPages()

    if tag in pages:
        try:
            metadata, content = p.parsefile(pages[tag])
        except:
            abort(404)

        return render_template('page.html', metadata = metadata, content = content, br = br)

    else:
        abort(404)

@app.route('/posts/<tag>')
def post (tag):
    br = getBR()
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
