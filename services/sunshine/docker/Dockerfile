
FROM alpine:3.16 AS gosu-downloader


# Download runtime requirements
ARG GOSU_VERSION=1.14
RUN \
    echo "**** Fetch gosu ****" \
        && mkdir -p /tmp/gosu/bin \
        && wget -O /tmp/gosu/bin/gosu https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-amd64 \
        && chmod +x /tmp/gosu/bin/gosu \
    && \
    echo


##############################
FROM ghcr.io/games-on-whales/sunshine:edge

# Set default user as root
USER root

# Install gosu
COPY --from=gosu-downloader /tmp/gosu/bin/gosu /usr/local/bin/gosu

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
    echo "**** Verify gosu works ****" \
        && gosu nobody true \
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

# Execute override
ENTRYPOINT ["/entrypoint.sh"]
