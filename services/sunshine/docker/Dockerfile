
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
# The users UID and GID will be set on container startup
ENV \
    PUID=1000 \
    PGID=1000 \
    UMASK=000

# Import overlay
COPY overlay /

# Ref:
#   - https://github.com/moonlight-stream/moonlight-docs/wiki/Setup-Guide#manual-port-forwarding-advanced
EXPOSE 47984-47990/tcp
EXPOSE 48010
EXPOSE 48010/udp 
EXPOSE 47998-48000/udp

# Execute override
ENTRYPOINT ["/entrypoint.sh"]
