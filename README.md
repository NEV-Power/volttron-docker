# Volttron Docker

This is a Docker configuration developed by [NEV Power](https://github.com/NEV-Power) based on the [official Volttron Docker](https://github.com/VOLTTRON/volttron-docker) which at time of development:

- Is not compatible with the latest Volttron 8.x
- Does not make use of the standard `vctl` utility
- Does not provide a means of installing custom agent dependencies

## Caveats

### Implementation

This implementation follows the [official Voltton installation instructions](https://volttron.readthedocs.io/en/main/introduction/platform-install.html) where possible. Some of the idiosyncrasies of this implementation are due to the tightly-coupled nature of the Volttron codebase and the standard Volttron deployment paradigm in which the Volttron virtual environment is managed internally by deployment scripts.

As of [January 2022](https://github.com/VOLTTRON/volttron-developer/blob/main/code-modular-white-paper.pdf) the Volttron development team have begun work to decouple the Volttron codebase and move toward a more standard deployment mechanism. When this work is complete it is envisaged that this implementation will need to be thoroughly revisited/refactored.

### RabbitMQ

This implementation _does not support RabbitMQ_ as it was not required by NEV Power.

### Requirements.txt

This implementation uses a `requirements.txt` file containing dependencies for specific NEV Power dependencies. At present this can only be changed by over-riding `requirements.txt` in this repo. In future it would be potentially possible to either mount `requirements.txt` as a volume or generate it dynamically.

### HTTP/S

While the Volttron platform web service feature can be used by setting `VOLTTRON_BIND_WEB_ADDRESS`, only http is supported. Adding https would require additional work to either generate or add SSL certificates to the image.

## Configuration

### Volumes

Volttron configuration is deployed to the Docker image via volume mounts:

- Mount a configuration file (for high-level configuration) at `/home/volttron/volttron/configuration.yml` (based on `configuration.yml.example`)
- Mount a config volume containing agent and driver config) at `/home/volttron/volttron/config` (based on `config.example`)
- Mount an agents volume (for any agents not provided with Volttron) at `/home/volttron/volttron/agents`
- Mount individual driver volumes (for any drivers not provided with Volttron) at `/home/volttron/volttron/services/core/PlatformDriverAgent/platform_driver/interfaces/<driver_name>`
- Mount a custom 

### Environment

 - `VOLTTRON_CONFIG_DIR` - This is where `configure-volttron.py` will look for Volttron config as mounted using the Volumes above. Unless you have reason to use a different location, set this to `/home/volttron/volttron/config`.
 - `VOLTTRON_BIND_WEB_ADDRESS` - If using the Volttron web interface set this to the `bind-web-address` as per the Volttron [platform configuration docs](https://volttron.readthedocs.io/en/develop/deploying-volttron/platform-configuration.html#volttron-config-file).

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
