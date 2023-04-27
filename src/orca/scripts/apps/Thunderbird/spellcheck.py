# Orca
#
# Copyright 2014 Igalia, S.L.
#
# Author: Joanmarie Diggs <jdiggs@igalia.com>
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

"""Customized support for spellcheck in Thunderbird."""

__id__ = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2014 Igalia, S.L."
__license__   = "LGPL"

import gi
gi.require_version("Atspi", "2.0")
from gi.repository import Atspi

import pyatspi

import orca.orca_state as orca_state
import orca.spellcheck as spellcheck

class SpellCheck(spellcheck.SpellCheck):

    def __init__(self, script):
        super(SpellCheck, self).__init__(script)

    def isAutoFocusEvent(self, event):
        if event.source != self._changeToEntry:
            return False

        locusOfFocus = orca_state.locusOfFocus
        if not locusOfFocus:
            return False

        role = locusOfFocus.getRole()
        if not role == Atspi.Role.PUSH_BUTTON:
            return False

        lastKey, mods = self._script.utilities.lastKeyAndModifiers()
        keys = self._script.utilities.mnemonicShortcutAccelerator(locusOfFocus)
        for key in keys:
            if key.endswith(lastKey.upper()):
                return True

        return False

    def _isCandidateWindow(self, window):
        if not (window and window.getRole() == Atspi.Role.DIALOG):
            return False

        roles = [Atspi.Role.PAGE_TAB_LIST, Atspi.Role.SPLIT_PANE]
        isNonSpellCheckChild = lambda x: x and x.getRole() in roles
        if pyatspi.findDescendant(window, isNonSpellCheckChild):
            return False

        return True

    def _findChangeToEntry(self, root):
        isEntry = lambda x: x and x.getRole() == Atspi.Role.ENTRY \
                  and x.getState().contains(Atspi.StateType.SINGLE_LINE)
        return pyatspi.findDescendant(root, isEntry)

    def _findErrorWidget(self, root):
        isError = lambda x: x and x.getRole() == Atspi.Role.LABEL \
                  and not ":" in x.name and not x.getRelationSet()
        return pyatspi.findDescendant(root, isError)

    def _findSuggestionsList(self, root):
        isList = lambda x: x and x.getRole() in [Atspi.Role.LIST, Atspi.Role.LIST_BOX] \
                  and 'Selection' in x.get_interfaces()
        return pyatspi.findDescendant(root, isList)

    def _getSuggestionIndexAndPosition(self, suggestion):
        attrs = self._script.utilities.objectAttributes(suggestion)
        index = attrs.get("posinset")
        total = attrs.get("setsize")
        if index is None or total is None:
            return super()._getSuggestionIndexAndPosition(suggestion)

        return int(index), int(total)
