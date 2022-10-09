
FROM ubuntu:22.04 AS builder

# Pulling Sunshine v0.11.1
ARG SUNSHINE_VERSION=v0.11.1

ARG CMAKE_BUILD_TYPE="${CMAKE_BUILD_TYPE:-Release}"
ARG SUNSHINE_EXECUTABLE_PATH="${SUNSHINE_EXECUTABLE_PATH:-/usr/bin/sunshine}"
ARG SUNSHINE_ASSETS_DIR="${SUNSHINE_ASSETS_DIR:-/etc/sunshine}"
ARG SUNSHINE_ENABLE_WAYLAND=${SUNSHINE_ENABLE_WAYLAND:-OFF}
ARG SUNSHINE_ENABLE_X11=${SUNSHINE_ENABLE_X11:-ON}
ARG SUNSHINE_ENABLE_DRM=${SUNSHINE_ENABLE_DRM:-ON}
ARG SUNSHINE_ENABLE_CUDA=${SUNSHINE_ENABLE_CUDA:-ON}

ARG DEBIAN_FRONTEND=noninteractive 
ARG TZ="Europe/London"

RUN \
    echo "**** Update apt database ****" \
        && apt-get update \
    && \
    echo "**** Install build dependinces ****" \
        && apt-get install -y \
            # Basic tools
            git build-essential \
            # Common
            cmake gcc-10 g++-10 libssl-dev libavdevice-dev libboost-thread-dev libboost-filesystem-dev libboost-log-dev libpulse-dev libopus-dev libevdev-dev \
            # X11
            libxtst-dev libx11-dev libxrandr-dev libxfixes-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev \
            # KMS
            libdrm-dev libcap-dev \
            # Cuda + NvFBC
            nvidia-cuda-dev nvidia-cuda-toolkit


RUN \
    echo "**** Fetch Sunshine source ****" \
        && git clone "https://github.com/loki-47-6F-64/sunshine.git" /sunshine \
        && cd /sunshine \
        && git checkout -qf ${SUNSHINE_VERSION} \
        && git submodule update --init --recursive \
    && \
    echo

RUN \
    echo "**** Build Sunshine ****" \
        && cd /sunshine \
        && mkdir build && cd build \
        && cmake \
            "-DCMAKE_C_COMPILER=gcc-10" \
            "-DCMAKE_CXX_COMPILER=g++-10" \
            "-DCMAKE_BUILD_TYPE=$CMAKE_BUILD_TYPE" \
            "-DSUNSHINE_EXECUTABLE_PATH=$SUNSHINE_EXECUTABLE_PATH" \
            "-DSUNSHINE_ASSETS_DIR=$SUNSHINE_ASSETS_DIR" \
            "-DSUNSHINE_ENABLE_WAYLAND=$SUNSHINE_ENABLE_WAYLAND" \
            "-DSUNSHINE_ENABLE_X11=$SUNSHINE_ENABLE_X11" \
            "-DSUNSHINE_ENABLE_DRM=$SUNSHINE_ENABLE_DRM" \
            "-DSUNSHINE_ENABLE_CUDA=$SUNSHINE_ENABLE_CUDA" \
            .. \
        && make -j${nproc} \
        && ./gen-deb \
    && \
    echo


##############################
FROM ubuntu:22.04

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
COPY --from=builder /sunshine/build/package-deb/sunshine.deb /sunshine.deb
RUN \
    echo "**** Update apt database ****" \
        && sed -i '/^.*main/ s/$/ contrib non-free/' /etc/apt/sources.list \
    && \
    echo "**** Update apt database ****" \
        && apt-get update \
    && \
    echo "**** Install certificates ****" \
        && apt-get install -y --reinstall \
            ca-certificates \
    && \
    echo "**** Install Sunshine ****" \
        && apt-get install -y /sunshine-debian.deb \
    && \
    echo "**** Section cleanup ****" \
        && rm -rf \
            /var/lib/apt/lists/* \
    && \
    echo


# Install remaining packages
# Ref: 
#   - https://github.com/games-on-whales/gow/blob/09a855234eb314f42bc70068a7e719ea84bcce10/images/sunshine/Dockerfile
RUN \
    echo "**** Update apt database ****" \
        && dpkg --add-architecture i386 \
    && \
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
