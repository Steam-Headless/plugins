#!/usr/bin/env bash

script_path=$(cd "$(dirname "${0}")" && pwd)
project_path=$(dirname $(dirname ${script_path}))


# Ensure the dependencies directory exists
if [[ ! -d "${project_path}/build/dependencies" ]]; then
    mkdir -p "${project_path}/build/dependencies"
    echo "Dependencies directory created successfully"
fi


# Create venv
echo "Setup appimage Python build environment"
pushd "${project_path}/build" &>/dev/null || exit
# Ensure venv exists. Create it if it does not
if [[ ! -d "./venv" ]]; then
    python3 -m venv venv
fi
# Activate the venv
source ./venv/bin/activate
# Upgrade pip prior to installing anything
python3 -m pip install --upgrade pip
# Install Launcher Python dependencies
python3 -m pip install --upgrade -r ../requirements.txt
# Install appimage python dev dependencies
python3 -m pip install --upgrade python_appimage==1.0.2
popd &>/dev/null || exit


# Create wheels for all Launcher dependencies
echo "Create wheels for all Launcher dependencies"
pushd "${project_path}" &>/dev/null || exit
if [[ -d "${project_path}/build/dependencies/wheels" ]]; then
    rm -rfv "${project_path}/build/dependencies/wheels"
fi
python3 -m pip wheel --wheel-dir build/dependencies/wheels -r requirements.txt
popd &>/dev/null || exit


# Prepare project
echo "Prepare project"
pushd "${project_path}" &>/dev/null || exit
# Clone build environment
rm -rf build/appimage
cp -rf targets/appimage build/
# Add main project dependencies to requirements
cat requirements.txt >>build/appimage/requirements.txt
# Create a wheel from the launcher
python3 -m pip wheel --no-verify -w ${project_path}/build/dependencies/wheels .
# Add wheel to requirements
echo "${project_path}/build/dependencies/wheels/$(ls -a build/dependencies/wheels | grep steam_headless_plugins)" >>build/appimage/requirements.txt
popd &>/dev/null || exit

# Pack project
sem_ver=$(cat "${project_path}/build/lib/steam_headless_plugins/version.txt")
echo "Pack project v${sem_ver}"
pushd "${project_path}/build" &>/dev/null || exit
python3 -m python_appimage build app -p 3.8 appimage/
popd &>/dev/null || exit
