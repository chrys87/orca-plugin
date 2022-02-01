class ResourceEntry():
    def __init__(self, entryType, resource, function, mappedFunction, resourceText):
        self.entryType = entryType # 'keyboard' = Keyboard, 'subscription' = Subscription, 'signal' = Signal
        self.resource = resource
        self.function = function
        self.mappedFunction = mappedFunction
        self.resourceText = resourceText

    def getEntryType(self):
        return self.entryType
    def getResourceText(self):
        return self.resourceText
    def getResource(self):
        return self.resource
    def getFunction(self):
        return self.function
    def getMappedFunction(self):
        return self.mappedFunction

class ResourceContext():
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.gestures = {} # gestures added by the context
        self.subscriptions = {} # subscription to signals by the context
        self.apis = {}
    def getGestures(self):
        return self.gestures
    def getSubscriptions(self):
        return self.subscriptions
    def getSignals(self):
        return self.signals
    def getAPIs(self):
        return self.apis
    def hasAPI(self, api, application):
        try:
            d = self.getAPIs()[application][api]
            return True
        except:
            return False
    def addAPI(self, application, api, entry):
        # add application
        try:
            d = self.apis[application]
        except KeyError: 
            self.apis[application] = {}
        # add entry
        self.apis[application][api] = entry

        #print('register', 'apis', self.name, application, entry.getResourceText())

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
        #print('register', 'gesture', self.name, profile, application, entry.getResourceText())

    def addSubscription(self, subscription, entry):
        # add entry
        try:
            e = self.subscriptions[subscription]
        except KeyError:
            self.subscriptions[subscription] = []
        self.subscriptions[subscription].append(entry)
        #print('register', 'subscription', self.name, entry.getResourceText())

    def addSignal(self, signal, entry):
        # add entry
        self.signals[signal] = entry
        #print('register', 'signal', self.name, entry.getResourceText())

    def unregisterAllResources(self):
        try:
            self.unregisterAllGestures()
            self.unregisterAllSubscriptions()
            self.unregisterAllSignals()
            self.unregisterAllAPI()
        except Exception as e:
            print(e)
    def removeAPI(self, api, application):
        try:
            del self.apis[application][api]
        except:
            pass
        
    def unregisterAllAPI(self):
        dynamicApiManager = self.app.getDynamicApiManager()
        apiCopy = self.getAPIs().copy()

        for application, value in apiCopy.items():
            for key, entry in value.items():
                dynamicApiManager.unregisterAPI(key, application)
                #print('unregister ', self.name, entry.getEntryType(), entry.getResourceText())
    def unregisterAllGestures(self):
        APIHelper = self.app.getAPIHelper()
        
        gestureCopy = self.getGestures().copy()
        for profile, profileValue in gestureCopy.items():
            for application, applicationValue in profileValue.items():
                for gesture, entry in applicationValue.items():
                    if entry.getEntryType() == 'keyboard':
                        try:
                            APIHelper.unregisterShortcut(entry.getResource())
                        except Exception as e:
                            pass
                        #print('unregister ', self.name, entry.getEntryType(), profile, application, entry.getResourceText())
    def unregisterAllSignals(self):
        pass
        # how to remove signals????

    def unregisterAllSubscriptions(self):
        SignalManager = self.app.getSignalManager()
        
        subscriptionsCopy = self.getSubscriptions().copy()

        for subscription, entryList in subscriptionsCopy.items():
            for entry in entryList:
                try:
                    SignalManager.disconnectSignalByFunction(entry.mappedFunction)
                except Exception as e:
                    print(e)
                    print('unregister ', self.name, entry.getEntryType(), entry.getResourceText())

class ResourceManager():
    def __init__(self, app):
        self.app = app
        self.resourceContextDict = {}
    def getResourceContextDict(self):
        return self.resourceContextDict
'''    
    def searchResourceContextByAPI(self, api, application):
        for contextName, resourceContext in self.getResourceContextDict().items():
            resourceContext.hasAPI(api, application):
                return resourceContext
        return None
    def searchResourceContextBySubscription(self, api, application):
        for contextName, resourceContext in self.getResourceContextDict().items():
            return resourceContext
        return None
    def searchResourceContextBySignal(self, api, application):
        for contextName, resourceContext in self.getResourceContextDict().items():
            resourceContext.hasSignal(api, application):
                return resourceContext
        return None
    def searchResourceContextByGesture(self, api, application):
        for contextName, resourceContext in self.getResourceContextDict().items():
            resourceContext.hasGesture(api, application):
                return resourceContext
        return None
'''
    def addResourceContext(self, contextName):
        try:
            d = self.resourceContextDict[contextName]
            return
        except KeyError:
            pass

        resourceContext = ResourceContext(self.app, contextName)

        self.resourceContextDict[contextName] = resourceContext
        print('add {}'.format(contextName))
    def removeResourceContext(self, contextName):
        try:
            self.resourceContextDict[contextName].unregisterAllResources()
        except:
            pass
        try:
            del self.resourceContextDict[contextName]
        except:
            pass
        print('rm {}'.format(contextName))

    def getResourceContext(self, contextName):
        try:
            return self.resourceContextDict[contextName]
        except KeyError:
            return None
    def printContext(self):
        for k, v in self.resourceContextDict.items():
            print('plugin', k)
            for k1, v1 in v.getGestures().items():
                print('  profile', k1)
                for k2, v2 in v1.items():
                    print('    application', k2)
                    for k3, v3 in v2.items():
                        print('    value', k3, v3)
'''
class ResourceContext():
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.signals = {} # signals added by the context
        self.gestures = {} # gestures added by the context
        self.subscriptions = {} # subscription to signals by the context
    def getGestures(self):
        return self.gestures
    def getSignals(self):
        return self.signals
    def getSubscriptions(self):
        return self.subscriptions
    def addSignal(self, signal):
        pass
    def removeSignal(self):
        pass
    def gestureExists(self, gesture):
        return self.doesExist(self.getGestures(), gesture)
    def signalExists(self, signal):
        return self.doesExist(self.getSignals(), signal)
    def subscriptionExists(self, subscription):
        return self.doesExist(self.getSubscriptions(), subscription)
    def doesExist(self, searchDict, key):
        try:
            dummy = self.searchDict[key]
            return True
        except KeyError:
            return False
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
    def removeGesture(self):
        pass
    def addSubscription(self, subscription):
        pass
    def removeSubscription(self):
        pass
    def unregisterAllResourcesForContext(self):
        self.unregisterAllGestures()
        self.unregisterAllSignals()
        self.unregisterAllSubscriptions()

    def unregisterAllGestures(self):
        pass
    def unregisterAllSignals(self):
        pass
    def unregisterAllSubscriptions(self):
        pass
'''
