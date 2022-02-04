from orca import plugin

import gettext
import inspect, os

import gi, time
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas

class HelloWorld(GObject.Object, Peas.Activatable, plugin.Plugin):
    __gtype_name__ = 'helloworld'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
    def do_activate(self):
        API = self.object
        self.registerGestureByString(self.speakTest, _('hello world'), 'kb:orca+z')
        print('activate hello world plugin')
        print(_("Hello World"))
        print(_("This is a translatable string"))
    def do_deactivate(self):
        API = self.object
        print('deactivate hello world plugin')
    def speakTest(self, script, inputEvent):
        API = self.object
        Message = self.getTranslationContext().gettext("Hello World")
        API.app.getDynamicApiManager().getAPI('OrcaState').activeScript.presentMessage('1:' + Message, resetStyles=False)
        asdf
