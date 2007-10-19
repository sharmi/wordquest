import trie
import time
import wx
import wx.lib.expando as expando
import xml.dom.minidom as dom
import sys
reload(sys)
sys.setdefaultencoding('utf8')


EVT_MENU = wx.EVT_MENU

def get_all_text_formatting(dom):
    nodes_list = [dom]
    results = []
    for node in nodes_list:
        node.parentslist = {}
        parent = node.parentNode
        if parent:
            node.parentslist[parent.nodeName] = 1
            node.parentslist.update(parent.parentslist)
        if node.nodeName == '#text':
            results.append((node.nodeValue, node.parentslist))
        index = nodes_list.index(node)
        index += 1
        for item in node.childNodes:
            nodes_list.insert(index, item)
            index += 1
        #nodes_list.extend(node.childNodes)

    return results
        
        
 


class DictFrame(wx.Frame):
    QUIT_ID = 100
    PASTE_ID = 201
    COPY_ID = 202
    FIND_ID = 203
    REMEMBER_HISTORY_ID = 301
    CLEAR_HISTORY_ID = 302
    ENCODING_ASCII_ID = 401
    ENCODING_LATIN_1_ID = 402
    ENCODING_UTF8_ID = 403
    TEXT_INPUT_ID = 1001
    SEARCH_BUTTON_ID = 1002
    RESULTS_BOX_ID = 1003
    def __init__(self, parent, id, title, dict_trie):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(450, 350))
        self.dict_trie = dict_trie
        self.CreateStatusBar()
        self.SetStatusText("Loading")
        #self.SetIcon(wx.Icon('resources/images/chippy.jpg', wx.BITMAP_TYPE_JPEG))
        self.SetIcon(wx.Icon('resources/images/dict.ico', wx.BITMAP_TYPE_ICO))
        self.getMenus()
        self.getLayouts()


    def getLayouts(self):
        searchpanel =  wx.Panel(self, -1, style=wx.RAISED_BORDER)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.searchtxt = wx.TextCtrl(searchpanel, DictFrame.TEXT_INPUT_ID, '', style=wx.TE_LEFT)
        hbox1.Add(self.searchtxt, 6, wx.TOP | wx.BOTTOM, 4)
        hbox1.Add(wx.Button(searchpanel, DictFrame.SEARCH_BUTTON_ID, "Search"), 1, wx.ALL, 3)
        searchpanel.SetSizer(hbox1)
        resultspanel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        #self.resulttxt = expando.ExpandoTextCtrl(resultspanel, DictFrame.RESULTS_BOX_ID, style=wx.TE_AUTO_SCROLL | wx.TE_MULTILINE| wx.TE_RICH2 | wx.TE_BESTWRAP) 
        self.resulttxt = wx.TextCtrl(resultspanel, DictFrame.RESULTS_BOX_ID, style=wx.TE_AUTO_SCROLL | wx.TE_MULTILINE| wx.TE_RICH2 | wx.TE_BESTWRAP | wx.TE_READONLY) 
        #self.resulttxt.SetEditable(False)
        #self.resulttxt.SetScrollbar(int orientation, int position, int thumbSize, int range)
        #self.resulttxt.SetScrollbar(0, 11, 15, 11)
        #wx.StaticText(resultspanel, DictFrame.RESULTS_BOX_ID, 'Results Pane')
        hbox2.Add(self.resulttxt, 1, wx.EXPAND | wx.ALL, 4)
        resultspanel.SetSizer(hbox2)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(searchpanel, 1, wx.ALL | wx.EXPAND, 4)
        vbox.Add(resultspanel, 5, wx.ALL | wx.EXPAND, 4)
        self.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.OnSearch, id=DictFrame.SEARCH_BUTTON_ID)
        self.searchtxt.Bind(wx.EVT_KEY_UP, self.OnSearch)
        self.searchtxt.SetFocus()


    def OnSearch(self, event):
        searchword = self.searchtxt.GetValue()
        self.resulttxt.Clear()
        meanings = self.dict_trie.get_item(searchword)
        string_index = 0
        for data in meanings:
            datadom = dom.parseString("<xml>" + data + "</xml>")
            results = get_all_text_formatting(datadom)
            results = [(x.strip(' '), y) for x,y in results if x.strip(' ')]
            strings = []
            for index, textinfo in enumerate(results):
                textstr, textattr = textinfo
                self.resulttxt.AppendText(textstr)
                text_font = wx.ROMAN
                text_slant = wx.NORMAL
                text_weight = wx.NORMAL
                text_size = 10
                if 'co' in textattr:
                    text_size = text_size - 2
                if 'i' in textattr:
                    text_slant = wx.ITALIC
                if 'b' in textattr:
                    text_weight = wx.BOLD
                font1 = wx.Font(text_size, text_font, text_slant, text_weight, False, u'Comic Sans MS')
                textattr1 = wx.TextAttr()
                textattr1.SetFont(font1)
                self.resulttxt.SetStyle(string_index, string_index + len(textstr) , textattr1)
                self.resulttxt.AppendText(' ')
                string_index += len(textstr) + 1
            self.delimiter = "\n\n\n\n\n"
            self.resulttxt.SetScrollbar(0,0,50,100)
            self.resulttxt.AppendText(self.delimiter)
            string_index += len(self.delimiter)
        
        

    def getMenus(self):
        file = wx.Menu()
        file.Append( DictFrame.QUIT_ID, "&Quit", "Quit Dictionary", wx.ITEM_NORMAL)
        edit = wx.Menu()
        edit.Append(DictFrame.COPY_ID, "&Copy\tCtrl+C", "Copy Selected Text")
        edit.Append(DictFrame.PASTE_ID, "&Paste\tCtrl+P", "Paste Clipboard Text")
        edit.AppendSeparator()
        edit.Append(DictFrame.FIND_ID, "&Find\tCtrl+F", "Find ...")
        options = wx.Menu()
        history = wx.MenuItem(options, DictFrame.REMEMBER_HISTORY_ID, "&Remember History", "Remembers Last 100 searches", wx.ITEM_CHECK)
        history.SetBitmap(wx.Image("resources/images/history.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap())
        options.AppendItem(history)
        options.Append(DictFrame.CLEAR_HISTORY_ID, "C&lear History")
        encoding_submenu = wx.Menu()
        encoding_submenu.Append(DictFrame.ENCODING_ASCII_ID, "Ascii", '', wx.ITEM_RADIO)
        encoding_submenu.Append(DictFrame.ENCODING_LATIN_1_ID, "Latin 1", '', wx.ITEM_RADIO)
        encoding_submenu.Append(DictFrame.ENCODING_UTF8_ID, "Utf8", '', wx.ITEM_RADIO)
        options.AppendMenu(400, "Encoding", encoding_submenu)
        menubar = wx.MenuBar()
        menubar.Append(file, "&File")
        menubar.Append(edit, "&Edit")
        menubar.Append(options, "&Options")
        self.SetMenuBar(menubar)
        self.Center()
        #EVT_MENU(self, ABOUT_ID, self.OnAbout)
        #EVT_MENU(self, PREV_ID, self.prev)


    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This sample program shows off\n"
                              "frames, menus, statusbars, and this\n"
                              "message dialog.",
                              "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def prev(self, event):
        self.Close(true)

        

class DictionaryApp(wx.App):
    def __init__(self, dict_trie=None, *pargs, **kwargs):
        self.dict_trie = dict_trie # store reference to args
        # call parent class initializer
        wx.App.__init__(self, *pargs, **kwargs)

    def OnInit(self):
        frame = DictFrame(None, -1, "Dictionary", self.dict_trie)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


if __name__ == "__main__":
    dict_trie = trie.Trie()
    time1 = time.time()
    #dict_trie.unpickle_me('pickled_data')
    dict_trie.unpickle_me('trie.data')
    dictionaryApp = DictionaryApp(redirect=0, dict_trie=dict_trie)
    dictionaryApp.MainLoop()
    """
    while 1:
        term = raw_input()
        if term == 'end': break
        st_time = time.time()
        result = me.get_item(term)
        print "time for retrieval", time.time() - st_time
        print result
    """
