#!/usr/bin/bash
#
#                      __   .__                    .___
# __  _  _____________|  | _|  |   _________     __| _/___________
# \ \/ \/ /  _ \_  __ \  |/ /  |  /  _ \__  \   / __ |/ __ \_  __ \
#  \     (  <_> )  | \/    <|  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
#   \/\_/ \____/|__|  |__|_ \____/\____(____  /\____ |\___  >__|
#                          \/               \/      \/    \/
#
# Copyright (c) 2018 Stephen Shao <sjh311@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

VERSION=1.1.3
#
# Color Definition
TXTRESET='\e[0m'
TXTRED='\e[0;31m'
TXTGREEN='\e[0;32m'
TXTBLUE='\e[0;34m'
TXTPURPLE='\e[0;35m'


BTXTRED='\e[1;31m'
BTXTGREEN='\e[1;32m'
BTXTBLUE='\e[1;34m'


ERROR_CODE=2 # Invalid parameters

usage() {

echo -e "$TXTGREEN
    ############################################

    USAGE: ${0} install|clean]

    ############################################
    $TXTRESET"
}

function display_ascii_logo() {
    echo -e "$TXTPURPLE\n========================================================"
    echo -e "$(cat .workloaderascii)"
    echo -e "========================================================$TXTRESET\n"
}

ACTION=$1

if [ "$ACTION" != "install" -a "$ACTION" != "clean" ]; then
   usage
   exit $ERROR_CODE
fi

# Directories
PROJECT_ROOT_DIR=/opt
WORKLOADER_BIN_DIR=$PROJECT_ROOT_DIR/workloader

WORKLOADER_VER=1.1.3


WORKLOADER_PKG_NAME=workloader-${WORKLOADER_VER}-py2.py3-none-any.whl
WORKLOADER_PKG_PATH=$WORKLOADER_BIN_DIR/$WORKLOADER_PKG_NAME

function inst_workloader() {
   pip install -U $WORKLOADER_PKG_PATH
}


function uninst_workloader() {
   if [ -d /opt/workloader ]; then
      pip uninstall -y workloader
      rm -rf $WORKLOADER_BIN_DIR
   fi
}


function main() {
display_ascii_logo
if [ "$ACTION" == "install" ]; then
   inst_workloader
elif [ "$ACTION" == "clean" ]; then
   uninst_workloader
   exit 0
else
   usage
   exit $ERROR_CODE
fi
cd $PROJECT_ROOT_DIR
}

main