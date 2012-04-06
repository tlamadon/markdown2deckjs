import markdown
from markdown import etree_loader
import sys
from elementtree.ElementTree import Element, SubElement, dump
import re

class SlideProcessor(markdown.treeprocessors.Treeprocessor):

    # method that creates the slide node
    # from the html node
    def create_slide(self, buf, i,name=''):
        # creating the name of the slide
        # by parsing the title and removing any odd character
        slidename = re.sub('[^a-zA-Z0-9\\s]','',name)
        slidename = re.sub('\\s','_',slidename)      

        # we create a new div that will contain the slide
        cont = Element("div") #etree_loader.importETree().Element('div')
        cont.set('class', 'slide')
        cont.set('id', slidename)

        return cont

    def create_source(self, root):
        if root.tag == 'img' and str(root.get('src'))[:4] == 'http':
            src = etree_loader.importETree().Element('cite')
            src.text = 'Quelle: ' + str(root.get('src'))
            src.set('class', 'source')
            root.append(src)
        for c in root:
            c = self.create_source(c)
        return root

    def parseClass(self,content):
      r = re.search('^\\s*~([\\w\\.]*)',content)
      if (r!=None):
        content = re.sub('^\\s*~([\\w\\.]*)','',content)
        eclass = r.group(1)
        if len(eclass)==0:
          eclass = 'slide'
      else:
        eclass = None


      return content,eclass


    # method that create wihtin slide effects
    # or nested effects
    # it looks for the '~' character
    def create_effects(self, root):
        if root.text:
          content,eclass = self.parseClass(root.text[:])
          if (eclass!=None):
            root.text = content
            root.set('class',eclass)
        elif root.tail:
          content,eclass = self.parseClass(root.tail[:])
          if (eclass!=None):
            root.tail = content
            root.set('class',eclass)

        for c in root:
            c = self.create_effects(c)
        return root

    # parsing the tree from the root
    # of the html document
    def run(self, root):
        root = self.create_source(root)
        root = self.create_effects(root)
        i = 1
        nodes = []
        buf = []
        slide      = Element('div')
        slide_node = Element('div')


        # finding and creating slides from H1 and H2
        for c in root:
          if c.tag in ('h1','h2'):
            # append previous slide_node
            if (slide_node!=None):
              slide.append(slide_node)
            # create a new one for this title
            slide_node = self.create_slide(buf,i,c.text)
            slide_node.append(c)
          else:
            # append this to the slide div
            slide_node.append(c)            
        
        return slide

class slider(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('slideprocessor', SlideProcessor(), '>prettify')
        md.registerExtension(self)

    def reset(self):
        pass


def makeExtension(configs=None) :
    return slider()
