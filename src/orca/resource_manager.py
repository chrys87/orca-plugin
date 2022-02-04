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

        if len(self.getAPIs()[application]) == 0:
            del self.apis[application]
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
    def removeGesture(self, entry):
        print('try remove gesture')
        gestureCopy = self.getGestures().copy()
        for profile, applicationDict in gestureCopy.items():
            for application, keyDict in applicationDict.items():
                try:
                    del self.getGestures()[profile][application][entry]
                    if len(self.getGestures()[profile][application]) == 0:
                        del self.getGestures()[profile][application]
                    if len(self.getGestures()[profile]) == 0:
                        del self.getGestures()[profile]
                except KeyError:
                    pass
                except Exception as e:
                    print(e)
        print('remove', 'gesture', self.getName(), profile, application, entry.getResourceText())

    def addSubscription(self, subscription, entry):
        # add entry
        try:
            e = self.subscriptions[subscription]
        except KeyError:
            self.subscriptions[subscription] = []
        self.subscriptions[subscription].append(entry)
        print('add', 'subscription', self.getName(), entry.getResourceText())
    def removeSubscriptionByFunction(self, function):
        print('remove subscription by function:', function)
        subscriptionsCopy = self.getSubscriptions().copy()
        for signalName, functionList in subscriptionsCopy.items():
            try:
                del self.getSubscriptions()[function]
            except ValueError as e: 
                print(e)
                print(subscriptionsCopy)
            if len(self.getSubscriptions()[signalName]) == 0:
                del self.getSubscriptions()[signalName]
        print('remove', 'subscription', self.getName(), function)
    def addSignal(self, signal, entry):
        # add entry
        self.signals[signal] = entry
        print('add', 'signal', self.getName(), entry.getResourceText())
    def removeSignal(self, signal):
        try:
            e = self.signals[signal]
        except KeyError:
            pass
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
        apiCopy = self.getAPIs().copy()

        for application, value in apiCopy.items():
            for key, entry in value.items():
                dynamicApiManager.unregisterAPI(self.getName(), key, application)
                print('unregister api ', self.getName(), entry.getEntryType(), entry.getResourceText())
    def unregisterAllGestures(self):
        APIHelper = self.app.getAPIHelper()
        
        gestureCopy = self.getGestures().copy()
        for profile, profileValue in gestureCopy.items():
            for application, applicationValue in profileValue.items():
                for gesture, entry in applicationValue.items():
                    if entry.getEntryType() == 'keyboard':
                        try:
                            APIHelper.unregisterShortcut(self.getName(), entry.getResource())
                        except Exception as e:
                            pass
                        print('unregister gesture', self.getName(), entry.getEntryType(), profile, application, entry.getResourceText())
    def unregisterAllSignals(self):
        pass
        # how to remove signals????

    def unregisterAllSubscriptions(self):
        SignalManager = self.app.getSignalManager()
        
        subscriptionsCopy = self.getSubscriptions().copy()

        for subscription, entryList in subscriptionsCopy.items():
            for entry in entryList:
                try:
                    SignalManager.disconnectSignalByFunction(self.getName(), entry.mappedFunction)
                except Exception as e:
                    print(e)
                print('unregister subscription', self.getName(), entry.getEntryType(), entry.getResourceText())

class ResourceManager():
    def __init__(self, app):
        self.app = app
        self.resourceContextDict = {}
    def getResourceContextDict(self):
        return self.resourceContextDict
    '''
    def searchResourceContextByAPI(self, api, application):
        resourceContextList = []
        for contextName, resourceContext in self.getResourceContextDict().items():
            resourceContext.hasAPI(api, application):
                resourceContextList.append(resourceContext)
        return resourceContextList
    def removeResourceContextByAPI(self, application, api):
        resourceContextList = self.searchResourceContextByAPI(application, api)
        for resourceContext in resourceContextList:
            resourceContext.removeAPI(application, api)

    def searchResourceContextBySubscription(self, function):
        resourceContextList = []
        for contextName, resourceContext in self.getResourceContextDict().items():
            resourceContext.hasSubscriptionWithFunction(function):
                resourceContextList.append(resourceContext)
        return resourceContextList
    def removeResourceContextSubscriptionByFunction(self, function):
        resourceContextList = self.searchResourceContextBySubscription(function)
        for resourceContext in resourceContextList:
            resourceContext.removeSubscriptionByFunction(function)

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
