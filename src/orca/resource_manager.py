class TryFunction():
    def __init__(self, function):
        self.function = function
    def runSignal(self, app):
        try:
            self.function(app)
        except Exception as e:
            print('try',e)
    def runInputEvent(self, script, inputEvent):
        try:
            self.function(script, inputEvent)
        except Exception as e:
            print('try',e)
    def getFunction(self):
        return self.function
    def setFunction(self, function):
        self.function = function

class ResourceEntry():
    def __init__(self, entryType, resource, function, tryFunction, resourceText):
        self.entryType = entryType # 'keyboard' = Keyboard, 'subscription' = Subscription, 'signal' = Signal, 'api'= Dynamic API
        self.resource = resource
        self.function = function
        self.tryFunction = tryFunction
        self.resourceText = resourceText

    def getEntryType(self):
        return self.entryType
    def getResourceText(self):
        return self.resourceText
    def getResource(self):
        return self.resource
    def getFunction(self):
        return self.function
    def getTryFunction(self):
        return self.tryFunction

class ResourceContext():
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.gestures = {} # gestures added by the context
        self.subscriptions = {} # subscription to signals by the context
        self.apis = {}
        self.signals = {}
    def getName(self):
        return self.name
    def getGestures(self):
        return self.gestures
    def getSubscriptions(self):
        return self.subscriptions
    def getSignals(self):
        return self.signals
    def getAPIs(self):
        return self.apis
    def hasAPI(self, application, api):
        try:
            d = self.getAPIs()[application][api]
            return True
        except KeyError:
            return False
    def addAPI(self, application, api, entry):
        # add application
        try:
            d = self.apis[application]
        except KeyError: 
            self.apis[application] = {}
        # add entry
        self.apis[application][api] = entry
        print('add', 'api', self.getName(), application, api)

    def removeAPI(self, application, api):
        try:
            del self.apis[application][api]
        except KeyError as e: 
            print(e)
        try:
            if len(self.getAPIs()[application]) == 0:
                del self.apis[application]
        except KeyError:
            pass
        print('remove', 'apis', self.getName(), application, api)

    def addGesture(self, profile, application, gesture, entry):
        # add profile
        try:
            d = self.gestures[profile]
        except KeyError: 
            self.gestures[profile]= {}
        # add application
        try:
            d = self.gestures[profile][application]
        except KeyError: 
            self.gestures[profile][application] = {}
        # add entry
        self.gestures[profile][application][gesture] = entry
        print('add', 'gesture', self.getName(), profile, application, entry.getResourceText())
    def removeGesture(self, gesture):
        gestureCopy = self.getGestures().copy()
        for profile, applicationDict in gestureCopy.items():
            for application, keyDict in applicationDict.copy().items():
                try:
                    del self.getGestures()[profile][application][gesture]
                    if len(self.getGestures()[profile][application]) == 0:
                        del self.getGestures()[profile][application]
                    if len(self.getGestures()[profile]) == 0:
                        del self.getGestures()[profile]
                except KeyError:
                    pass

        print('remove', 'gesture', self.getName(), profile, application, gesture)

    def addSubscription(self, signalName, function, entry):
        # add entry
        try:
            e = self.subscriptions[signalName]
        except KeyError:
            self.subscriptions[signalName] = {}
        self.subscriptions[signalName][function] = entry
        print('add', 'subscription', self.getName(), entry.getResourceText())

    def removeSubscriptionByFunction(self, function):
        for signalName, functionDict in self.getSubscriptions().copy().items():
            for function, entry in functionDict.copy().items():
                try:
                    del self.getSubscriptions()[signalName][entry.function]
                except KeyError as e: 
                    print(e)

                try:
                    if len(self.getSubscriptions()[signalName]) == 0:
                        del self.getSubscriptions()[signalName]
                except KeyError:
                    pass
        print('remove', 'subscription', self.getName(), function)
    def addSignal(self, signal, entry):
        # add entry
        self.signals[signal] = entry
        print('add', 'signal', self.getName(), entry.getResourceText())
    def removeSignal(self, signal):
        print('remove', 'signal', self.getName(), entry.getResourceText())

    def unregisterAllResources(self):
        try:
            self.unregisterAllGestures()
            self.unregisterAllSubscriptions()
            self.unregisterAllSignals()
            self.unregisterAllAPI()
        except Exception as e:
            print(e)
        
    def unregisterAllAPI(self):
        dynamicApiManager = self.app.getDynamicApiManager()
        for application, value in self.getAPIs().copy().items():
            for key, entry in value.items():
                try:
                    dynamicApiManager.unregisterAPI(self.getName(), key, application)
                except Exception as e:
                    print(e)
                print('unregister api ', self.getName(), entry.getEntryType(), entry.getResourceText())
    def unregisterAllGestures(self):
        APIHelper = self.app.getAPIHelper()
        
        for profile, profileValue in self.getGestures().copy().items():
            for application, applicationValue in profileValue.copy().items():
                for gesture, entry in applicationValue.copy().items():
                    if entry.getEntryType() == 'keyboard':
                        try:
                            APIHelper.unregisterShortcut(self.getName(), entry.getResource())
                        except Exception as e:
                            print(e)
                        print('unregister gesture', self.getName(), entry.getEntryType(), profile, application, entry.getResourceText())
    def unregisterAllSignals(self):
        pass
        # how to remove signals????

    def unregisterAllSubscriptions(self):
        SignalManager = self.app.getSignalManager()

        for signalName, entryList in self.getSubscriptions().copy().items():
            for function, entry in entryList.copy().items():
                try:
                    SignalManager.disconnectSignalByFunction(self.getName(), entry.tryFunction)
                except Exception as e:
                    print(e)
                print('unregister subscription', self.getName(), entry.getEntryType(), entry.getResourceText())

