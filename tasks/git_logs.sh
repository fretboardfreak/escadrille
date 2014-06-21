#!/bin/bash

TASK=$(basename $0)
DEST=$1/pages
REPOS="blog fret"

get_header () {
    echo -e "$1 log\n=================\n\n"
    echo ":date: $(date +"%Y-%m-%d %H:%M")"
    echo ":summary: A log of activity in repository $1."
    echo -e "\n----\n\n.. raw:: html\n\n    <pre>\n"
}

get_log () {
    if [[ ! -z $1 ]]; then
        pushd $1 &>/dev/null;
    fi
    # replace @ to make email address scraping harder
    git log | sed -e 's/@/<AT>/g'
    if [[ ! -z $1 ]]; then
        popd &>/dev/null;
    fi
}

get_footer () {
    echo -e "\n.. raw:: html\n\n    </pre>\n\n[End of log]"
}

write_log_page () {
    local repo=$1
    local file=$DEST/$repo.rst
    echo "$TASK: writing $repo log..."
    touch $file
    get_header "$repo" &> $file
    get_log &>> $file
    get_footer &>> $file
}


echo "$TASK: Writing Git Log Pages..."

if [[ ! -d $DEST ]]; then
    echo "$TASK: mkdir $DEST";
    mkdir -p $DEST;
fi

for repo in $REPOS; do
    write_log_page $repo;
done

echo "$TASK: done"
