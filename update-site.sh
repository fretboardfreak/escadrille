#!/bin/bash

usage () {
    echo -e "$0 INTERVAL\n";
    echo "Update the site in a loop.";
}

LOG_FILE="./update_log.txt";

PULL_FAILURE=false;
BUILD_FAILURE=false;
ITERATION=0;
INTERVAL=1800;
ONCE=false;
if [[ $# -eq 1 ]]; then
    if [[ $1 == "-1" ]]; then
        ONCE=true;
    else
        INTERVAL=$1;
    fi
else
    usage;
fi

update_repo () {
    echo pulling new updates...;
    git clean -fd
    git submodule update
    git pull --rebase;
    pull_rc=$?;

    pushd fret;
    git checkout master;
    git pull --rebase;
    fret_rc=$?;
    popd;

    if [[ $pull_rc != 0 ]] || [[ $fret_rc != 0 ]]; then
        echo "git pull failed :( - blog=$pull_rc fret=$fret_rc";
        PULL_FAILURE=true;
    fi;
}

build () {
    echo building and uploading...;
    make rsync_upload;
    build_rc=$?;
    if [[ $build_rc != 0 ]]; then
        echo "build or rsync error :( - rc=$build_rc";
        BUILD_FAILURE=true;
        break;
    fi;
}

start_updates () {
    while ! $PULL_FAILURE && ! $BUILD_FAILURE; do
        ITERATION=$(($ITERATION + 1));
        cat /dev/null > $LOG_FILE;
        sleep 1;

        echo "Starting iteration $ITERATION...";
        date;

        update_repo;
        $PULL_FAILURE && break;

        build;
        $BUILD_FAILURE && break;

        date;

        if [[ $ONCE ]]; then
            echo "Single update complete."
            exit 1;
        fi
        echo "$INTERVAL seconds until next update...";
        sleep $INTERVAL;
    done
}

pushd $(dirname $0) &> /dev/null
start_updates &>> $LOG_FILE
echo "Build failed=$BUILD_FAILURE" &>> $LOG_FILE
echo "Pull failed=$PULL_FAILED" &>> $LOG_FILE
exit 0
