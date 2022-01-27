import gi, os, locale, gettext
from gi.repository import GObject
import gettext

from orca import orca_i18n

class TranslationContext():
    def __init__(self, app):
        self.app = app
        self.localeDir = orca_i18n.localedir
        self.domain = 'orca'
        self.language = 'en'
        self.fallbackToOrcaTranslation = True
        self.domainTranslation = None
        self.orcaMainTranslation = None

    def setDomain(self, domain):
        self.domain = domain
    def setLanguage(self, language):
        self.language = language
    def setLocaleDir(self, localeDir):
        self.localeDir = localeDir
    def getCurrentDefaultLocale(self):
        return locale.getdefaultlocale()[0]
    def setFallbackToOrcaTranslation(self, fallback):
        self.fallback = fallback
    def getFallbackToOrcaTranslation(self):
        return self.fallback
    def getLocaleDir(self):
        return self.localeDir
    def getLanguage(self):
        return self.language
    def getDomain(self):
        return self.domain
    def getDomainTranslation(self):
        return self.domainTranslation
    def getOrcaMainTranslation(self):
        return self.orcaMainTranslation
    def setDomainTranslation(self, domainTranslation):
        self.domainTranslation = domainTranslation
    def setOrcaMainTranslation(self, orcaMainTranslation):
        self.orcaMainTranslation = orcaMainTranslation
    def updateTranslation(self):
        self.setDomainTranslation(None)
        self.setOrcaMainTranslation(None)

        try:
            self.setLanguage(self.getCurrentDefaultLocale())
        except:
            self.setLanguage('en')
            print(e)
        if self.getFallbackToOrcaTranslation():
            orcaMainTranslation = orca_i18n
            self.setOrcaMainTranslation(orcaMainTranslation)
        try:
            domainTranslation = gettext.translation(self.getDomain(), self.getLocaleDir(), languages=[self.getLanguage()])
            self.setDomainTranslation(domainTranslation)
        except Exception as e:
            print(e)

    def gettext(self, text):
        translatedText = text
        if self.getDomainTranslation() != None:
            try:
                translatedText = self.getDomainTranslation().gettext(text)
            except Exception as e:
                print(e)
        if translatedText == text:
            if self.getFallbackToOrcaTranslation() or self.getDomainTranslation() == None:
                if self.getOrcaMainTranslation() != None:
                    try:
                        translatedText = self.getOrcaMainTranslation().cgettext(text) # gettext from orca_i18n
                    except Exception as e:
                        print(e)
        return translatedText

    def ngettext(self, singular, plural, n):
        translatedText = singular
        if n > 1:
            translatedText = plural
        if self.getDomainTranslation() != None:
            try:
                translatedText = self.getDomainTranslation().ngettext(singular, plural, n)
            except:
                pass
        if translatedText in [singular, plural]: # not translated
            if self.getFallbackToOrcaTranslation() or self.getDomainTranslation() == None:
                if self.getOrcaMainTranslation() != None:
                    try:
                        translatedText = self.getOrcaMainTranslation().ngettext(singular, plural, n)
                    except:
                        pass
        return translatedText
