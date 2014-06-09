#!/bin/bash

CONTENT_DIR="./content"
TASKS_DIR="./tasks"

usage () {
    echo -e "Usage: $0\n";
    echo -e "Runs any executable in the directory $TASKS_DIR with the pelican";
    echo -e "source directory as the only argument.";
}

if [[ $# -gt 0 ]]; then
    usage;
    exit 1;
fi;

if [[ ! -d $TASKS_DIR ]]; then
    echo "No tasks found...";
    exit 0;
fi;

if [[ ! -d $CONTENT_DIR ]]; then
    echo "No content dir found, nothing to pre-proces...";
    exit 0;
fi;

echo -e "pre-processing..."
for task_f in $(ls $TASKS_DIR); do
    task=$TASKS_DIR/$task_f
    if [[ -x $task ]]; then
        $task $CONTENT_DIR
    fi
done;
