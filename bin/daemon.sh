#!/bin/bash

rc=0
SCRIPT="$(dirname $(readlink -f $0))/update-site.sh"
DAEMON_NAME="updatesite"

usage () {
    echo -e "Usage:> $0 [status|start|stop|restart]";
    echo -e "\nManage the $DAEMON_NAME daemon.";
}

_exit () {
    case $rc in
        (0) echo -e "success";;
        (1) echo -e "failure";;
        (*) echo -e "unknown $rc";;
    esac
    exit $rc;
}

status () {
    echo -en "Checking $DAEMON_NAME daemon...    "
    daemon -n $DAEMON_NAME --running
    rc=$?;
}

start () {
    echo -en "Starting $DAEMON_NAME daemon...    "
    daemon -n $DAEMON_NAME $SCRIPT
    rc=$?;
}

stop () {
    echo -en "Stopping $DAEMON_NAME daemon...    "
    daemon -n $DAEMON_NAME --stop
    rc=$?;
}

restart () {
    if [[ status -eq 0 ]]; then
        stop;
    fi
    start;
}

if [[ $# -eq 0 ]]; then
    status;
elif [[ $# -eq 1 ]]; then
    case $1 in
        (status) status;;
        (start) start;;
        (stop) stop;;
        (restart) restart;;
        (*) usage;;
    esac;
else
    rc=1;
    echo "$0 only accepts a single argument."
fi
_exit;
