#!/usr/bin/env bash

script_path=$(cd "$(dirname "${0}")" && pwd)
project_path=$(dirname $(dirname ${script_path}))

# Create venv
echo "Setup Python build environment"
pushd "${project_path}" &>/dev/null || exit
# Ensure venv exists. Create it if it does not
if [[ ! -d "${project_path}/venv" ]]; then
    python3 -m venv venv
fi
# Activate the venv
source ./venv/bin/activate
# Upgrade pip prior to installing anything
python3 -m pip install --upgrade pip
# Install Launcher Python dependencies
python3 -m pip install --upgrade -r requirements.txt
popd &>/dev/null || exit
