#!/bin/python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(label=data))

class PluginManagerUi(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.pluginList = []
        self.set_default_size(200, -1)
        self.connect("destroy", Gtk.main_quit)
        self.listBox = Gtk.ListBox()

        self.buttomBox = Gtk.Box(spacing=6)
        self.mainVBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.mainVBox.pack_start(self.listBox, True, True, 0)
        self.mainVBox.pack_start(self.buttomBox, True, True, 0)

        self.add(self.mainVBox)

        self.oKButton = Gtk.Button(label="OK")
        self.oKButton.connect("clicked", self.on_oKButton_clicked)
        self.buttomBox.pack_start(self.oKButton, True, True, 0)

        self.applyButton = Gtk.Button(label="Apply")
        self.applyButton.connect("clicked", self.on_applyButton_clicked)
        self.buttomBox.pack_start(self.applyButton, True, True, 0)

        self.cancelButton = Gtk.Button(label="Cancel")
        self.cancelButton.connect("clicked", self.on_cancelButton_clicked)
        self.buttomBox.pack_start(self.cancelButton, True, True, 0)

        self.listBox.connect("row-activated", self.on_row_activated)

    def on_row_activated(self, listBox, listboxrow):
        print("Row %i activated" % (listboxrow.get_index()))

    def on_oKButton_clicked(self, widget):
        print("OK")

    def on_applyButton_clicked(self, widget):
        print("Apply")

    def on_cancelButton_clicked(self, widget):
        print("Cancel")


    def addPlugin(self, Name, Active, Description = ''):
        self.pluginList.append([Name, Active, Description])

    def run(self):
        for plugin in self.pluginList:
            print(plugin)
            box = Gtk.Box(spacing=10)
            pluginNameLabel = Gtk.Label(plugin[0])
            #pluginActiveCheckButton = Gtk.CheckButton(label="_Active", use_underline=True)
            #pluginActiveCheckButton.set_active(plugin[1])
            pluginActiveSwitch = Gtk.Switch()
            pluginActiveSwitch.set_active(plugin[1])


            pluginDescriptionLabel = Gtk.Label(plugin[2])

            box.pack_start(pluginNameLabel, True, True, 0)
            box.pack_start(pluginActiveSwitch, True, True, 0)
            box.pack_start(pluginDescriptionLabel, True, True, 0)

            self.listBox.add(box)
        self.show_all()
        Gtk.main()

if __name__ == "__main__":
    ui = PluginManagerUi()
    ui.addPlugin('plugin1', True, 'bla')
    ui.addPlugin('plugin2', True, 'bla')
    ui.addPlugin('plugin3', True, 'bla')
    ui.run()
