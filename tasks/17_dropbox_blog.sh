#!/bin/bash

TASK_NAME=$(basename $0)
DEST=$1

die () {
    echo "$TASK_NAME: $2";
    exit $1
}

HOSTNAME=$(hostname)
if [[ $HOSTNAME == "csand-fedora-vm" ]]; then
    SRC="/home/csand/Dropbox/blog"
elif [[ $HOSTNAME == "shiny" ]]; then
    SRC="/home/csand/Dropbox/blog"
elif [[ $HOSTNAME == "obsidian" ]]; then
    SRC="/home/csand/Dropbox/blog"
elif [[ $HOSTNAME == 'fedora-vm' ]]; then
    SRC="/home/csand/storage/Dropbox/blog"
elif [[ $HOSTNAME == 'hackmanite' ]]; then
    SRC="/Users/csand/Dropbox/blog"
else
    echo "AAHHH, DONT KNOW WHAT TO DO WITH HOST `hostname`"
fi

test -z $SRC && die 1 "No source path defined for $HOSTNAME"

echo "$TASK_NAME: copying blog: $SRC $DEST"
rsync -haP --no-whole-file --inplace --exclude template.rst $SRC $DEST
echo "$TASK_NAME: done"
