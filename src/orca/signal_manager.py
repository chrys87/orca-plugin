import gi
from gi.repository import GObject

from orca import resource_manager

class SignalManager():
    def __init__(self, app):
        self.app = app
        self.resourceManager = self.app.getResourceManager()

    def registerSignal(self, contextName, signalName, signalFlag = GObject.SignalFlags.RUN_LAST, closure = GObject.TYPE_NONE, accumulator=()):
        # register signal
        ok = False
        if not self.signalExist(signalName):
            GObject.signal_new(signalName, self.app, signalFlag, closure,accumulator)
            resourceContext = self.resourceManager.getResourceContext(contextName)
            resourceEntry = resource_manager.ResourceEntry('signal', signalName, signalName, signalName, signalName)
            resourceContext.addSignal(signalName, resourceEntry)
            ok = True
        return ok

    def signalExist(self, signalName):
        return GObject.signal_lookup(signalName, self.app) != 0
    def connectSignal(self, contextName, signalName, function, profile, param = None):
        signalID = None
        #try:
        if self.signalExist(signalName):
            signalID = self.app.connect(signalName, function)

            resourceContext = self.resourceManager.getResourceContext(contextName)
            resourceEntry = resource_manager.ResourceEntry('subscription', signalID, function, function, signalName)
            resourceContext.addSubscription(function, resourceEntry)
        #    else:
        #        print('signal {} does not exist'.format(signalName))
        #except Exception as e:
        #    print(e)
        return signalID
    def disconnectSignalByFunction(self, contextName, function):
        ok = False
        resourceContext = self.resourceManager.getResourceContext(contextName)
        try:
            self.app.disconnect_by_func(function)
            resourceContext.removeSubscriptionByFunction(function)
            ok = True
        except:
            pass
        return ok
    def emitSignal(self, signalName):
        # emit an signal
        try:
            self.app.emit(signalName)
            print('after Emit Signal: {}'.format(signalName))
        except:
            print('Signal "{}" does not exist.'.format(signalName))
