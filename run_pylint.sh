#!/bin/bash
#
# Script to run pylint on the Orca sources you've modified or added.
# See http://live.gnome.org/Orca/Pylint for more info.
#
exec_prefix=/usr
INSTALL_DIR=${PYTHON_EXEC_PREFIX}/lib/python3.11/site-packages
if [ "x$*" == "x" ]
then
    if [ -d .git ]
    then
        FILES=`git status | egrep 'modified:|new file:' | grep '[.]py$' | awk '{ print $NF }'`
    else
        FILES=`svn stat src/orca | egrep '^M|^A' | grep '[.]py$' | awk '{ print $NF }'`
    fi
else
    FILES="$*"
fi
FILES=`echo $FILES | sed 's^src/orca/^^g'`
echo Thank you for your attention to quality
for foo in $FILES
do
    echo
    OUTPUT_FILE=`dirname $foo`/`basename $foo .py`.pylint
    OUTPUT_FILE=`echo $OUTPUT_FILE | sed 's~^./~~' | sed 's^/^.^g'`
    echo Checking $foo, sending output to $OUTPUT_FILE
    PYTHONPATH=$INSTALL_DIR:$PYTHONPATH pylint --init-hook="import pyatspi" $INSTALL_DIR/orca/$foo > $OUTPUT_FILE 2>&1
    grep "code has been rated" $OUTPUT_FILE | cut -f1 -d\( \
    | sed "s/.pylint:Your code has been rated at / /" \
    | sed "s^/10^^" | sort -n -k 2,2
done
