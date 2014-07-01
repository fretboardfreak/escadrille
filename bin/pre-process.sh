#!/bin/bash

CONTENT_DIR=$(readlink -f $(dirname $0)/../content)
TASKS_DIR=$(readlink -f $(dirname $0)/../tasks)

usage () {
    echo -e "Usage: $0\n";
    echo -e "Runs any executable in the directory $TASKS_DIR with the pelican";
    echo -e "source directory as the only argument.";
}

if [[ $# -gt 0 ]]; then
    usage;
    exit 1;
fi;

pushd $(dirname $0)/.. # descend from .../bin to the top dir

if [[ ! -d $TASKS_DIR ]]; then
    echo "No tasks found...";
    exit 0;
fi;

if [[ ! -d $CONTENT_DIR ]]; then
    echo "No '$CONTENT_DIR' dir found, making it...";
    mkdir -p $CONTENT_DIR
fi;

echo -e "pre-processing..."
for task_f in $(ls $TASKS_DIR); do
    task=$TASKS_DIR/$task_f
    if [[ -x $task ]]; then
        $task $CONTENT_DIR
    fi
done;
