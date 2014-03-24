import os
import git
import yaml
from misaka import Markdown, HtmlRenderer

class CatastrophicGitlessness (Exception):
    pass

class BlogRepo:
    '''
    Automatically caches remote Git repository locally. Handles blog/page
    access from the repository.
    '''

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

    def _getTree (self, treename):
        '''
        List files in named directory.
        '''

        if not hasattr(self, treename):
            for tree in self.repo.head.commit.tree.trees:
                if tree.path == treename:
                    setattr(self, treename, tree)
                    break

        retval = {os.path.splitext(p.name)[0]: p.abspath for p in getattr(self, treename).blobs}
        return retval

    def getPosts (self):
        return self._getTree('posts')

    def getPages (self):
        return self._getTree('pages')

    def getTrees (self):
        return {tree.path: tree.abspath for tree in self.repo.head.commit.tree.trees}

class Parser:

    maxlen = 1024**2 # 1 MB
    yaml_delimiter = '---\n'
    mdtypes = ['.md', '.txt']

    def __init__ (self):
    
        rndr = HtmlRenderer()
        self.md = Markdown(rndr)

    def parsefile (self, filename):
        '''
        Return contents of file 'filename'. If the file extension identifies
        it as a Markdown document, pass through the Markdown parser.
        '''

        if os.path.isfile(filename):
            with open(filename, 'r') as fp:
                lines = fp.readlines(self.maxlen)

        else:
            raise IOError('No such file or directory: \'{}\''.format(filename))

        if os.path.splitext(filename)[1] in self.mdtypes:
            return self.parse(lines)
        else:
            return {}, ''.join(lines)

    def parse (self, lines):
        '''
        Parse Markdown and YAML header.
        '''
    
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
        
