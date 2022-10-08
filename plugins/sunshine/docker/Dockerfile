FROM ubuntu:20.04 AS base


ENV DEBIAN_FRONTEND=noninteractive 
ENV TZ="Pacific/Auckland"


# Install runtime requirements
RUN \
    echo "**** Update apt database ****" \
        && apt-get update \
    && \
    echo "**** Install runtime dependencies ****" \
        && apt-get install -y --no-install-recommends \
            gosu \
    && \
    echo "**** Verify gosu works ****" \
        && gosu nobody true \
    && \
    echo "**** Section cleanup ****" \
        && rm -rf \
            /var/lib/apt/lists/* \
    && \
    echo


# Install sunshine
ARG SUNSHINE_VERSION=0.11.1
ARG SUNSHINE_PACKAGE=sunshine-2004.deb
RUN \
    echo "**** Update apt database ****" \
        && apt-get update \
    && \
    echo "**** Install certificates ****" \
        && apt-get install -y --reinstall \
            ca-certificates \
    && \
    echo "**** Install isntall dependinces ****" \
        && apt-get install -y --no-install-recommends \
            wget \
    && \
    echo "**** Fetch Sunshine deb package ****" \
        && cd /tmp \
        && wget -O /tmp/sunshine-debian.deb \
            https://github.com/loki-47-6F-64/sunshine/releases/download/v${SUNSHINE_VERSION}/${SUNSHINE_PACKAGE} \
    && \
    echo "**** Install Sunshine ****" \
        && apt-get install -y /tmp/sunshine-debian.deb \
    && \
    echo "**** Section cleanup ****" \
        && rm -rf \
            /var/lib/apt/lists/* \
            /tmp/* \
    && \
    echo


# Install remaining packages
# Ref: 
#   - https://github.com/games-on-whales/gow/blob/09a855234eb314f42bc70068a7e719ea84bcce10/images/sunshine/Dockerfile
RUN \
    echo "**** Update apt database ****" \
        && apt-get update \
    && \
    echo "**** Install remaining dependencies ****" \
        && apt-get install -y --no-install-recommends \
            # Seems that libgbm1 and libgl is missing
            libgbm1 libgles2-mesa libegl1 libgl1-mesa-dri \
            # Intel GPU drivers
            i965-va-driver-shaders \
            intel-media-va-driver-non-free \
            libdrm-intel1 \
            libva-drm2 libva-x11-2 va-driver-all \
            # Install xdpyinfo so that we can wait for X11 on startup
            x11-utils \
            # libavahi for LAN discovery
            libavahi-client3 \
    && \
    echo "**** Section cleanup ****" \
        && rm -rf \
            /var/lib/apt/lists/* \
    && \
    echo


# Configure default user and set env
ENV \
    USER="default" \
    USER_PASSWORD="password" \
    HOME="/home/default" \
    TZ="Pacific/Auckland" \
    USER_LOCALES="en_US.UTF-8 UTF-8"
RUN \
    echo "**** Configure default user '${USER}' ****" \
        && mkdir -p ${HOME} \
        && useradd -d ${HOME} -s /bin/bash ${USER} \
        && chown -R ${USER} ${HOME} \
        && echo "${USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && \
    echo

# Set the working directory
WORKDIR ${HOME}

# Config files
COPY overlay /

# Ref:
#   - https://github.com/moonlight-stream/moonlight-docs/wiki/Setup-Guide#manual-port-forwarding-advanced
EXPOSE 47984-47990/tcp
EXPOSE 48010
EXPOSE 48010/udp 
EXPOSE 47998-48000/udp


ENTRYPOINT ["/entrypoint.sh"]
