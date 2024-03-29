# Orca v46.alpha

## Important information about keyboard-related regressions

TL;DR: You should use the gnome-45 branch. It is the branch in which
development related to Orca v45 is taking place.

Orca's `master` branch contains work-in-progress development to use new
key handling support. There are currently a number of regressions that
make this branch unsuitable for regular use. In order to facilitate
work continuing in this area, without disrupting Orca users who want
to try the development version of Orca, we have already branched for
the GNOME 45 release. The `gnome-45` branch is being actively developed
and lacks the new key handling support. Thus it is suitable for end-user
testing. Apologies for this temporary inconvenience.

## Introduction

Orca is a free, open source, flexible, and extensible screen reader
that provides access to the graphical desktop via user-customizable
combinations of speech and/or braille.

Orca works with applications and toolkits that support the assistive
technology service provider interface (AT-SPI), which is the primary
assistive technology infrastructure for the Solaris and Linux
operating environments.  Applications and toolkits supporting the
AT-SPI include the GNOME GTK+ toolkit, the Java platform's Swing
toolkit, OpenOffice/LibreOffice, Gecko, and WebKitGtk.  AT-SPI support
for the KDE Qt toolkit is currently being pursued.

See also <http://wiki.gnome.org/Projects/Orca> for detailed information
on Orca, including how to run Orca, how to communicate with the Orca user
community, and where to log bugs and feature requests.

## Dependencies

Orca v46.x is supported on GNOME 46.x only.  We highly suggest you
use the latest releases of GNOME because they contain accessibility
infrastructure and application bug fixes that help Orca work better.

Orca also has the following dependencies:

* Python 3         - Python platform
* pygobject-3.0    - Python bindings for the GObject library
* gtk+-3.0         - GTK+ toolkit
* libpeas          - GObject based Plugin engine
* json-py          - a JSON (<https://json.org/>) reader and writer in Python
* python-speechd   - Python bindings for Speech Dispatcher (optional)
* BrlTTY           - BrlTTY (<https://mielke.cc/brltty/>) support for braille (optional)
* BrlAPI           - BrlAPI support for braille (optional)
* liblouis         - Liblouis (<http://liblouis.org/>) support for contracted braille (optional)
* py-setproctitle  - Python library to set the process title (optional)
* gstreamer-1.0    - GStreamer - Streaming media framework (optional)
You are strongly encouraged to also have the latest stable versions
of AT-SPI2 and ATK for the GNOME 46.x release.


## NOTE FOR BRLTTY USERS:

Orca depends upon the Python bindings for BrlAPI available in BrlTTY v4.5
or better.  You can determine if the Python bindings for BrlAPI are
installed by running the following command:

```sh
python -c "import brlapi"
```

If you get an error, the Python bindings for BrlAPI are not installed.

## Running Orca

If you wish to modify your Orca preferences, you can press "Insert+space"
while Orca is running.

To get help while running Orca, press "Insert+H".  This will enable
"learn mode", which provides a spoken and brailled description of what
various keyboard and braille input device actions will do.  To exit
learn mode, press "Escape."  Finally, the preferences dialog contains
a "Key Bindings" tab that lists the keyboard binding for Orca.

For more information, see the Orca documentation which is available
within Orca as well as at: <https://help.gnome.org/users/orca/stable/>

## Scripting Orca

So, you want to write a script for Orca?  The best thing to do is 
start by looking at other scripts under the src/orca/scripts/ hierarchy
of the source tree.
