from flask import render_template, redirect, session, url_for, request, g, abort
from airwombly import app, backend, gitconfig, cache
import json

def getBR ():
    '''
    Short function to get access to the repo.
    '''

    return backend.BlogRepo(gitconfig['LOCALREPO'], gitconfig['REMOTEREPO'])

@app.route('/', methods = ['GET'])
@cache.cached(300)
def root ():
    '''
    Handle the site index. Preload post listing for convenience.
    '''

    br = getBR()
    posts = br.getPosts().keys()

    return render_template('index.html', posts = posts, br = br)

@app.route('/', methods = ['POST'])
def webhook ():
    '''
    Handle POST requests to the site index. This acts as the target for the
    webhook on a Git repository (could be GitHub, another Git server, or even
    a server-side hook on a bare repo.
    '''

    try:
        # We don't really do anything with this data for now
        data = json.loads(request.data)
    except:
        pass

    br = getBR()
    br.origin.pull()
    cache.clear()
    return str(br.repo.head.commit.hexsha)

@app.route('/<tag>')
@cache.cached(3600)
def page (tag):
    '''
    Handles rendering of pages in the site root; pulls from Git backing.
    Converts from Markdown if appropriate.
    '''

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
@cache.cached(3600)
def post (tag):
    '''
    Handles rendering of posts in the site root; pulls from Git backing.
    Converts from Markdown if appropriate.
    '''

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
