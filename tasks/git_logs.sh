#!/bin/bash

TASK=$(basename $0)
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

echo "$TASK: Writing Git Log Pages..."

if [[ ! -d $DEST ]]; then
    echo "$TASK: mkdir $DEST"
    mkdir -p $DEST
fi

echo "$TASK: writing blog log..."
touch $DEST/blog.rst
write_header "blog" &> $DEST/blog.rst
get_log &>> $DEST/blog.rst

echo "$TASK: writing fret log..."
touch $DEST/fret.rst
write_header "fret" &> $DEST/fret.rst
get_log "./fret" &>> $DEST/fret.rst
