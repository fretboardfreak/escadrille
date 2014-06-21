#!/bin/bash

TASK_NAME=$(basename $0)
DEST=$1

die () {
    echo "$TASK_NAME: $2";
    exit $1
}

if [[ $HOSTNAME -eq "crunchbang-vm" ]]; then
    SRC="/home/csand/storage/Dropbox/images"
elif [[ $HOSTNAME -eq "shiny" ]]; then
    SRC="/home/csand/Dropbox/images"
fi

test -z $SRC && die 1 "No source path defined for $HOSTNAME"

echo "$TASK_NAME: copying images: $SRC $DEST"
rsync -haP --no-whole-file --inplace $SRC $DEST
echo "$TASK_NAME: done"
