import os
import git
import yaml
from misaka import Markdown, HtmlRenderer

class CatastrophicGitlessness (Exception):
    pass

class BlogRepo:

    def __init__ (self, local, remote):
        try:
            repo = git.Repo(local)
        except git.NoSuchPathError:
            try:
                repo = git.Repo.clone_from(remote, local)
            except:
                repo = None

        if repo is None:
            raise CatastrophicGitlessness('Unable to initialize the Git repository!')

        self.repo = repo
        self.origin = repo.remotes.origin

    def getPosts (self):

        if not hasattr(self, 'posts'):
            for tree in self.repo.head.commit.tree.trees:
                if tree.path == 'posts':
                    self.posts = tree
                break

        posts = {os.path.splitext(p.name)[0]: p.abspath for p in self.posts.blobs}
        return posts

class Parser:

    maxlen = 1024**2 # 1 MB
    yaml_delimiter = '---\n'

    def __init__ (self):
    
        rndr = HtmlRenderer()
        self.md = Markdown(rndr)

    def parsefile (self, filename):

        if os.path.isfile(filename):
            with open(filename, 'r') as fp:
                lines = fp.readlines(self.maxlen)

        else:
            raise IOError('No such file or directory: \'{}\''.format(filename))

        return self.parse(lines)

    def parse (self, lines):
    
        if lines[0] == self.yaml_delimiter:
            for i, txt in enumerate(lines[1:]):
                if txt == self.yaml_delimiter:
                    txtyaml = ''.join(lines[1:i+1])
                    txtmd = ''.join(lines[i+3])
                    break
        else:
            txtyaml = ''
            txtmd = ''.join(lines)
   
        metadata = yaml.load(txtyaml)
        html = self.md.render(txtmd)

        return [metadata, html]
        