class ResourceManager():
    def __init__(self, app):
        self.app = app
        self.resourceContextDict = {}
    def getResourceContextDict(self):
        return self.resourceContextDict

    def addResourceContext(self, contextName, overwrite = False):
        if not contextName:
            return
        resourceContext = self.getResourceContext(contextName)
        if resourceContext:
            if not overwrite:
                return
        resourceContext = ResourceContext(self.app, contextName)
        self.resourceContextDict[contextName] = resourceContext
        print('add {}'.format(contextName))

    def removeResourceContext(self, contextName):
        if not contextName:
            return
        
        try:
            self.resourceContextDict[contextName].unregisterAllResources()
        except:
            pass
        
        # temp
        try:
            print('api', self.resourceContextDict[contextName].getAPIs())
            print('signals', self.resourceContextDict[contextName].getSignals())
            print('subscriptions', self.resourceContextDict[contextName].getSubscriptions())
            print('gestrues ', self.resourceContextDict[contextName].getGestures())
            print('_________', self.resourceContextDict[contextName].getName(), '_________')
        except:
            pass
        # temp
        try:
            del self.resourceContextDict[contextName]
        except KeyError:
            pass
        print('rm {}'.format(contextName))

    def getResourceContext(self, contextName):
        if not contextName:
            return None
        try:
            return self.resourceContextDict[contextName]
        except KeyError:
            return None
        
    def addAPI(self, application, api, contextName = None):
        if not contextName:
            return
        resourceContext = self.getResourceContext(contextName)
        if not resourceContext:
            return
        entry = None
        resourceContext.addAPI(application, api, entry)
    def removeAPI(self, application, api, contextName = None):
        if not contextName:
            return
        resourceContext = self.getResourceContext(contextName)
        if not resourceContext:
            return
        resourceContext.removeAPI(application, api)
    def addGesture(self, profile, application, gesture, entry, contextName = None):
        if not contextName:
            return
        resourceContext = self.getResourceContext(contextName)
        if not resourceContext:
            return
        entry = None
        resourceContext.addGesture(profile, application, gesture, entry)
    def removeGesture(self, gesture, contextName = None):
        if not contextName:
            return
        resourceContext = self.getResourceContext(contextName)
        if not resourceContext:
            return
        resourceContext.removeGesture(gesture)
    def addSubscription(self, subscription, entry, contextName = None):
        if not contextName:
            return
        resourceContext = self.getResourceContext(contextName)
        if not resourceContext:
            return
        entry = None
        resourceContext.addSubscription(subscription, entry)
    def removeSubscriptionByFunction(self, function, contextName = None):
        if not contextName:
            return
        resourceContext = self.getResourceContext(contextName)
        if not resourceContext:
            return
        resourceContext.removeSubscriptionByFunction(function)
    def addSignal(self, signal, entry, contextName = None):
        if not contextName:
            return
        resourceContext = self.getResourceContext(contextName)
        if not resourceContext:
            return
        entry = None
        resourceContext.addSignal(signal, entry)
    def removeSignal(self, signal, contextName = None):
        if not contextName:
            return
        resourceContext = self.getResourceContext(contextName)
        if not resourceContext:
            return
        resourceContext.removeSignal(signal)
    def printContext(self):
        for k, v in self.resourceContextDict.items():
            print('plugin', k)
            for k1, v1 in v.getGestures().items():
                print('  profile', k1)
                for k2, v2 in v1.items():
                    print('    application', k2)
                    for k3, v3 in v2.items():
                        print('    value', k3, v3)
