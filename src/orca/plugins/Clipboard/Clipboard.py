import gi, os
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class Clipboard(GObject.Object, Peas.Activatable):
    #__gtype_name__ = 'Clipboard'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        self.keybinding = None
    def do_activate(self):
        API = self.object
        self.setKeybinding('w')
    def do_deactivate(self):
        API = self.object
        self.setKeybinding(None)
    def do_update_state(self):
        API = self.object
    def setKeybinding(self, keybinding):
        API = self.object
        if keybinding == None:
            API.app.getAPIHelper().unregisterShortcut(self.keybinding)
        else:
            keybinding = keybinding = API.app.getAPIHelper().registerShortcut(self.speakClipboard, keybinding, 'clipboard')
        self.keybinding = keybinding
    def speakClipboard(self, script, inputEvent):
        API = self.object
        Message = self.getClipboard()
        API.app.getDynamicApiManager().getAPI('OrcaState').activeScript.presentMessage(Message, resetStyles=False)
    def getClipboard(self):
        Message = ""
        FoundClipboardContent = False
        # Get Clipboard
        ClipboardObj = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        ClipboardText = ClipboardObj.wait_for_text()
        ClipboardImage = ClipboardObj.wait_for_image()

        if (ClipboardText != None):
            FoundClipboardContent = True
            if (ClipboardObj.wait_is_uris_available()):
                UriList = ClipboardText.split('\n')
                ObjectNo = 0
                for Uri in UriList:
                    ObjectNo += 1
                    if (os.path.isdir(Uri)):
                        Message = Message + "Folder" #Folder
                    if (os.path.isfile(Uri)):
                        Message = Message + "File" #File
                    if (os.path.ismount(Uri)):
                        Message = Message + "Disk" #Mountpoint
                    if (os.path.islink(Uri)):
                        Message = Message + "Link" #Link
                    Message += " " + Uri[Uri.rfind('/') + 1:] + " "
                if (ObjectNo > 1):			
                    Message = str(ObjectNo) + " Objects in clipboard " + Message # X Objects in Clipboard Object Object
                else:
                    Message = str(ObjectNo) + " Object in clipboard " + Message # 1 Object in Clipboard Object
            else:		
                Message = "Text in clipboard " + ClipboardText # Text in Clipboard

        if (ClipboardImage != None):
            FoundClipboardContent = True
            Message = "The clipboard contains a image" # Image is in Clipboard

        if (not FoundClipboardContent):
            Message = "The clipboard is empty"
        return Message
