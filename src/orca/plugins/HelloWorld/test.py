#!/bin/python
# main.py
import gettext
_ = gettext.gettext
def print_some_strings():
    el = gettext.translation('base', localedir='locales')
    #el = gettext.translation('base', localedir='locales', languages=['de'])
    el.install()
    _ = el.gettext # Greek
    print(_("Hello World"))
    print(_("This is a translatable string"))
if __name__=='__main__':
    print_some_strings() 
