# Orca
#
# Copyright 2004-2009 Sun Microsystems Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""Manages the default speech server for orca.  A script can use this
as its speech server, or it can feel free to create one of its own."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2005-2009 Sun Microsystems Inc."
__license__   = "LGPL"

import importlib
import time

from . import debug
from . import logger
from . import settings
from . import speech_generator
from .speechserver import VoiceFamily

from .acss import ACSS

_logger = logger.getLogger()
log = _logger.newLog("speech")

# The speech server to use for all speech operations.
#
_speechserver = None

# The last time something was spoken.
_timestamp = 0

def _initSpeechServer(moduleName, speechServerInfo):

    global _speechserver

    if not moduleName:
        return

    factory = None
    try:
        factory = importlib.import_module(f'orca.{moduleName}')
    except Exception:
        try:
            factory = importlib.import_module(moduleName)
        except Exception:
            debug.printException(debug.LEVEL_SEVERE)

    # Now, get the speech server we care about.
    #
    speechServerInfo = settings.speechServerInfo
    if speechServerInfo:
        _speechserver = factory.SpeechServer.getSpeechServer(speechServerInfo)

    if not _speechserver:
        _speechserver = factory.SpeechServer.getSpeechServer()
        if speechServerInfo:
            msg = f'SPEECH: Invalid speechServerInfo: {speechServerInfo}'
            debug.println(debug.LEVEL_INFO, msg, True)

    if not _speechserver:
        raise Exception(f"ERROR: No speech server for factory: {moduleName}")

def init():
    debug.println(debug.LEVEL_INFO, 'SPEECH: Initializing', True)
    if _speechserver:
        debug.println(debug.LEVEL_INFO, 'SPEECH: Already initialized', True)
        return

    try:
        moduleName = settings.speechServerFactory
        _initSpeechServer(moduleName,
                          settings.speechServerInfo)
    except Exception:
        moduleNames = settings.speechFactoryModules
        for moduleName in moduleNames:
            if moduleName != settings.speechServerFactory:
                try:
                    _initSpeechServer(moduleName, None)
                    if _speechserver:
                        break
                except Exception:
                    debug.printException(debug.LEVEL_SEVERE)

    if _speechserver:
        msg = f'SPEECH: Using speech server factory: {moduleName}'
        debug.println(debug.LEVEL_INFO, msg, True)
    else:
        msg = 'SPEECH: Not available'
        debug.println(debug.LEVEL_INFO, msg, True)

    debug.println(debug.LEVEL_INFO, 'SPEECH: Initialized', True)

def checkSpeechSetting():
    msg = "SPEECH: Checking speech setting."
    debug.println(debug.LEVEL_INFO, msg, True)

    if not settings.enableSpeech:
        shutdown()
    else:
        init()

def __resolveACSS(acss=None):
    if isinstance(acss, ACSS):
        family = acss.get(acss.FAMILY)
        try:
            family = VoiceFamily(family)
        except Exception:
            family = VoiceFamily({})
        acss[acss.FAMILY] = family
        return acss
    elif isinstance(acss, list) and len(acss) == 1:
        return ACSS(acss[0])
    elif isinstance(acss, dict):
        return ACSS(acss)
    else:
        voices = settings.voices
        return ACSS(voices[settings.DEFAULT_VOICE])

def sayAll(utteranceIterator, progressCallback):
    if settings.silenceSpeech:
        return
    if _speechserver:
        _speechserver.sayAll(utteranceIterator, progressCallback)
    else:
        for [context, acss] in utteranceIterator:
            logLine = "SPEECH OUTPUT: '" + context.utterance + "'"
            debug.println(debug.LEVEL_INFO, logLine, True)
            log.info(logLine)

def cancel():
    if _speechserver:
        try:
            _speechserver._cancel()
        except:
            pass


def _speak(text, acss, interrupt):
    """Speaks the individual string using the given ACSS."""

    logLine = "SPEECH OUTPUT: '" + text + "'"
    extraDebug = ""
    if acss in list(settings.voices.values()):
        for key in settings.voices:
            if acss == settings.voices[key]:
                if key != settings.DEFAULT_VOICE:
                    extraDebug = f" voice={key}"
                break

    debug.println(debug.LEVEL_INFO, logLine + extraDebug + str(acss), True)
    log.info(logLine + extraDebug)

    if _speechserver:
        voice = ACSS(settings.voices.get(settings.DEFAULT_VOICE))
        try:
            voice.update(__resolveACSS(acss))
        except Exception:
            pass
        _speechserver.speak(text, __resolveACSS(voice), interrupt)

