#!/usr/bin/python

from macaroon.playback import *
import utils

sequence = MacroSequence()

sequence.append(KeyComboAction("<Control>f"))
sequence.append(TypeAction("Popovers"))
sequence.append(KeyComboAction("Escape"))
sequence.append(KeyComboAction("Down"))
sequence.append(KeyComboAction("Down"))
sequence.append(KeyComboAction("<Shift>Right"))
sequence.append(KeyComboAction("Down"))
sequence.append(KeyComboAction("Return"))
sequence.append(KeyComboAction("Tab"))
sequence.append(PauseAction(3000))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("<Shift>ISO_Left_Tab"))
sequence.append(utils.AssertPresentationAction(
    "1. Shift+Tab",
    ["BRAILLE LINE:  'gtk3-demo application Print dialog General page tab'",
     "     VISIBLE:  'General page tab', cursor=1",
     "SPEECH OUTPUT: 'General page tab.'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_8"))
sequence.append(utils.AssertPresentationAction(
    "2. Review current line",
    ["BRAILLE LINE:  'General Page Setup $l'",
     "     VISIBLE:  'General Page Setup $l', cursor=1",
     "SPEECH OUTPUT: 'General Page Setup'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_7"))
sequence.append(utils.AssertPresentationAction(
    "3. Review previous line",
    ["BRAILLE LINE:  'Cancel Preview Print $l'",
     "     VISIBLE:  'Cancel Preview Print $l', cursor=1",
     "SPEECH OUTPUT: 'Cancel Preview Print'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_9"))
sequence.append(utils.AssertPresentationAction(
    "4. Review next line",
    ["BRAILLE LINE:  'General Page Setup $l'",
     "     VISIBLE:  'General Page Setup $l', cursor=1",
     "SPEECH OUTPUT: 'General Page Setup'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_9"))
sequence.append(utils.AssertPresentationAction(
    "5. Review next line",
    ["BRAILLE LINE:  'table column header Printer Location Status $l'",
     "     VISIBLE:  'table column header Printer Loca', cursor=1",
     "SPEECH OUTPUT: 'table column header Printer Location Status'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_9"))
sequence.append(utils.AssertPresentationAction(
    "6. Review next line",
    ["BRAILLE LINE:  'Print to File $l'",
     "     VISIBLE:  'Print to File $l', cursor=1",
     "SPEECH OUTPUT: 'Print to File'"]))

# Skip over personal printer
sequence.append(KeyComboAction("KP_9"))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_9"))
sequence.append(utils.AssertPresentationAction(
    "7. Review next line",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'File: ~/Documents/gtk-demo.pdf O', cursor=1",
     "SPEECH OUTPUT: 'File: ~/Documents/gtk-demo.pdf Output format: selected PDF not selected Postscript not selected SVG'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "8. Review next word",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'File: ~/Documents/gtk-demo.pdf O', cursor=7",
     "SPEECH OUTPUT: '~/Documents/gtk-demo.pdf'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "9. Review next word",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'File: ~/Documents/gtk-demo.pdf O', cursor=32",
     "SPEECH OUTPUT: 'Output'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_3"))
sequence.append(utils.AssertPresentationAction(
    "10. Review next char",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'utput format: &=y PDF & y Postsc', cursor=1",
     "SPEECH OUTPUT: 'u'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_3"))
sequence.append(utils.AssertPresentationAction(
    "11. Review next char",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'utput format: &=y PDF & y Postsc', cursor=2",
     "SPEECH OUTPUT: 't'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_3"))
sequence.append(utils.AssertPresentationAction(
    "12. Review next char",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'utput format: &=y PDF & y Postsc', cursor=3",
     "SPEECH OUTPUT: 'p'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_3"))
sequence.append(utils.AssertPresentationAction(
    "13. Review next char",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'utput format: &=y PDF & y Postsc', cursor=4",
     "SPEECH OUTPUT: 'u'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_3"))
sequence.append(utils.AssertPresentationAction(
    "14. Review next char",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'utput format: &=y PDF & y Postsc', cursor=5",
     "SPEECH OUTPUT: 't'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_3"))
sequence.append(utils.AssertPresentationAction(
    "15. Review next char",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'utput format: &=y PDF & y Postsc', cursor=6",
     "SPEECH OUTPUT: 'space'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_3"))
sequence.append(utils.AssertPresentationAction(
    "16. Review next char",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'utput format: &=y PDF & y Postsc', cursor=7",
     "SPEECH OUTPUT: 'f'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_1"))
sequence.append(utils.AssertPresentationAction(
    "17. Review previous char",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'utput format: &=y PDF & y Postsc', cursor=6",
     "SPEECH OUTPUT: 'space'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_1"))
sequence.append(utils.AssertPresentationAction(
    "18. Review previous char",
    ["BRAILLE LINE:  'File: ~/Documents/gtk-demo.pdf Output format: &=y PDF & y Postscript & y SVG $l'",
     "     VISIBLE:  'utput format: &=y PDF & y Postsc', cursor=5",
     "SPEECH OUTPUT: 't'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_9"))
sequence.append(utils.AssertPresentationAction(
    "19. Review next line",
    ["BRAILLE LINE:  'Range Copies $l'",
     "     VISIBLE:  'Range Copies $l', cursor=1",
     "SPEECH OUTPUT: 'Range Copies'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_9"))
sequence.append(utils.AssertPresentationAction(
    "20. Review next line",
    ["KNOWN ISSUE: The value is not reviewable",
     "BRAILLE LINE:  '&=y All Pages Copies: spin button $l'",
     "     VISIBLE:  '&=y All Pages Copies: spin butto', cursor=1",
     "SPEECH OUTPUT: 'selected All Pages Copies: spin button'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_5"))
sequence.append(utils.AssertPresentationAction(
    "21. Review current word",
    ["BRAILLE LINE:  '&=y All Pages Copies: spin button $l'",
     "     VISIBLE:  '&=y All Pages Copies: spin butto', cursor=1",
     "SPEECH OUTPUT: 'selected'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_2"))
sequence.append(utils.AssertPresentationAction(
    "22. Review current char",
    ["BRAILLE LINE:  '&=y All Pages Copies: spin button $l'",
     "     VISIBLE:  '&=y All Pages Copies: spin butto', cursor=1",
     "SPEECH OUTPUT: 'selected'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "23. Review next word",
    ["BRAILLE LINE:  '&=y All Pages Copies: spin button $l'",
     "     VISIBLE:  '&=y All Pages Copies: spin butto', cursor=5",
     "SPEECH OUTPUT: 'All Pages'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "24. Review next word",
    ["BRAILLE LINE:  '&=y All Pages Copies: spin button $l'",
     "     VISIBLE:  '&=y All Pages Copies: spin butto', cursor=15",
     "SPEECH OUTPUT: 'Copies:'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_3"))
sequence.append(utils.AssertPresentationAction(
    "25. Review next char",
    ["BRAILLE LINE:  '&=y All Pages Copies: spin button $l'",
     "     VISIBLE:  '&=y All Pages Copies: spin butto', cursor=16",
     "SPEECH OUTPUT: 'o'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "26. Review next word",
    ["BRAILLE LINE:  '&=y All Pages Copies: spin button $l'",
     "     VISIBLE:  '&=y All Pages Copies: spin butto', cursor=23",
     "SPEECH OUTPUT: 'spin button'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_9"))
sequence.append(utils.AssertPresentationAction(
    "27. Review next line",
    ["BRAILLE LINE:  '& y Current Page $l'",
     "     VISIBLE:  '& y Current Page $l', cursor=1",
     "SPEECH OUTPUT: 'not selected Current Page'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_5"))
sequence.append(utils.AssertPresentationAction(
    "28. Review current word",
    ["BRAILLE LINE:  '& y Current Page $l'",
     "     VISIBLE:  '& y Current Page $l', cursor=1",
     "SPEECH OUTPUT: 'not selected'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "29. Review next word",
    ["KNOWN ISSUE: These labels don't implement the text interface so it's a single word",
     "BRAILLE LINE:  '& y Current Page $l'",
     "     VISIBLE:  '& y Current Page $l', cursor=5",
     "SPEECH OUTPUT: 'Current Page'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "30. Review next word",
    ["BRAILLE LINE:  'drawing area $l'",
     "     VISIBLE:  'drawing area $l', cursor=1",
     "SPEECH OUTPUT: 'drawing area'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "31. Review next word",
    ["BRAILLE LINE:  '<x> Collate $l'",
     "     VISIBLE:  '<x> Collate $l', cursor=1",
     "SPEECH OUTPUT: 'checked'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "32. Review next word",
    ["BRAILLE LINE:  '<x> Collate $l'",
     "     VISIBLE:  '<x> Collate $l', cursor=5",
     "SPEECH OUTPUT: 'Collate'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_6"))
sequence.append(utils.AssertPresentationAction(
    "33. Review next word",
    ["BRAILLE LINE:  '& y Pages:  < > Reverse $l'",
     "     VISIBLE:  '& y Pages:  < > Reverse $l', cursor=1",
     "SPEECH OUTPUT: 'not selected'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("KP_9"))
sequence.append(utils.AssertPresentationAction(
    "34. Review next line",
    [""]))

sequence.append(utils.AssertionSummaryAction())
sequence.start()
