# Volttron Docker

Based on the [official Volttron Docker image](https://github.com/VOLTTRON/volttron-docker) which currently:

- Is not compatible with the latest Volttron 8.x
- Does not make use of the standard `vctl` utility

## Configuration

- Mount a configuration file (for high-level configuration) at `/home/volttron/configuration.yml`
- Mount a config volume (for agent and driver config) at `/home/volttron/config`
- Mount a user_agents volume (for agents not provided with volttron) at `/home/volttron/user_agents`
