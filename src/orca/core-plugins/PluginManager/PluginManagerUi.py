#!/bin/python
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# PMS_installPlugin
import os, tarfile, shutil

class PluginManagerUi(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Orca Plugin Manager")
        self.connect("destroy", self.on_cancelButton_clicked)

        self.set_default_size(400, 600)

        self.listStore = Gtk.ListStore(str, bool, str)

        self.treeView = Gtk.TreeView(model=self.listStore)
        self.treeView.connect("row-activated", self.rowActivated)

        self.rendererText = Gtk.CellRendererText()
        self.columnText = Gtk.TreeViewColumn("Name", self.rendererText, text=0)
        self.treeView.append_column(self.columnText)

        self.rendererToggle = Gtk.CellRendererToggle()
        self.rendererToggle.connect("toggled", self.on_cell_toggled)

        self.columnToggle = Gtk.TreeViewColumn("Active", self.rendererToggle, active=1)
        self.treeView.append_column(self.columnToggle)


        self.buttomBox = Gtk.Box(spacing=6)
        self.mainVBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.mainVBox.pack_start(self.treeView, True, True, 0)
        self.mainVBox.pack_start(self.buttomBox, False, True, 0)

        self.add(self.mainVBox)

        self.oKButton = Gtk.Button(label="OK")
        self.oKButton.connect("clicked", self.on_oKButton_clicked)
        self.buttomBox.pack_start(self.oKButton, True, True, 0)

        self.applyButton = Gtk.Button(label="Apply")
        self.applyButton.connect("clicked", self.on_applyButton_clicked)
        self.buttomBox.pack_start(self.applyButton, True, True, 0)


        self.applyButton = Gtk.Button(label="Install")
        self.applyButton.connect("clicked", self.on_installButton_clicked)
        self.buttomBox.pack_start(self.applyButton, True, True, 0)
        
        self.applyButton = Gtk.Button(label="Uninstall")
        self.applyButton.connect("clicked", self.on_uninstallButton_clicked)
        self.buttomBox.pack_start(self.applyButton, True, True, 0)
        
        self.cancelButton = Gtk.Button(label="Cancel")
        self.cancelButton.connect("clicked", self.on_cancelButton_clicked)
        self.buttomBox.pack_start(self.cancelButton, True, True, 0)

    def closeWindow(self):
        Gtk.main_quit()
    def uninstallPlugin(self):
        print("Uninstall")
        selection = self.treeView.get_selection()
        model, list_iter = selection.get_selected()
        print(model)
        self.PMS_uninstallPlugin('InstallTest')

        if list_iter:
            self.listStore.remove(list_iter)
        
    def installPlugin(self):
        print("Install")
        ok, filePath = self.chooseFile()
        if not ok:
            return
        self.PMS_installPlugin(filePath)
    def applySettings(self):
        print("Apply")
        selection = self.treeView.get_selection()
        model, list_iter = selection.get_selected()
        print(model.get_value(list_iter,0))
    def rowActivated(self, tree_view, path, column):
        print('active')

    def PMS_installPlugin(self, pluginFilePath, pluginStore=''):
        if not self.PMS_isValidPluginFile(pluginFilePath):
            print('out')
            return False
        if pluginStore == '':
            pluginStore = os.path.expanduser('~') + '/.local/share/orca/plugins/'
        if not pluginStore.endswith('/'):
            pluginStore += '/'
        if not os.path.exists(pluginStore):
            os.mkdir(pluginStore)
        else:
            if not os.path.isdir(pluginStore):
                return False

        try:
            with tarfile.open(pluginFilePath) as tar:
                tar.extractall(path=pluginStore)
        except Exception as e:
            print(e)
        print('install', pluginFilePath)
        return True
    def PMS_isValidPluginFile(self, pluginFilePath):
        if not isinstance(pluginFilePath, str):
            return False
        if pluginFilePath == '':
            return False
        if not os.path.exists(pluginFilePath):
            print('notexist')
            return False
        pluginFolder = ''
        pluginFileExists = False
        try:
            with tarfile.open(pluginFilePath) as tar:
                tarMembers = tar.getmembers()
                for tarMember in tarMembers:
                    if tarMember.isdir():
                        if pluginFolder == '':
                            pluginFolder = tarMember.name
                    if tarMember.isfile():
                        if tarMember.name.endswith('.plugin'):
                            pluginFileExists = True
                    if not tarMember.name.startswith(pluginFolder):
                        print(pluginFolder, tarMember.name)
                        return False
        except Exception as e:
            print(e)
            return False
        return pluginFileExists
    def PMS_uninstallPlugin(self, pluginName, pluginStore=''):
        if pluginStore == '':
            pluginStore = os.path.expanduser('~') + '/.local/share/orca/plugins/'
        if not pluginStore.endswith('/'):
            pluginStore += '/'
        if not os.path.isdir(pluginStore):
            return False
        if not os.path.isdir(pluginStore + pluginName):
            return False
        try:
            shutil.rmtree(pluginStore + pluginName, ignore_errors=True)
        except Exception as e:
            print(e)
            return False
        return True

    def on_oKButton_clicked(self, widget):
        self.applySettings()
        self.closeWindow()
    def on_applyButton_clicked(self, widget):
        self.applySettings()
    def on_installButton_clicked(self, widget):
        self.installPlugin()
    def on_uninstallButton_clicked(self, widget):
        self.uninstallPlugin()
    def on_cancelButton_clicked(self, widget):
        self.closeWindow()

    def addPlugin(self, Name, Active, Description = ''):
        self.listStore.append([Name, Active, Description])
    def chooseFile(self):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        filter_plugin = Gtk.FileFilter()
        filter_plugin.set_name("Plugin Archive")
        filter_plugin.add_mime_type("application/gzip")
        dialog.add_filter(filter_plugin)
        
        response = dialog.run()
        filePath = ''
        ok = False
        
        if response == Gtk.ResponseType.OK:
            ok = True
            filePath = dialog.get_filename()

        dialog.destroy()
        return ok, filePath
    def on_cell_toggled(self, widget, path):
        self.listStore[path][1] = not self.listStore[path][1]
    def run(self):
        self.show_all()
        Gtk.main()


if __name__ == "__main__":
    ui = PluginManagerUi()
    ui.addPlugin('InstallTest', True, 'bla')
    ui.addPlugin('plugin2', True, 'bla')
    ui.addPlugin('plugin3', True, 'bla')
    ui.run()
