#!/usr/bin/env bash

set -e

gow_log "**** Configure devices ****"

# make sure we're in the right groups to use all the required devices
# we're actually relying on word splitting for this call, so disable the
# warning from shellcheck
# shellcheck disable=SC2086
gow_log "Exec device groups"
/opt/gow/ensure-groups ${GOW_REQUIRED_DEVICES:-/dev/uinput /dev/input/event*}

gow_log "DONE"
