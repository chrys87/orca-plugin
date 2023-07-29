from orca import plugin

import gi
gi.require_version('Peas', '1.0')
from gi.repository import GObject
from gi.repository import Peas
from threading import Thread, Lock
import subprocess, time, re, os

class CapsLockHack(GObject.Object, Peas.Activatable, plugin.Plugin):
    __gtype_name__ = 'CapsLockHack'

    object = GObject.Property(type=GObject.Object)
    def __init__(self):
        plugin.Plugin.__init__(self)
        self.lock = Lock()
        self.active = False
        self.workerThread = Thread(target=self.worker)
    def do_activate(self):
        API = self.object
        """Enable or disable use of the caps lock key as an Orca modifier key."""
        self.interpretCapsLineProg = re.compile(
            r'^\s*interpret\s+Caps[_+]Lock[_+]AnyOfOrNone\s*\(all\)\s*{\s*$', re.I)
        self.normalCapsLineProg = re.compile(
            r'^\s*action\s*=\s*LockMods\s*\(\s*modifiers\s*=\s*Lock\s*\)\s*;\s*$', re.I)
        self.interpretShiftLineProg = re.compile(
            r'^\s*interpret\s+Shift[_+]Lock[_+]AnyOf\s*\(\s*Shift\s*\+\s*Lock\s*\)\s*{\s*$', re.I)
        self.normalShiftLineProg = re.compile(
            r'^\s*action\s*=\s*LockMods\s*\(\s*modifiers\s*=\s*Shift\s*\)\s*;\s*$', re.I)
        self.disabledModLineProg = re.compile(
            r'^\s*action\s*=\s*NoAction\s*\(\s*\)\s*;\s*$', re.I)
        self.normalCapsLine = '        action= LockMods(modifiers=Lock);'
        self.normalShiftLine = '        action= LockMods(modifiers=Shift);'
        self.disabledModLine = '        action= NoAction();'
        self.activateWorker()
    def do_deactivate(self):
        API = self.object
        self.deactivateWorker()
    def do_update_state(self):
        API = self.object
    def deactivateWorker(self):
        with self.lock:
            self.active = False
        self.workerThread.join()
    def activateWorker(self):
        with self.lock:
            self.active = True
        self.workerThread.start()
    def isActive(self):
        with self.lock:
            return self.active
    def worker(self):
        """Makes an Orca-specific Xmodmap so that the keys behave as we
        need them to do. This is especially the case for the Orca modifier.
        """
        API = self.object
        capsLockCleared = False
        settings = API.app.getDynamicApiManager().getAPI('Settings')
        time.sleep(1)
        while self.isActive():
            #time.sleep(0.5)
            print('drin')
            continue
            start = time.time()
            if "Caps_Lock" in settings.orcaModifierKeys \
              or "Shift_Lock" in settings.orcaModifierKeys:
                self.setCapsLockAsOrcaModifier(True)
                capsLockCleared = True
            elif capsLockCleared:
                self.setCapsLockAsOrcaModifier(False)
                capsLockCleared = False
            print(time.time() - start)


    def setCapsLockAsOrcaModifier(self, enable):
        originalXmodmap = None
        lines = None
        try:
            originalXmodmap = subprocess.check_output(['xkbcomp', os.environ['DISPLAY'], '-'])
            lines = originalXmodmap.decode('UTF-8').split('\n')
        except:
            return
        foundCapsInterpretSection = False
        foundShiftInterpretSection = False
        modified = False
        for i, line in enumerate(lines):
            if not foundCapsInterpretSection and not foundShiftInterpretSection:
                if self.interpretCapsLineProg.match(line):
                    foundCapsInterpretSection = True
                elif self.interpretShiftLineProg.match(line):
                    foundShiftInterpretSection = True
            elif foundCapsInterpretSection:
                if enable:
                    if self.normalCapsLineProg.match(line):
                        lines[i] = self.disabledModLine
                        modified = True
                else:
                    if self.disabledModLineProg.match(line):
                        lines[i] = self.normalCapsLine
                        modified = True
                if line.find('}'):
                    foundCapsInterpretSection = False
            else: # foundShiftInterpretSection
                if enable:
                    if self.normalShiftLineProg.match(line):
                        lines[i] = self.disabledModLine
                        modified = True
                else:
                    if self.disabledModLineProg.match(line):
                        lines[i] = self.normalShiftLine
                        modified = True
                if line.find('}'):
                    foundShiftInterpretSection = False
        if modified:
            newXmodMap = bytes('\n'.join(lines), 'UTF-8')
            self.setXmodmap(newXmodMap)
    def setXmodmap(self, xkbmap):
        """Set the keyboard map using xkbcomp."""
        try:
            p = subprocess.Popen(['xkbcomp', '-w0', '-', os.environ['DISPLAY']],
                stdin=subprocess.PIPE, stdout=None, stderr=None)
            p.communicate(xkbmap)
        except:
            pass
