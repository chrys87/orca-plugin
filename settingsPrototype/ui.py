#!/bin/python
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk 
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

from orca.plugin_system_manager import PluginType
from orca.plugin_system_manager import PluginSystemManager

#userPluginFolder = expanduser('~/.local/share/orca/plugins/')

class ListBoxWindow(Gtk.Window):
    DEFAULT_LOADERS = ("python3", )

    def __init__(self):
        Gtk.Window.__init__(self, title="Orca Settings")
        self.set_border_width(10)
        self.connect("delete-event", Gtk.main_quit)
        self.pluginSystemManager = PluginSystemManager(None)
    def load(self):
        self.loadCoreInformation()
        self.loadPluginInformation()
    def loadCoreInformation(self):
        pass
    def loadPluginInformation(self):
        pass
    def createUI(self):
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)
        holi = Gtk.Label(label="Orca Settings")
        box_outer.add(holi)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)
        
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(label="Orca", xalign=0)
        button = Gtk.Button.new_with_label(label="Open")
        hbox.pack_start(label, True, True, 0)
        hbox.add(button)
        listbox.add(row)
        for plugin in self.pluginSystemManager.plugins:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            row.add(hbox)
            label = Gtk.Label(label=self.pluginSystemManager.getPluginModuleName(plugin), xalign=0)
            button = Gtk.Button.new_with_label(label="Open")
            hbox.pack_start(label, True, True, 0)
            hbox.add(button)
            listbox.add(row)

        for plugin in self.pluginSystemManager.plugins:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            row.add(hbox)
            label = Gtk.Label(label=self.pluginSystemManager.getPluginModuleName(plugin), xalign=0)
            button = Gtk.Button.new_with_label(label="Open")
            hbox.pack_start(label, True, True, 0)
            hbox.add(button)
            listbox.add(row)

win = ListBoxWindow()
win.createUI()
win.show_all()
Gtk.main() 
