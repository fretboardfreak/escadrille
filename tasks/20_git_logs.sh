#!/bin/bash

TASK=$(basename $0)
DEST=$1/pages
REPOS="blog fret fretsmusic"

get_header () {
    (echo -e "$1 log\n=================\n\n"
    echo ":date: $(date +"%Y-%m-%d %H:%M")"
    echo ":summary: A log of activity in repository $1."
    echo -e "\n----\n\n.. raw:: html\n\n    <pre>\n") > $2
}

get_log () {
    if [[ ! -z $1 ]]; then
        echo "$TASK: changing dirs to $1..."
        pushd $1 &>/dev/null;
    fi
    # replace @ to make email address scraping harder
    local data=$(git log | sed -e 's/@/<AT>/g' -e 's/*/\\*/g')
    if [[ ! -z $1 ]]; then
        echo -n "$TASK: changing back to "
        popd
    fi
    echo $data 2>&1 >> $2
}

get_footer () {
    echo -e "\n.. raw:: html\n\n    </pre>\n\n[End of log]" >> $1
}

write_log_page () {
    local repo="$1"
    local file="$DEST/$repo.rst"
    local dir="$1"
    if [[ "$dir" == "blog" ]]; then
        dir=".";
    else
        dir="${HOME}/$dir"
    fi
    echo "$TASK: writing $repo log..."
    touch $file && sync
    get_header $repo $file
    get_log $dir $file
    get_footer $file
}


echo "$TASK: Writing Git Log Pages..."

if [[ ! -d $DEST ]]; then
    echo "$TASK: mkdir $DEST";
    mkdir -p $DEST;
fi

for rp in $REPOS; do
    write_log_page $rp;
done

echo "$TASK: done"
