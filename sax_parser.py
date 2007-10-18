import xml.sax.handler
import xml.sax
import pprint
import time
import trie
from xml.sax.saxutils import escape
 
class DictionaryHandler(xml.sax.handler.ContentHandler):
  def __init__(self):
    self.buffer = ''
    self.processing = 0
    self.mapping = {}
    self.inkeyword = 0
    self.keyword = ''
 
  def startElement(self, name, attributes):
    if name == "ar":
      self.processing = 1
    elif name == "k":
      self.inkeyword = 1
    else:
      self.buffer += '<%s>' %name

  def characters(self, data):
    if self.inkeyword:
      self.keyword += data
    elif self.processing:
      self.buffer += escape(data)
 
  def endElement(self, name):
    if name == "ar":
      self.processing = 0
      self.mapping[self.keyword] = self.buffer
      self.keyword = ''
      self.buffer = ''
    elif name == 'k':
      self.inkeyword = 0
    else:
      self.buffer += '</%s>' %name


parser = xml.sax.make_parser(  )
handler = DictionaryHandler(  )
parser.setContentHandler(handler)
time1 = time.time()
parser.parse("mwc/dict.xdxf")
print "time to parse xdxf", time.time() - time1
dict_trie = trie.Trie()
map = handler.mapping
time2 = time.time()
for term in map:
    dict_trie.add_term(term, map[term])
print "time to build trie", time.time() - time2
time3 = time.time()
dict_trie.pickle_me('trie.data')    
print  "time to pickle", time.time() - time3



