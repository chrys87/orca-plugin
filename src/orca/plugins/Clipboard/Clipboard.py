from orca import plugin

import gi, os
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class Clipboard(GObject.Object, Peas.Activatable, plugin.Plugin):
    #__gtype_name__ = 'Clipboard'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
    def do_activate(self):
        API = self.object
        self.registerGestureByString(self.speakClipboard, _('clipboard'), 'kb:orca+c')
    def do_deactivate(self):
        API = self.object
    def do_update_state(self):
        API = self.object
    def speakClipboard(self, script=None, inputEvent=None):
        API = self.object
        Message = self.getClipboard()
        API.app.getDynamicApiManager().getAPI('OrcaState').activeScript.presentMessage(Message, resetStyles=False)
        return True
    def getClipboard(self):
        Message = ""
        FoundClipboardContent = False
        # Get Clipboard
        ClipboardObj = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        ClipboardText = ClipboardObj.wait_for_text()
        ClipboardImage = ClipboardObj.wait_for_image()
        ClipboardURI = ClipboardObj.wait_for_uris()
        if (ClipboardText != None):
            FoundClipboardContent = True
            if (ClipboardObj.wait_is_uris_available()):
                noOfObjects = 0
                noOfFolder = 0
                noOfFiles = 0
                noOfDisks = 0
                noOfLinks = 0
                for Uri in ClipboardURI:
                    if Uri == '':
                        continue
                    noOfObjects += 1
                    uriWithoutProtocoll = Uri[Uri.find('://') + 3:]
                    Message += " " + Uri[Uri.rfind('/') + 1:] + " "
                    if (os.path.isdir(uriWithoutProtocoll)):
                        noOfFolder += 1
                        Message = Message + _("Folder") #Folder
                    if (os.path.isfile(uriWithoutProtocoll)):
                        noOfFiles += 1
                        Message = Message + _("File") #File
                    if (os.path.ismount(uriWithoutProtocoll)):
                        noOfDisks += 1
                        Message = Message + _("Disk") #Mountpoint
                    if (os.path.islink(uriWithoutProtocoll)):
                        noOfLinks += 1
                        Message = Message + _("Link") #Link
                if (noOfObjects > 1):			
                    Message = str(noOfObjects) + _(" Objects in clipboard ") + Message # X Objects in Clipboard Object Object
                else:
                    Message = str(noOfObjects) + _(" Object in clipboard ") + Message # 1 Object in Clipboard Object
            else:		
                Message = _("Text in clipboard ") + ClipboardText # Text in Clipboard

        if (ClipboardImage != None):
            FoundClipboardContent = True
            Message = _("The clipboard contains a image") # Image is in Clipboard

        if (not FoundClipboardContent):
            Message = _("The clipboard is empty")
        return Message
