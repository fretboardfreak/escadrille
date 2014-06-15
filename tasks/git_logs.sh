#!/bin/bash

DEST=$1/pages

write_header () {
    echo "========"
    echo "$1 log"
    echo "========"
    echo ""
    echo ":date: $(date +"%Y-%m-%d %H:%M")"
    echo ":summary: A log of activity in repository $1."
    echo -e "\n----\n"
}

get_log () {
    if [[ ! -z $1 ]]; then
        pushd $1 &>/dev/null;
    fi
    git log
    if [[ ! -z $1 ]]; then
        popd &>/dev/null;
    fi
}

write_header "blog" &> $DEST/blog.rst
get_log &>> $DEST/blog.rst

write_header "fret" &> $DEST/fret.rst
get_log "./fret" &>> $DEST/fret.rst
