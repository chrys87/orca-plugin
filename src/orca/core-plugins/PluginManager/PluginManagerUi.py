import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class PluginManagerUi(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Orca Plugin Manager")
        self.connect("destroy", Gtk.main_quit)

        self.set_default_size(200, 200)

        self.listStore = Gtk.ListStore(str, bool, str)

        treeView = Gtk.TreeView(model=self.listStore)

        rendererText = Gtk.CellRendererText()
        columnText = Gtk.TreeViewColumn("Text", rendererText, text=0)
        treeView.append_column(columnText)

        rendererToggle = Gtk.CellRendererToggle()
        rendererToggle.connect("toggled", self.on_cell_toggled)

        columnToggle = Gtk.TreeViewColumn("Toggle", rendererToggle, active=1)
        treeView.append_column(columnToggle)

        self.add(treeView)
    def addPlugin(self, Name, Active, Description = ''):
        self.listStore.append([Name, Active, Description])

    def on_cell_toggled(self, widget, path):
        self.listStore[path][1] = not self.listStore[path][1]
    def run(self):
        self.show_all()
        Gtk.main()
