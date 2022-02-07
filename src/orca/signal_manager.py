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
            ok = True
        if contextName:
            resourceContext = self.resourceManager.getResourceContext(contextName)
            if resourceContext:
                resourceEntry = resource_manager.ResourceEntry('signal', signalName, signalName, signalName, signalName)
                resourceContext.addSignal(signalName, resourceEntry)
        return ok

    def signalExist(self, signalName):
        return GObject.signal_lookup(signalName, self.app) != 0
    def connectSignal(self, contextName, signalName, function, profile, param = None):
        signalID = None
        #try:
        if self.signalExist(signalName):
            tryFunction = resource_manager.TryFunction(function)
            signalID = self.app.connect(signalName, tryFunction.runSignal)
        if contextName:
            resourceContext = self.resourceManager.getResourceContext(contextName)
            if resourceContext:
                resourceEntry = resource_manager.ResourceEntry('subscription', signalID, function, tryFunction, signalName)
                resourceContext.addSubscription(signalName, function, resourceEntry)
        #    else:
        #        print('signal {} does not exist'.format(signalName))
        #except Exception as e:
        #    print(e)
        return signalID
    def disconnectSignalByFunction(self, contextName, function):
        ok = False
        try:
            self.app.disconnect_by_func(function)
            ok = True
        except:
            pass
        if contextName:
            resourceContext = self.resourceManager.getResourceContext(contextName)
            if resourceContext:
                resourceContext.removeSubscriptionByFunction(function)
        return ok
    def emitSignal(self, signalName):
        # emit an signal
        try:
            self.app.emit(signalName)
            #print('after Emit Signal: {}'.format(signalName))
        except:
            print('Signal "{}" does not exist.'.format(signalName))
