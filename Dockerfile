FROM python:3.9-slim-bullseye

ENV VOLTTRON_VERSION=8.1.1 
ENV VOLTTRON_REPO=https://github.com/VOLTTRON/volttron
ENV VOLTTRON_USER=volttron
ENV VOLTTRON_GROUP=volttron
ENV VOLTTRON_ROOT=/home/${VOLTTRON_USER}/volttron
ENV VOLTTRON_HOME=/home/${VOLTTRON_USER}/.volttron

USER root

# Install system dependencies
RUN apt-get update \
 && apt-get -y upgrade \
 && apt-get install -y --no-install-recommends \
     build-essential \
     python3-dev \
     python3-venv \
     openssl \
     libssl-dev \
     libevent-dev \
     libpq-dev \
     git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Create volttron user
RUN useradd --create-home $VOLTTRON_USER

# Get volttron
USER $VOLTTRON_USER
RUN git -c advice.detachedHead=false clone --depth 1 --branch $VOLTTRON_VERSION $VOLTTRON_REPO $VOLTTRON_ROOT

# Bootstrap volttron
WORKDIR $VOLTTRON_ROOT
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1
RUN python3 bootstrap.py

# Install additional Python dependencies
RUN . env/bin/activate
# TODO: make this externally configurable
RUN ./env/bin/pip install \
     psycopg2 \
     paho-mqtt \
     minimalmodbus

# Entrypoint
USER root 
COPY --chown=volttron:volttron entrypoint.sh ./entrypoint.sh
COPY --chown=volttron:volttron configure-volttron.py ./configure-volttron.py
USER $VOLTTRON_USER
ENTRYPOINT ["./entrypoint.sh"]
