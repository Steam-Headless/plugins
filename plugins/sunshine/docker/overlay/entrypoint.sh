#!/usr/bin/env bash
###
# File: entrypoint.sh
# Project: overlay
# File Created: Sunday, 9th October 2022 1:35:46 am
# Author: Josh.5 (jsunnex@gmail.com)
# -----
# Last Modified: Sunday, 9th October 2022 3:05:31 am
# Modified By: Josh.5 (jsunnex@gmail.com)
###
set -e 

# If a command was passed, run that instead of the usual init process
if [ ! -z "$@" ]; then
    exec $@
    exit $?
fi

# Print the current version (if the file exists)
if [[ -f /version.txt ]]; then
    cat /version.txt
fi

# Wait for X server to start
#   (Credit: https://gist.github.com/tullmann/476cc71169295d5c3fe6)
wait_for_x() {
    MAX=60 # About 30 seconds
    CT=0
    while ! runuser -u default -- xdpyinfo >/dev/null 2>&1; do
        sleep 0.50s
        CT=$(( CT + 1 ))
        if [ "$CT" -ge "$MAX" ]; then
            echo "FATAL: $0: Gave up waiting for X server $DISPLAY"
            exit 11
        fi
    done
}


# Configure the default user
PUID=${PUID:-99}
PGID=${PGID:-100}
UMASK=${UMASK:-000}
echo "Setting default user uid=${PUID}(${USER}) gid=${PGID}(${USER})"
usermod -o -u "${PUID}" ${USER}
groupmod -o -g "${PGID}" ${USER}
echo "Setting umask to ${UMASK}";
umask ${UMASK}


# Ensure the container default user has access to the required devices
echo "Adding default user to any additional required device groups"
device_nodes=( /dev/uinput /dev/input/event* /dev/dri/* )
added_groups=""
for dev in "${device_nodes[@]}"; do
    # Only process $dev if it's a character device
    if [[ ! -c "${dev}" ]]; then
        continue
    fi

    # Get group name and ID
    dev_group=$(stat -c "%G" "${dev}")
    dev_gid=$(stat -c "%g" "${dev}")

    # Dont add root
    if [[ "${dev_gid}" = 0 ]]; then
        continue
    fi

    # Create a name for the group ID if it does not yet already exist
    if [[ "${dev_group}" = "UNKNOWN" ]]; then
        dev_group="user-gid-${dev_gid}"
        groupadd -g $dev_gid "${dev_group}"
    fi

    # Add group to user
    if [[ "${added_groups}" != *"${dev_group}"* ]]; then
        echo "Adding user '${USER}' to group: '${dev_group}' for device: ${dev}"
        usermod -a -G ${dev_group} ${USER}
        added_groups=" ${added_groups} ${dev_group} "
    fi
done
# Ensure uinput is able to be read/write by everyone
if [ -e /dev/uinput ]; then
    echo "Allow /dev/uinput r/w to the group"
    chmod 0666 /dev/uinput
fi

# Configure Sunshine for the first time
mkdir -p /home/${USER}/sunshine
if [[ ! -f /home/${USER}/sunshine/sunshine.conf ]]; then
    cp -vf /templates/sunshine.conf /home/${USER}/sunshine/
    cp -vf /templates/apps.json /home/${USER}/sunshine/
fi
chown -R ${PUID}:${PGID} /home/${USER}

# Reset the default username/password if variables were provided
if ([ "X${SUNSHINE_USER:-}" != "X" ] && [ "X${SUNSHINE_PASS:-}" != "X" ]); then
    echo "Setting sunshine default username/password"
    gosu ${USER} sunshine /home/${USER}/sunshine/sunshine.conf --creds ${SUNSHINE_USER} ${SUNSHINE_PASS}
fi

# Wait here for the X server to be available
echo "Waiting for X Server $DISPLAY to be available"
wait_for_x

LOG_LEVEL=${LOG_LEVEL:-info}
echo "Starting sunshine with DISPLAY=${DISPLAY} and LOG_LEVEL=${LOG_LEVEL}"

# Start Sunshine
gosu ${USER} sunshine min_log_level=$LOG_LEVEL /home/${USER}/sunshine/sunshine.conf
