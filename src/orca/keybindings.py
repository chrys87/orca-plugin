# Orca
#
# Copyright 2005-2008 Sun Microsystems Inc.
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

"""Provides support for defining keybindings and matching them to input
events."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

from gi.repository import Gdk

import gi
gi.require_version('Atspi', '2.0') 
from gi.repository import Atspi

import functools

from . import debug
from . import settings
from . import orca_state

from .orca_i18n import _

_keysymsCache = {}
_keycodeCache = {}

MODIFIER_ORCA = 8
NO_MODIFIER_MASK              =  0
ALT_MODIFIER_MASK             =  1 << Atspi.ModifierType.ALT
CTRL_MODIFIER_MASK            =  1 << Atspi.ModifierType.CONTROL
ORCA_MODIFIER_MASK            =  1 << MODIFIER_ORCA
ORCA_ALT_MODIFIER_MASK        = (1 << MODIFIER_ORCA |
                                 1 << Atspi.ModifierType.ALT)
ORCA_CTRL_MODIFIER_MASK       = (1 << MODIFIER_ORCA |
                                 1 << Atspi.ModifierType.CONTROL)
ORCA_CTRL_ALT_MODIFIER_MASK   = (1 << MODIFIER_ORCA |
                                 1 << Atspi.ModifierType.CONTROL |
                                 1 << Atspi.ModifierType.ALT)
ORCA_SHIFT_MODIFIER_MASK      = (1 << MODIFIER_ORCA |
                                 1 << Atspi.ModifierType.SHIFT)
SHIFT_MODIFIER_MASK           =  1 << Atspi.ModifierType.SHIFT
SHIFT_ALT_MODIFIER_MASK       = (1 << Atspi.ModifierType.SHIFT |
                                 1 << Atspi.ModifierType.ALT)
CTRL_ALT_MODIFIER_MASK        = (1 << Atspi.ModifierType.CONTROL |
                                 1 << Atspi.ModifierType.ALT)
COMMAND_MODIFIER_MASK         = (1 << Atspi.ModifierType.ALT |
                                 1 << Atspi.ModifierType.CONTROL |
                                 1 << Atspi.ModifierType.META2 |
                                 1 << Atspi.ModifierType.META3)
NON_LOCKING_MODIFIER_MASK     = (1 << Atspi.ModifierType.SHIFT |
                                 1 << Atspi.ModifierType.ALT |
                                 1 << Atspi.ModifierType.CONTROL |
                                 1 << Atspi.ModifierType.META2 |
                                 1 << Atspi.ModifierType.META3 |
                                 1 << MODIFIER_ORCA)
defaultModifierMask = NON_LOCKING_MODIFIER_MASK

def getKeycode(keysym):
    """Converts an XKeysym string (e.g., 'KP_Enter') to a keycode that
    should match the event.hw_code for key events.

    This whole situation is caused by the fact that Solaris chooses
    to give us different keycodes for the same key, and the keypad
    is the primary place where this happens: if NumLock is not on,
    there is no telling the difference between keypad keys and the
    other navigation keys (e.g., arrows, page up/down, etc.).  One,
    for example, would expect to get KP_End for the '1' key on the
    keypad if NumLock were not on.  Instead, we get 'End' and the
    keycode for it matches the keycode for the other 'End' key.  Odd.
    If NumLock is on, we at least get KP_* keys.

    So...when setting up keybindings, we say we're interested in
    KeySyms, but those keysyms are carefully chosen so as to result
    in a keycode that matches the actual key on the keyboard.  This
    is why we use KP_1 instead of KP_End and so on in our keybindings.

    Arguments:
    - keysym: a string that is a valid representation of an XKeysym.

    Returns an integer representing a key code that should match the
    event.hw_code for key events.
    """

    if not keysym:
        return 0

    if keysym not in _keycodeCache:
        keymap = Gdk.Keymap.get_default()

        # Find the numerical value of the keysym
        #
        keyval = Gdk.keyval_from_name(keysym)
        if keyval == 0:
            return 0

        # Now find the keycodes for the keysym.   Since a keysym can
        # be associated with more than one key, we'll shoot for the
        # keysym that's in group 0, regardless of shift level (each
        # entry is of the form [keycode, group, level]).
        #
        _keycodeCache[keysym] = 0
        success, entries = keymap.get_entries_for_keyval(keyval)

        for entry in entries:
            if entry.group == 0:
                _keycodeCache[keysym] = entry.keycode
                break
            if _keycodeCache[keysym] == 0:
                _keycodeCache[keysym] = entries[0].keycode

        #print keysym, keyval, entries, _keycodeCache[keysym]

    return _keycodeCache[keysym]

def getModifierNames(mods):
    """Gets the modifier names of a numeric modifier mask as a human
    consumable string.
    """

    text = ""
    if mods & ORCA_MODIFIER_MASK:
        if settings.keyboardLayout == settings.GENERAL_KEYBOARD_LAYOUT_DESKTOP:
            # Translators: this is presented in a GUI to represent the
            # "insert" key when used as the Orca modifier.
            text += _("Insert") + "+"
        else:
            # Translators: this is presented in a GUI to represent the
            # "caps lock" modifier.
            text += _("Caps_Lock") + "+"
    elif mods & (1 << Atspi.ModifierType.SHIFTLOCK):
        # Translators: this is presented in a GUI to represent the
        # "caps lock" modifier.
        #
        text += _("Caps_Lock") + "+"
    #if mods & (1 << Atspi.ModifierType.NUMLOCK):
    #    text += _("Num_Lock") + "+"
    if mods & 128:
        # Translators: this is presented in a GUI to represent the
        # "right alt" modifier.
        #
        text += _("Alt_R") + "+"
    if mods & (1 << Atspi.ModifierType.META3):
        # Translators: this is presented in a GUI to represent the
        # "super" modifier.
        #
        text += _("Super") + "+"
    if mods & (1 << Atspi.ModifierType.META2):
        # Translators: this is presented in a GUI to represent the
        # "meta 2" modifier.
        #
        text += _("Meta2") + "+"
    #if mods & (1 << Atspi.ModifierType.META):
    #    text += _("Meta") + "+"
    if mods & ALT_MODIFIER_MASK:
        # Translators: this is presented in a GUI to represent the
        # "left alt" modifier.
        #
        text += _("Alt_L") + "+"
    if mods & CTRL_MODIFIER_MASK:
        # Translators: this is presented in a GUI to represent the
        # "control" modifier.
        #
        text += _("Ctrl") + "+"
    if mods & SHIFT_MODIFIER_MASK:
        # Translators: this is presented in a GUI to represent the
        # "shift " modifier.
        #
        text += _("Shift") + "+"
    return text

def getClickCountString(count):
    """Returns a human-consumable string representing the number of
    clicks, such as 'double click' and 'triple click'."""

    if count == 2:
        # Translators: Orca keybindings support double
        # and triple "clicks" or key presses, similar to
        # using a mouse.
        #
        return _("double click")
    if count == 3:
        # Translators: Orca keybindings support double
        # and triple "clicks" or key presses, similar to
        # using a mouse.
        #
        return _("triple click")
    return ""

class KeyBinding:
    """A single key binding, consisting of a keycode, a modifier mask,
    and the InputEventHandler.
    """

    def __init__(self, keysymstring, modifier_mask, modifiers, handler,
                 click_count = 1):
        """Creates a new key binding.

        Arguments:
        - keysymstring: the keysymstring - this is typically a string
          from /usr/include/X11/keysymdef.h with the preceding 'XK_'
          removed (e.g., XK_KP_Enter becomes the string 'KP_Enter').
        - modifier_mask: bit mask where a set bit tells us what modifiers
          we care about (see Atspi.ModifierType.*)
        - modifiers: the state the modifiers we care about must be in for
          this key binding to match an input event (see also
          Atspi.ModifierType.*)
        - handler: the InputEventHandler for this key binding
        """

        self.keysymstring = keysymstring
        self.modifier_mask = modifier_mask
        self.modifiers = modifiers
        self.handler = handler
        self.click_count = click_count
        self.keycode = None

    def matches(self, keycode, modifiers):
        """Returns true if this key binding matches the given keycode and
        modifier state.
        """

        # We lazily bind the keycode.  The primary reason for doing this
        # is so that atspi does not have to be initialized before setting
        # keybindings in the user's preferences file.
        #
        if not self.keycode:
            self.keycode = getKeycode(self.keysymstring)

        if self.keycode == keycode:
            result = modifiers & self.modifier_mask
            return result == self.modifiers
        else:
            return False

    def description(self):
        """Returns the description of this binding's functionality."""

        try:
            return self.handler.description
        except Exception:
            return ''

    def asString(self):
        """Returns a more human-consumable string representing this binding."""

        mods = getModifierNames(self.modifiers)
        clickCount = getClickCountString(self.click_count)
        keysym = self.keysymstring
        string = f'{mods}{keysym} {clickCount}'

        return string.strip()

    def keyDefs(self):
        """ return a list of Atspi key definitions for the given binding.
            This may return more than one binding if the Orca modifier is bound
            to more than one key.
            If AT-SPI is older than 2.40, then this function will not work and
            will return an empty set.
        """
        ret = []
        if not self.keycode:
            self.keycode = getKeycode(self.keysymstring)

        if self.modifiers & ORCA_MODIFIER_MASK:
            device = orca_state.device
            if device is None:
                return ret
            modList = []
            otherMods = self.modifiers & ~ORCA_MODIFIER_MASK
            numLockMod = device.get_modifier(getKeycode("Num_Lock"))
            lockedMods = device.get_locked_modifiers()
            numLockOn = lockedMods & numLockMod
            for key in settings.orcaModifierKeys:
                keycode = getKeycode(key)
                if keycode == 0 and key == "Shift_Lock":
                    keycode = getKeycode("Caps_Lock")
                mod = device.map_modifier(keycode)
                if key != "KP_Insert" or not numLockOn:
                    modList.append(mod | otherMods)
        else:
            modList = [self.modifiers]
        for mod in modList:
            kd = Atspi.KeyDefinition()
            kd.keycode = self.keycode
            kd.modifiers = mod
            ret.append(kd)
        return ret

