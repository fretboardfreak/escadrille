#!/bin/bash

update () {
    date

    echo pulling new updates...
    git pull --rebase
    git submodule update

    if [[ $? -ne 0 ]] ; then
        echo "git pull failed :("
        exit;
    fi


    echo building and uploading...
    make rsync_upload
    rc=$?

    date
    return $rc
}

echo entering repository...
pushd $(dirname $0)

while true; do
    update
    echo "returncode: $?";
    echo "1800 seconds until next update...";
    sleep 1800;
done
