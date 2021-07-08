#!/bin/python
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class PluginManagerUi(Gtk.ApplicationWindow):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Orca Plugin Manager")
        self.app = app
        self.connect("destroy", self._onCancelButtonClicked)
        self.connect('key-press-event', self._onKeyPressWindow)

        self.set_default_size(650, 650)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        # pluginInfo (object) = 0
        # name (str) = 1
        # active (bool) = 2
        # buildIn (bool) = 3
        # dataDir (str) = 4
        # moduleDir (str) = 5
        # dependencies (object) = 6
        # moduleName (str) = 7
        # description (str) = 8
        # authors (object) = 9
        # website (str) = 10
        # copyright (str) = 11
        # version (str) = 12
        # helpUri (str) = 13
        # iconName (str) = 14
        self.listStore = Gtk.ListStore(object,str, bool, bool, str, str,object,str,str,object,str,str,str,str,str)

        self.treeView = Gtk.TreeView(model=self.listStore)
        self.treeView.connect("row-activated", self._rowActivated)
        self.treeView.connect('key-press-event', self._onKeyPressTreeView)

        self.rendererText = Gtk.CellRendererText()
        self.columnText = Gtk.TreeViewColumn("Name", self.rendererText, text=1)
        self.treeView.append_column(self.columnText)

        self.rendererToggle = Gtk.CellRendererToggle()
        self.rendererToggle.connect("toggled", self._onCellToggled)

        self.columnToggle = Gtk.TreeViewColumn("Active", self.rendererToggle, active=2)
        self.treeView.append_column(self.columnToggle)


        self.buttomBox = Gtk.Box(spacing=6)
        self.mainVBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.mainVBox.pack_start(self.treeView, True, True, 0)
        self.mainVBox.pack_start(self.buttomBox, False, True, 0)

        self.add(self.mainVBox)
        self.oKButton = Gtk.Button.new_with_mnemonic("_Details")
        self.oKButton.connect("clicked", self._onDetailsButtonClicked)
        self.buttomBox.pack_start(self.oKButton, True, True, 0)
        
        self.oKButton = Gtk.Button.new_with_mnemonic("_OK")
        self.oKButton.connect("clicked", self._onOkButtonClicked)
        self.buttomBox.pack_start(self.oKButton, True, True, 0)

        self.applyButton = Gtk.Button.new_with_mnemonic("_Apply")
        self.applyButton.connect("clicked", self._onApplyButtonClicked)
        self.buttomBox.pack_start(self.applyButton, True, True, 0)

        self.applyButton = Gtk.Button.new_with_mnemonic("_Install")
        self.applyButton.connect("clicked", self._onInstallButtonClicked)
        self.buttomBox.pack_start(self.applyButton, True, True, 0)
        
        self.applyButton = Gtk.Button.new_with_mnemonic("_Uninstall")
        self.applyButton.connect("clicked", self._onUninstallButtonClicked)
        self.buttomBox.pack_start(self.applyButton, True, True, 0)
        
        self.cancelButton = Gtk.Button.new_with_mnemonic("_Cancel")
        self.cancelButton.connect("clicked", self._onCancelButtonClicked)
        self.buttomBox.pack_start(self.cancelButton, True, True, 0)

    def closeWindow(self):
        Gtk.main_quit()
    def uninstallPlugin(self):
        selection = self.treeView.get_selection()
        model, list_iter = selection.get_selected()
        try:
            if model.get_value(list_iter,0):
                pluginInfo = model.get_value(list_iter,0)
                pluginName = self.app.getPluginSystemManager().getPluginName(pluginInfo)
                dialog = Gtk.MessageDialog(None,
                        Gtk.DialogFlags.MODAL,
                        type=Gtk.MessageType.INFO,
                        buttons=Gtk.ButtonsType.YES_NO)

                dialog.set_markup("<b>%s</b>" % 'Remove Plugin {}?'.format(pluginName))
                dialog.format_secondary_markup('Do you really want to remove Plugin {}?'.format(pluginName))
                response = dialog.run()
                if response == Gtk.ResponseType.YES:
                    dialog.destroy()
                else:
                    dialog.destroy()
                    return
                self.app.getPluginSystemManager().uninstallPlugin(model.get_value(list_iter,0))
                self.refreshPluginList()
        except:
            pass
        
    def installPlugin(self):
        ok, filePath = self.chooseFile()
        if not ok:
            return
        self.app.getPluginSystemManager().installPlugin(filePath)
        self.refreshPluginList()
        
    def _onKeyPressWindow(self, _, event):
        _, key_val = event.get_keyval()
        if key_val == Gdk.KEY_Escape:
            self.closeWindow()
    def _onKeyPressTreeView(self, _, event):
        _, key_val = event.get_keyval()
        if key_val == Gdk.KEY_Return:
            self.applySettings()
            self.closeWindow()
        if key_val == Gdk.KEY_Escape:
            self.closeWindow()
        # CTRL + Q
        #modifiers = event.get_state()
        #if modifiers == Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK:
        #    if key_val == Gdk.KEY_q:
        #        self._on_scan()
    def applySettings(self):
        for row in self.listStore:
            pluginInfo = row[0]
            isActive = row[2]
            self.app.getPluginSystemManager().setPluginActive(pluginInfo, isActive)
        self.app.getPluginSystemManager().syncAllPluginsActive()
        self.refreshPluginList()

    def _rowActivated(self, tree_view, path, column):
        print('rowActivated')
    def showDetails(self):
        selection = self.treeView.get_selection()
        model, list_iter = selection.get_selected()
        try:
            if model.get_value(list_iter,0):
                name = model.get_value(list_iter,1)
                description = model.get_value(list_iter,8)
                authors = model.get_value(list_iter,9)
                website =model.get_value(list_iter,10)
                copyright = model.get_value(list_iter,11)
                license = '' #model.get_value(list_iter,0)
                version = model.get_value(list_iter,12)
                dialog = Gtk.AboutDialog(self)
                dialog.set_authors(authors)
                dialog.set_website(website)
                dialog.set_copyright(copyright)
                dialog.set_license(license)
                dialog.set_version(version)
                dialog.set_program_name(name)
                dialog.set_comments(description)
                dialog.run()
                dialog.destroy()
        except:
            pass

    def _onDetailsButtonClicked(self, widget):
        self.showDetails()

    def _onOkButtonClicked(self, widget):
        self.applySettings()
        self.closeWindow()
    def _onApplyButtonClicked(self, widget):
        self.applySettings()
    def _onInstallButtonClicked(self, widget):
        self.installPlugin()
    def _onUninstallButtonClicked(self, widget):
        self.uninstallPlugin()
    def _onCancelButtonClicked(self, widget):
        self.closeWindow()
    def refreshPluginList(self):
        self.clearPluginList()
        pluginList = self.app.getPluginSystemManager().plugins
        for pluginInfo in pluginList:
            self.addPlugin(pluginInfo)
    def clearPluginList(self):
        self.listStore.clear()

    def addPlugin(self, pluginInfo):
        ignoredPlugins = self.app.getPluginSystemManager().getIgnoredPlugins()
        moduleDir = self.app.getPluginSystemManager().getPluginModuleDir(pluginInfo)
        if moduleDir in ignoredPlugins:
            return

        hidden = self.app.getPluginSystemManager().isPluginHidden(pluginInfo)
        if hidden:
            return

        moduleName = self.app.getPluginSystemManager().getPluginModuleName(pluginInfo)
        name = self.app.getPluginSystemManager().getPluginName(pluginInfo)
        version = self.app.getPluginSystemManager().getPluginVersion(pluginInfo)
        website = self.app.getPluginSystemManager().getPluginWebsite(pluginInfo)
        authors = self.app.getPluginSystemManager().getPluginAuthors(pluginInfo)
        buildIn = self.app.getPluginSystemManager().isPluginBuildIn(pluginInfo)
        description = self.app.getPluginSystemManager().getPluginDescription(pluginInfo)
        iconName = self.app.getPluginSystemManager().getPluginIconName(pluginInfo)
        copyright = self.app.getPluginSystemManager().getPluginCopyright(pluginInfo)
        dependencies = self.app.getPluginSystemManager().getPluginDependencies(pluginInfo)

        #settings = self.app.getPluginSystemManager().getPluginSettings(pluginInfo)
        #hasDependencies = self.app.getPluginSystemManager().hasPluginDependency(pluginInfo)
        loaded = self.app.getPluginSystemManager().isPluginLoaded(pluginInfo)
        available = self.app.getPluginSystemManager().isPluginAvailable(pluginInfo)
        active = self.app.getPluginSystemManager().isPluginActive(pluginInfo)

        #externalData = self.app.getPluginSystemManager().getPluginExternalData(pluginInfo)
        helpUri = self.app.getPluginSystemManager().getPlugingetHelpUri(pluginInfo)
        dataDir = self.app.getPluginSystemManager().getPluginDataDir(pluginInfo)
        
        # pluginInfo (object) = 0
        # name (str) = 1
        # active (bool) = 2
        # buildIn (bool) = 3
        # dataDir (str) = 4
        # moduleDir (str) = 5
        # dependencies (object) = 6
        # moduleName (str) = 7
        # description (str) = 8
        # authors (object) = 9
        # website (str) = 10
        # copyright (str) = 11
        # version (str) = 12
        # helpUri (str) = 13
        # iconName (str) = 14
        self.listStore.append([pluginInfo, name, active, buildIn, dataDir, moduleDir, dependencies, moduleName, description, authors, website, copyright, version, helpUri, iconName])
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
    def _onCellToggled(self, widget, path):

        self.listStore[path][2] = not self.listStore[path][2]
    def present(self):
        orca_state = self.app.getDynamicApiManager().getAPI('OrcaState')
        ts = 0
        try:
            ts = orca_state.lastInputEvent.timestamp
        except:
            pass
        if ts == 0:
            ts = Gtk.get_current_event_time()
        self.present_with_time(ts)
    def run(self):
        self.refreshPluginList()
        self.present()
        self.show_all()
        Gtk.main()
        self.destroy()