def speak(content, acss=None, interrupt=True):
    """Speaks the given content.  The content can be either a simple
    string or an array of arrays of objects returned by a speech
    generator."""

    if settings.silenceSpeech:
        return

    validTypes = (str, list, speech_generator.Pause,
                  speech_generator.LineBreak, ACSS)
    error = "SPEECH: bad content sent to speak(): '%s'"
    if not isinstance(content, validTypes):
        debug.printStack(debug.LEVEL_WARNING)
        debug.println(debug.LEVEL_WARNING, error % content, True)
        return

    global _timestamp
    if _timestamp:
        msg = f"SPEECH: Last spoke {time.time() - _timestamp:.4f} seconds ago"
        debug.println(debug.LEVEL_INFO, msg, True)
    _timestamp = time.time()

    if isinstance(content, str):
        _speak(content, acss, interrupt)
    if not isinstance(content, list):
        return

    toSpeak = []
    activeVoice = ACSS(acss)
    for element in content:
        if not isinstance(element, validTypes):
            debug.println(debug.LEVEL_WARNING, error % element, True)
        elif isinstance(element, list):
            speak(element, acss, interrupt)
        elif isinstance(element, str):
            if len(element):
                toSpeak.append(element)
        elif toSpeak:
            newVoice = ACSS(acss)
            newItemsToSpeak = []
            if isinstance(element, speech_generator.Pause):
                if toSpeak[-1] and toSpeak[-1][-1].isalnum():
                    toSpeak[-1] += '.'
            elif isinstance(element, ACSS):
                newVoice.update(element)
                if newVoice == activeVoice:
                    continue
                newItemsToSpeak.append(toSpeak.pop())

            if toSpeak:
                string = " ".join(toSpeak)
                _speak(string, activeVoice, interrupt)
            activeVoice = newVoice
            toSpeak = newItemsToSpeak

    if toSpeak:
        string = " ".join(toSpeak)
        _speak(string, activeVoice, interrupt)

def speakKeyEvent(event, acss=None):
    """Speaks a key event immediately.

    Arguments:
    - event: input_event.KeyboardEvent to speak.
    """

    if settings.silenceSpeech:
        return

    keyname = event.getKeyName()
    lockingStateString = event.getLockingStateString()
    acss = __resolveACSS(acss)
    msg = f"{keyname} {lockingStateString}"
    logLine = f"SPEECH OUTPUT: '{msg.strip()}' {acss}"
    debug.println(debug.LEVEL_INFO, logLine, True)
    log.info(logLine)

    if _speechserver:
        _speechserver.speakKeyEvent(event, acss)

def speakCharacter(character, acss=None):
    """Speaks a single character immediately.

    Arguments:
    - character: text to be spoken
    - acss:      acss.ACSS instance; if None,
                 the default voice settings will be used.
                 Otherwise, the acss settings will be
                 used to augment/override the default
                 voice settings.
    """
    if settings.silenceSpeech:
        return

    acss = __resolveACSS(acss)
    msg = "SPEECH OUTPUT: '" + character + "' " + str(acss)
    debug.println(debug.LEVEL_INFO, msg, True)
    log.info(f"SPEECH OUTPUT: '{character}'")

    if _speechserver:
        _speechserver.speakCharacter(character, acss=acss)

def getInfo():
    info = None
    if _speechserver:
        info = _speechserver.getInfo()

    return info

def stop():
    if _speechserver:
        _speechserver.stop()

def shutdown():
    debug.println(debug.LEVEL_INFO, 'SPEECH: Shutting down', True)
    global _speechserver
    if _speechserver:
        _speechserver.shutdownActiveServers()
        _speechserver = None

def reset(text=None, acss=None):
    if _speechserver:
        _speechserver.reset(text, acss)

def getSpeechServer():
    return _speechserver
