#!/bin/bash

date

echo entering repository...
pushd $(dirname $0)

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

echo exiting...

date

exit $rc
