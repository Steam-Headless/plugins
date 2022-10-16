#!/usr/bin/env bash

script_path=$(cd "$(dirname "${0}")" && pwd)
project_path=$(dirname $(dirname ${script_path}))

# Set project version
echo "Set project version"
pushd "${project_path}" &>/dev/null || exit
sem_ver=$(build/tools/gitversion/gitversion /showvariable SemVer)
echo "${sem_ver}" >steam_headless_plugins/version.txt
echo "${sem_ver}"
popd &>/dev/null || exit
