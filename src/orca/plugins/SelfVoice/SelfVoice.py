# Example usage:
# echo "This is a test." | socat - UNIX-CLIENT:/tmp/orca-PID.sock
# Where PID is orca's process id.
# Prepend text to be spoken with <!#APPEND#!> to make it not interrupt, for inaccessible windows.
# Append message to be spoken with <#PERSISTENT#> to present a persistent message in braille
# <#APPEND#> is only usable for a persistent message

from orca import plugin

import gi
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas
import select, socket, os, os.path
from threading import Thread, Lock

APPEND_CODE = '<#APPEND#>'
PERSISTENT_CODE = '<#PERSISTENT#>'

class SelfVoice(GObject.Object, Peas.Activatable, plugin.Plugin):
    __gtype_name__ = 'SelfVoice'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
        self.lock = Lock()
        self.active = False
        self.voiceThread = Thread(target=self.voiceWorker)
    def do_activate(self):
        API = self.object
        self.activateWorker()
    def do_deactivate(self):
        API = self.object
        self.deactivateWorker()
    def do_update_state(self):
        API = self.object
    def deactivateWorker(self):
        with self.lock:
            self.active = False
        self.voiceThread.join()
    def activateWorker(self):
        with self.lock:
            self.active = True
        self.voiceThread.start()
    def isActive(self):
        with self.lock:
            return self.active
    def outputMessage(self,  Message):
        # Prepare
        API = self.object
        append = Message.startswith(APPEND_CODE)
        if append:
            Message = Message[len(APPEND_CODE):]
        if Message.endswith(PERSISTENT_CODE):
            Message = Message[:len(Message)-len(PERSISTENT_CODE)]
            API.app.getAPIHelper().outputMessage(Message, not append)
        else:
            script_manager = API.app.getDynamicApiManager().getAPI('ScriptManager')
            scriptManager = script_manager.getManager()
            scriptManager.getDefaultScript().presentMessage(Message, resetStyles=False)
        return
        try:
            settings = API.app.getDynamicApiManager().getAPI('Settings')
            braille = API.app.getDynamicApiManager().getAPI('Braille')
            speech = API.app.getDynamicApiManager().getAPI('Speech')
            # Speak
            if speech != None:
                if (settings.enableSpeech):
                    if not append:
                        speech.cancel()
                    if Message != '':
                        speech.speak(Message)
            # Braille
            if braille != None:
                if (settings.enableBraille):
                    braille.displayMessage(Message)
        except e as Exception:
            print(e)

    def voiceWorker(self):
        socketFile = '/tmp/orca-' + str(os.getppid()) + '.sock'
        # for testing purposes
        #socketFile = '/tmp/orca-plugin.sock'

        if os.path.exists(socketFile):
            os.unlink(socketFile)
        orcaSock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        orcaSock.bind(socketFile)
        os.chmod(socketFile, 0o222)
        orcaSock.listen(1)
        while self.isActive():
            # Check if the client is still connected and if data is available:
            try:
                r, _, _ = select.select([orcaSock], [], [], 0.8)
            except select.error:
                break
            if r == []:
                continue
            if orcaSock in r:
                client_sock, client_addr = orcaSock.accept()
            try:
                rawdata = client_sock.recv(8129)
                data = rawdata.decode("utf-8").rstrip().lstrip()
                self.outputMessage(data)
            except:
                pass
            try:
                client_sock.close()
            except:
                pass
        if orcaSock:
            orcaSock.close()
            orcaSock = None
        if os.path.exists(socketFile):
            os.unlink(socketFile)


