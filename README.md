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

Volttron configuration is deployed to the Docker image via volume mounts:

- Mount a configuration file (for high-level configuration) at `/home/volttron/configuration.yml`
- Mount a config volume (for agent and driver config) at `/home/volttron/config`
- Mount a user_agents volume (for agents not provided with volttron) at `/home/volttron/user_agents`

Examples of configuration files are included for reference.
