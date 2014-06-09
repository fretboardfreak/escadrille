#!/bin/bash

# remove *pyc files
find . -iname "*pyc" -delete

# clean up files from link_avoider task
la_data="task_data/link_avoider.txt"
for dest in $(grep "^DEST" $la_data); do
    for f in $(grep -v "^DEST" $la_data); do
        rm -f ./content/${dest:5}/$(basename $f);
    done;
done
