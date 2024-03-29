# Orca
#
# Copyright 2005-2008 Sun Microsystems Inc.
# Copyright 2013 Igalia, S.L.
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

"""Custom script for Evolution."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc." \
                "Copyright (c) 2013 Igalia, S.L."
__license__   = "LGPL"


import orca.debug as debug
import orca.orca as orca
import orca.orca_state as orca_state
import orca.scripts.toolkits.gtk as gtk
import orca.scripts.toolkits.WebKitGtk as WebKitGtk
import orca.settings_manager as settings_manager
from orca.ax_object import AXObject
from orca.ax_utilities import AXUtilities

from .braille_generator import BrailleGenerator
from .speech_generator import SpeechGenerator
from .script_utilities import Utilities

_settingsManager = settings_manager.getManager()

########################################################################
#                                                                      #
# The Evolution script class.                                          #
#                                                                      #
########################################################################

class Script(WebKitGtk.Script, gtk.Script):

    def __init__(self, app):
        """Creates a new script for the given application.

        Arguments:
        - app: the application to create a script for.
        """

        if _settingsManager.getSetting('sayAllOnLoad') is None:
            _settingsManager.setSetting('sayAllOnLoad', False)

        super().__init__(app)
        self.presentIfInactive = False

    def getBrailleGenerator(self):
        return BrailleGenerator(self)

    def getSpeechGenerator(self):
        return SpeechGenerator(self)

    def getUtilities(self):
        return Utilities(self)

    def isActivatableEvent(self, event):
        """Returns True if the given event is one that should cause this
        script to become the active script.  This is only a hint to
        the focus tracking manager and it is not guaranteed this
        request will be honored.  Note that by the time the focus
        tracking manager calls this method, it thinks the script
        should become active.  This is an opportunity for the script
        to say it shouldn't.
        """

        if event.type.startswith("focus:") and AXUtilities.is_menu(event.source):
            return True

        window = self.utilities.topLevelObject(event.source)
        if not AXUtilities.is_active(window):
            return False

        return True

    def stopSpeechOnActiveDescendantChanged(self, event):
        """Whether or not speech should be stopped prior to setting the
        locusOfFocus in onActiveDescendantChanged.

        Arguments:
        - event: the Event

        Returns True if speech should be stopped; False otherwise.
        """

        return False

    ########################################################################
    #                                                                      #
    # AT-SPI OBJECT EVENT HANDLERS                                         #
    #                                                                      #
    ########################################################################

    def onActiveDescendantChanged(self, event):
        """Callback for object:active-descendant-changed accessibility events."""

        if not event.any_data:
            msg = "EVOLUTION: Ignoring event. No any_data."
            debug.println(debug.LEVEL_INFO, msg, True)
            return

        if self.utilities.isComposeAutocomplete(event.source):
            if AXUtilities.is_selected(event.any_data):
                msg = "EVOLUTION: Source is compose autocomplete with selected child."
                debug.println(debug.LEVEL_INFO, msg, True)
                orca.setLocusOfFocus(event, event.any_data)
            else:
                msg = "EVOLUTION: Source is compose autocomplete without selected child."
                debug.println(debug.LEVEL_INFO, msg, True)
                orca.setLocusOfFocus(event, event.source)
            return

        if AXUtilities.is_table_cell(orca_state.locusOfFocus):
            table = AXObject.find_ancestor(
                orca_state.locusOfFocus, AXUtilities.is_tree_or_tree_table)
            if table is not None and table != event.source:
                msg = "EVOLUTION: Event is from a different tree or tree table."
                debug.println(debug.LEVEL_INFO, msg, True)
                return

        child = AXObject.get_active_descendant_checked(event.source, event.any_data)
        if child is not None and child != event.any_data:
            msg = f"EVOLUTION: Bogus any_data suspected. Setting focus to {child}"
            debug.println(debug.LEVEL_INFO, msg, True)
            orca.setLocusOfFocus(event, child)
            return

        msg = "EVOLUTION: Passing event to super class for processing."
        debug.println(debug.LEVEL_INFO, msg, True)
        super().onActiveDescendantChanged(event)

    def onBusyChanged(self, event):
        """Callback for object:state-changed:busy accessibility events."""
        pass

    def onFocus(self, event):
        """Callback for focus: accessibility events."""

        if self.utilities.isWebKitGtk(event.source):
            return

        # This is some mystery child of the 'Messages' panel which fails to show
        # up in the hierarchy or emit object:state-changed:focused events.
        if AXUtilities.is_layered_pane(event.source):
            obj = self.utilities.realActiveDescendant(event.source)
            orca.setLocusOfFocus(event, obj)
            return

        gtk.Script.onFocus(self, event)

    def onNameChanged(self, event):
        """Callback for object:property-change:accessible-name events."""

        if self.utilities.isWebKitGtk(event.source):
            return

        gtk.Script.onNameChanged(self, event)

    def onSelectionChanged(self, event):
        """Callback for object:selection-changed accessibility events."""

        if AXUtilities.is_combo_box(event.source) \
           and not AXUtilities.is_focused(event.source):
            return

        gtk.Script.onSelectionChanged(self, event)
