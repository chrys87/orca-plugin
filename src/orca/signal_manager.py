import gi
from gi.repository import GObject


class SignalManager():
    def __init__(self, app):
        self.app = app
    def registerSignal(self, signalName, signalFlag = GObject.SignalFlags.RUN_LAST, closure = GObject.TYPE_NONE, accumulator=()):
        # register signal
        if not self.signalExist(signalName):
            GObject.signal_new(signalName, self.app, signalFlag, closure,accumulator)
    def signalExist(self, signalName):
        return GObject.signal_lookup(signalName, self.app) != 0
    def connectSignal(self, signalName, function, param = None):
        try:
            if self.signalExist(signalName):
                self.app.connect(signalName, function)
            else:
                print('signal {} does not exist'.format(signalName))
        except:
            pass
    def disconnectSignalByFunction(self, function):
        try:
            self.app.disconnect_by_func(function)
        except:
            pass
    def emitSignal(self, signalName):
        # emit an signal
        try:
            self.app.emit(signalName)
            print('after Emit Signal: {}'.format(signalName))
        except:
            print('Signal "{}" does not exist.'.format(signalName))