class KeyBindings:
    """Structure that maintains a set of KeyBinding instances.
    """

    def __init__(self):
        self.keyBindings = []

    def __str__(self):
        result = "[\n"
        for keyBinding in self.keyBindings:
            result += "  [%x %x %s %d %s]\n" % \
                      (keyBinding.modifier_mask,
                       keyBinding.modifiers,
                       keyBinding.keysymstring,
                       keyBinding.click_count,
                       keyBinding.handler.description)
        result += "]"
        return result

    def add(self, keyBinding):
        """Adds the given KeyBinding instance to this set of keybindings.
        """

        if keyBinding.keysymstring and self.hasKeyBinding(keyBinding, "keysNoMask"):
           msg = (
               f"WARNING: '{keyBinding.asString()}' "
               f"({keyBinding.description()}) already in keybindings"
           )
           debug.println(debug.LEVEL_INFO, msg, True)

        self.keyBindings.append(keyBinding)

    def remove(self, keyBinding):
        """Removes the given KeyBinding instance from this set of keybindings.
        """

        try:
            i = self.keyBindings.index(keyBinding)
        except Exception:
            pass
        else:
            del self.keyBindings[i]

    def removeByHandler(self, handler):
        """Removes the given KeyBinding instance from this set of keybindings.
        """
        i = len(self.keyBindings)
        while i > 0:
            if self.keyBindings[i - 1].handler == handler:
                del self.keyBindings[i - 1]
            i = i - 1

    def hasKeyBinding (self, newKeyBinding, typeOfSearch="strict"):
        """Return True if keyBinding is already in self.keyBindings.

           The typeOfSearch can be:
              "strict":      matches description, modifiers, key, and
                             click count
              "description": matches only description.
              "keys":        matches the modifiers, key, and modifier mask,
                             and click count
              "keysNoMask":  matches the modifiers, key, and click count
        """

        hasIt = False

        for keyBinding in self.keyBindings:
            if typeOfSearch == "strict":
                if (keyBinding.handler.description \
                    == newKeyBinding.handler.description) \
                    and (keyBinding.keysymstring \
                         == newKeyBinding.keysymstring) \
                    and (keyBinding.modifier_mask \
                         == newKeyBinding.modifier_mask) \
                    and (keyBinding.modifiers \
                         == newKeyBinding.modifiers) \
                    and (keyBinding.click_count \
                         == newKeyBinding.click_count):
                    hasIt = True
            elif typeOfSearch == "description":
                if keyBinding.handler.description \
                    == newKeyBinding.handler.description:
                    hasIt = True
            elif typeOfSearch == "keys":
                if (keyBinding.keysymstring \
                    == newKeyBinding.keysymstring) \
                    and (keyBinding.modifier_mask \
                         == newKeyBinding.modifier_mask) \
                    and (keyBinding.modifiers \
                         == newKeyBinding.modifiers) \
                    and (keyBinding.click_count \
                         == newKeyBinding.click_count):
                    hasIt = True
            elif typeOfSearch == "keysNoMask":
                if (keyBinding.keysymstring \
                    == newKeyBinding.keysymstring) \
                    and (keyBinding.modifiers \
                         == newKeyBinding.modifiers) \
                    and (keyBinding.click_count \
                         == newKeyBinding.click_count):
                    hasIt = True

        return hasIt

    def getBoundBindings(self, uniqueOnly=False):
        """Returns the KeyBinding instances which are bound to a keystroke.

        Arguments:
        - uniqueOnly: Should alternative bindings for the same handler be
          filtered out (default: False)
        """

        bound = [kb for kb in self.keyBindings if kb.keysymstring]
        if uniqueOnly:
            handlers = [kb.handler.description for kb in bound]
            bound = [bound[i] for i in map(handlers.index, set(handlers))]

        bindings = {}
        for kb in bound:
            string = kb.asString()
            match = bindings.get(string)
            if match is not None:
                msg = f"WARNING: '{string}' ({kb.description()}) also matches: {match}"
                debug.println(debug.LEVEL_INFO, msg, True)
            bindings[string] = kb.description()

        return bound

    def getBindingsForHandler(self, handler):
        """Returns the KeyBinding instances associated with handler."""

        return [kb for kb in self.keyBindings if kb.handler == handler]

    def _checkMatchingBindings(self, keyboardEvent, result):
        if debug.debugLevel > debug.LEVEL_INFO:
            return

        # If we don't have multiple matches, we're good.
        if len(result) <= 1:
            return

        # If we have multiple matches, but they have unique click counts, we're good.
        if len(set(map(lambda x: x.click_count, result))) == len(result):
            return

        def toString(x):
            return "%s (%ix)" % (x.handler.description, x.click_count)

        msg = (
            f"WARNING: '{keyboardEvent.event_string}' "
            f"matches multiple handlers: {', '.join(map(toString, result))}"
        )
        debug.println(debug.LEVEL_INFO, msg, True)

    def getInputHandler(self, keyboardEvent):
        """Returns the input handler of the key binding that matches the
        given keycode and modifiers, or None if no match exists.
        """

        matches = []
        candidates = []
        clickCount = keyboardEvent.getClickCount()
        for keyBinding in self.keyBindings:
            if keyBinding.matches(keyboardEvent.hw_code, keyboardEvent.modifiers):
                if keyBinding.modifier_mask == keyboardEvent.modifiers and \
                   keyBinding.click_count == clickCount:
                    matches.append(keyBinding)
                # If there's no keysymstring, it's unbound and cannot be
                # a match.
                #
                if keyBinding.keysymstring:
                    candidates.append(keyBinding)

        self._checkMatchingBindings(keyboardEvent, matches)
        if matches:
            return matches[0].handler

        if keyboardEvent.isKeyPadKeyWithNumlockOn():
            return None

        # If we're still here, we don't have an exact match. Prefer
        # the one whose click count is closest to, but does not exceed,
        # the actual click count.
        #
        candidates.sort(key=functools.cmp_to_key(lambda x, y: y.click_count - x.click_count))
        self._checkMatchingBindings(keyboardEvent, candidates)
        for candidate in candidates:
            if candidate.click_count <= clickCount:
                return candidate.handler

        return None

    def load(self, keymap, handlers):
        """ Takes the keymappings and tries to find a matching named
           function in handlers.
           keymap is a list of lists, each list contains 5 elements
           If addUnbound is set to true, then at the end of loading all the
           keybindings, any remaining functions will be unbound.
        """


        for i in keymap:
            keysymstring = i[0]
            modifierMask = i[1]
            modifiers = i[2]
            handler = i[3]
            try:
                clickCount = i[4]
            except Exception:
                clickCount = 1

            if handler in handlers:
                # add the keybinding
                self.add(KeyBinding( \
                  keysymstring, modifierMask, modifiers, \
                    handlers[handler], clickCount))
            else:
                debug.println(debug.LEVEL_WARNING, \
                  f"WARNING: could not find {handler} handler to associate with keybinding.")
