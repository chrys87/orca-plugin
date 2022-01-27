import gi, os, locale, gettext
from gi.repository import GObject
import gettext

from orca import orca_i18n
from orca import translation_context

class TranslationManager():
    def __init__(self, app):
        self.app = app
        self.translatioContextnDict = {}
    def initTranslation(self, name, domain = None, localeDir = None, language = None, fallbackToOrcaTranslation = True):
        translationContext = translation_context.TranslationContext(self.app)
        if os.path.isdir(localeDir):
            translationContext.setDomain(domain)
            translationContext.setLocaleDir(localeDir)
        translationContext.setLanguage(language)
        translationContext.setFallbackToOrcaTranslation(fallbackToOrcaTranslation)
        translationContext.updateTranslation()
        self.addTranslationDict(name, translationContext)
        return translationContext
    def addTranslationDict(self, name, translationContext):
        self.translatioContextnDict[name] = translationContext
    def getTranslationContextByName(name):
        try:
            return self.translatioContextnDict[name]
        except KeyError:
            return self.translatioContextnDict['orca']
    #def getTranslationsInstance(self, domain='orca'):
        """ Gets the gettext translation instance for this add-on.
        <addon-path>\\locale will be used to find .mo files, if exists.
        If a translation file is not found the default fallback null translation is returned.
        @param domain: the translation domain to retrieve. The 'orca' default should be used in most cases.
        @returns: the gettext translation class.
        """
     #   localedir = os.path.join(self.path, "locale")
     #   return gettext.translation(domain, localedir=localedir, languages=[languageHandler.getLanguage()], fallback=True)
"""
    def initTranslation():
        addon = getCodeAddon(frameDist=2)
        translations = addon.getTranslationsInstance()
        # Point _ to the translation object in the globals namespace of the caller frame
        # FIXME: should we retrieve the caller module object explicitly?
        try:
            callerFrame = inspect.currentframe().f_back
            callerFrame.f_globals['_'] = translations.gettext
            # Install our pgettext function.
            callerFrame.f_globals['pgettext'] = languageHandler.makePgettext(translations)
        finally:
            del callerFrame # Avoid reference problems with frames (per python docs)
"""

