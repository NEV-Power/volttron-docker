# Volttron Docker

This is a Docker configuration based on the [official Volttron Docker](https://github.com/VOLTTRON/volttron-docker) which at time of development:

- Is not compatible with the latest Volttron 8.x
- Does not make use of the standard `vctl` utility

## Caveats

### Implementation

This implementation follows the [official Voltton installation instructions](https://volttron.readthedocs.io/en/main/introduction/platform-install.html) where possible. Some of the idiosyncrasies of this implementation are due to the tightly-coupled nature of the Volttron codebase and the standard Volttron deployment paradigm in which the Volttron virtual environment is managed internally by deployment scripts.

As of [December 2021](https://github.com/VOLTTRON/volttron-developer/blob/be303669d137d3ffc2492c6e01f28e864d4605cd/README.md) the Volttron development team have begun work to decouple the Volttron codebase and move toward a more standard deployment mechanism. When this work is complete it is envisaged that this implementation will need to be thoroughly revisited/refactored.

### RabbitMQ

This implementation _does not support RabbitMQ_ as it was not required by NEV Power.

## Configuration

### Volumes

Volttron configuration is deployed to the Docker image via volume mounts:

- Mount a configuration file (for high-level configuration) at `/home/volttron/volttron/configuration.yml` (based on `configuration.yml.example`)
- Mount a config volume containing agent and driver config) at `/home/volttron/volttron/config` (based on `config.example`)
- Mount an agents volume (for any agents not provided with Volttron) at `/home/volttron/volttron/agents`
- Mount individual driver volumes (for any drivers not provided with Volttron) at `/home/volttron/volttron/services/core/PlatformDriverAgent/platform_driver/interfaces/<driver_name>`

### Environment

 - `VOLTTRON_CONFIG_DIR` - This is where `configure-volttron.py` will look for Volttron config as mounted using the Volumes above. Unless you have reason to use a different location, set this to `/home/volttron/volttron/config`.

## Deployment

### Docker-compose

An example `docker-compose.yml` is included.

### Updating configuration

While it is possible to add agents, drivers and configuration to a running container, the container created by this image is designed to be ephemeral.

As such when deploying updated agents, drivers and configuration it is usually easiest to simply rebuild the container from scratch:

```
docker-compose stop volttron
docker-compose up -d --build --force-recreate volttron
```

### Logging

The Volttron logfile can be followed via standard Docker logging:

```
docker-compose logs -f --tail=100 volttron
```
