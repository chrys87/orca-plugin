import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class HelloWorld(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'helloworld'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        pass
    def do_activate(self):
        API = self.object
        API.app.connect("start-orca", self.process)
        print('activate')
    def do_deactivate(self):
        API = self.object
        API.app.disconnect_by_func(self.process)
        print('deactivate')
    def do_update_state(self):
        API = self.object
        print('update')
    def process(self, app):
        print('process')
        app.getAPI('Speech').speak('hello world')
