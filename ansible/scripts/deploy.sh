#!/bin/bash

set -euxo pipefail

# Portable way to get absolute path, readlink -f doesnt work for mac osx
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd`
popd > /dev/null

PARENTPATH="$(dirname "$SCRIPTPATH")"

echo "Beginning Installation at $(date)."

# Must connect to the VPN for Git packages and DNS resolution
cd $PARENTPATH
vagrant up
echo "Sleep for short time while VM ethernet interfaces are set up..."
sleep 15
echo "Resuming..."
ansible-playbook provision_ipfs.yaml -i inventory.py || true
