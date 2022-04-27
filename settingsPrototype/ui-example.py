#!/bin/python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk 

userPluginFolder = '/.local/share/orca/plugins/'

class ListBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Orca Settings")
        self.set_border_width(10)
        self.connect("delete-event", Gtk.main_quit)

    def loadPluginInformation(self):
        pass
    def createUI(self):
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)
        holi = Gtk.Label(label="Choose your favourite language")
        box_outer.add(holi)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(label="Javascript", xalign=0)
        button = Gtk.LinkButton.new_with_label(uri="https://www.javascript.com/",label="Go to Javascript web")
        hbox.pack_start(label, True, True, 0)
        hbox.add(button)
        listbox.add(row)
       
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label(label="C", xalign=0)
        button = Gtk.LinkButton(uri="http://www.learn-c.org/",label="Go to C web")
        hbox.pack_start(label, True, True, 0)
        hbox.add(button)
        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        button = Gtk.LinkButton(uri="https://www.python.org/",label="Go to Python web")
        row.add(hbox)
        label = Gtk.Label(label="Python", xalign=0)
        hbox.pack_start(label, True, True, 0)
        hbox.add(button)
        listbox.add(row)
        
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        button = Gtk.LinkButton(uri="https://www.java.com/es/download/",label="Go to Java web")
        row.add(hbox)
        label = Gtk.Label(label="Java", xalign=0)
        hbox.pack_start(label, True, True, 0)
        hbox.add(button)
        listbox.add(row)

win = ListBoxWindow()
win.createUI()
win.show_all()
Gtk.main() 
