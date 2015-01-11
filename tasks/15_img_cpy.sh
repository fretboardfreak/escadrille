#!/bin/bash

TASK_NAME=$(basename $0)
DEST=$1

die () {
    echo "$TASK_NAME: $2";
    exit $1
}

HOSTNAME=$(hostname)
if [[ $HOSTNAME == "csand-fedora-vm" ]]; then
    SRC="/home/csand/Dropbox/images"
elif [[ $HOSTNAME == "shiny" ]]; then
    SRC="/home/csand/Dropbox/images"
elif [[ $HOSTNAME == "obsidian" ]]; then
    SRC="/home/csand/Dropbox/images"
else
    echo "AAHHH, DONT KNOW WHAT TO DO WITH HOST `hostname`"
fi

test -z $SRC && die 1 "No source path defined for $HOSTNAME"

echo "$TASK_NAME: copying images: $SRC $DEST"
rsync -haP --no-whole-file --inplace $SRC $DEST
echo "$TASK_NAME: done"
