#!/bin/python
"""UI Manager to handle basic GUI stuff"""

class UiManager():
    def __init__(self, app):
        self.app = app
    def requestPreferences(self):
        self.app.emitSignal('request-orca-preferences');
    def requestAppPreferences(self):
        self.app.emitSignal('request-application-preferences');
