#!/usr/bin/env python
"""
Hello World, but with more meat.
"""

import wx
from summarizer import generate_summary

class MainFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw)

        #set current frame size
        self.SetSize((750, 600))

        # create a panel in the frame
        panel = wx.Panel(self)

        # put some text with a larger bold font on it
        st = wx.StaticText(panel, label="Article Summarizer")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # create text input
        self.article_url = wx.TextCtrl(panel, style = wx.TE_MULTILINE)
        self.summarized_text = wx.TextCtrl(panel, style = wx.TE_MULTILINE)

        # create button
        process_button = wx.Button(panel, label='Proccess')
        process_button.Bind(wx.EVT_BUTTON, self.OnPressButton)

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 10))
        sizer.Add(self.article_url, 10, wx.ALL | wx.EXPAND, 5)
        sizer.Add(process_button, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 3))
        sizer.Add(self.summarized_text, 10, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Summarize article content")

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Ask and Exit items
        fileMenu = wx.Menu()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a Article summarizer application",
                      "About Article Summarizer",
                      wx.OK|wx.ICON_INFORMATION)

    def OnPressButton(self, event):
        """Summarize article from URL"""
        value = self.article_url.GetValue()
        result = results = ""
        if not value:
            result = "You didn't enter anything!"
        if 'http' in value[:5]:
            results = generate_summary('url', value, 2)
        if len(value.split(". ")) >= 3:
            results = generate_summary('text', value, 2)

        for r in results:
            result += "%s \n\n" % r

        self.summarized_text.SetValue('%s' % result)

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MainFrame(None, title='Article Summarizer')
    frm.Show()
    app.MainLoop()