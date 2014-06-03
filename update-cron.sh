#!/bin/bash

# pull new updates
git pull --rebase &>/dev/null

[[ $? -eq 0 ]] || exit;

# build and upload site using Makefile
make rsync_upload &>/dev/null
