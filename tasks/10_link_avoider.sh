#!/bin/bash

# Copy files to the content directory. Read the data file by line, each line is
# a file to copy. Destination defaults to the content directory but can be
# changed by specifying the new destination with a line like:
#
#     DEST|new/destination
#
# Destinations are always relative to the content directory.

TASK=$(basename $0)
CONTENT_DIR=$1
DATA_FILE="$CONTENT_DIR/../task_data/link_avoider.txt"

echo "$TASK: copying files..."
DEST=$CONTENT_DIR
while read line ; do
    if [[ ${line:0:5} == "DEST|" ]]; then
        DEST=$CONTENT_DIR/${line:5};
        if [[ ! -d $DEST ]]; then
            mkdir $DEST
        fi
        continue;
    elif [[ ${line:0:1} == "#" ]]; then
        continue;
    else # [[ -f $line ]] ; then
        cp -fr $line $DEST
    fi
done < "$DATA_FILE";

echo "$TASK: done"
