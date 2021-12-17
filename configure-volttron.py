"""
Configure Volttron.

Currently installs agents using vctl as per official docs:

    https://volttron.readthedocs.io/en/main/platform-features/control/agent-management-control.html#agent-installation-and-removal

TODO:

    - Detect if config has changed for an installed agent and update accordingly
    - Detect if config for an installed agent has been removed and uninstall that agent
"""

import os
import sys
import logging
import subprocess
import yaml
from time import sleep


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
)
LOGGER = logging.getLogger("configure-volttron")
VOLTTRON_CTL_CMD = "vctl"


def store_configuration(identity: str, name: str, source_path: str, entry_type: str):
    """
    Store configuration.
    """
    LOGGER.info(f"Storing configuration: {identity} | {name}")
    store_config_cmd = [
        VOLTTRON_CTL_CMD,
        "config",
        "store",
        identity,
        name,
        os.path.expandvars(source_path),
        f"--{entry_type}",
    ]
    try:
        LOGGER.info(f"Running store configuration command: {store_config_cmd}")
        subprocess.check_call(store_config_cmd)
    except subprocess.CalledProcessError as e:
        LOGGER.error(f"Error storing configuration {identity} | {name}: {e}")
    LOGGER.info(f"Configuration stored: {identity} | {name}")


def install_agent(
    agent: str,
    source_path: str,
    identity: str,
    tag: str,
    config_path: str,
    priority: int,
):
    """
    Install an agent.
    """
    LOGGER.info(f"Installing agent: {agent}")
    install_cmd = [VOLTTRON_CTL_CMD, "install"]
    install_cmd.extend(["--vip-identity", identity])
    install_cmd.extend(["--priority", str(priority)])
    install_cmd.extend(["--tag", tag])
    install_cmd.extend(["--start"])
    install_cmd.extend(["--enable"])
    if config_path != "":
        install_cmd.extend(["--agent-config", os.path.expandvars(config_path)])
    install_cmd.extend([os.path.expandvars(source_path)])
    try:
        LOGGER.info(f"Running install command: {install_cmd}")
        subprocess.check_call(install_cmd)
    except subprocess.CalledProcessError as e:
        LOGGER.error(f"Error installing {agent}: {e}")
    LOGGER.info(f"Agent installed: {agent}")


def get_installed_agents() -> dict:
    """
    Get details of currently installed agents
    """
    process = subprocess.run(["vctl", "list"], capture_output=True)
    error = process.stderr.decode("utf-8")
    agents = []
    if error.strip() != "No installed Agents found":
        for line in process.stdout.decode("utf-8").splitlines():
            LOGGER.debug(f"Processing vctl list output line: {line}")
            split_line = line.strip().split()
            split_line += [""] * (5 - len(split_line))  # Sometimes tag is missing
            _, name, identity, tag, priority = split_line
            agents.append(
                {
                    "name": name,
                    "identity": identity,
                    "tag": tag,
                    "priority": int(priority),
                }
            )
    return agents


def configure_agents(agents: dict) -> None:
    """
    Configure agents based on given configration.

    NOTE:

        - Installs agents but currently does not remove them.
        - Installs config store keys/values but currently does not remove them.
        - When a config key is installed to the config store for a given agent
          any existing entry for that key is simply over-written. So we just
          re-apply all pieces of config defined in config_store every time.
    """
    installed_agents = get_installed_agents()
    LOGGER.debug(f"Installed agents: {installed_agents}")

    for agent, spec in agents.items():
        identity = spec["identity"]
        if identity not in [agent["identity"] for agent in installed_agents]:
            # Install missing agent
            source = spec["source"]
            tag = spec["tag"]
            config = spec.get("config", "")
            priority = spec.get("priority", 50)
            install_agent(agent, source, identity, tag, config, priority)
        if "config_store" in spec:
            # Install agent configuration store entries
            for name, entry in spec["config_store"].items():
                if "file" not in entry or not entry["file"]:
                    LOGGER.warn(
                        f"Ignoring {agent} configuration entry {name}: No file specified"
                    )
                    continue
                store_configuration(
                    identity, name, entry["file"], entry.get("type", "json")
                )


def load_config(config_file: str) -> dict:
    """
    Load configuration from file.
    """
    with open(config_file) as f:
        try:
            config = yaml.safe_load(f)
        except Exception:
            raise
    return config


def volttron_running() -> bool:
    """
    Check if volttron is running.
    """
    LOGGER.debug(f"Checking if Volttron has started")
    try:
        process = subprocess.run(
            ["vctl", "status"],
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=4,
        )
    except subprocess.TimeoutExpired:
        LOGGER.debug(f"Volttron status timed out")
        return False
    returncode = process.returncode
    output = process.stdout.decode("utf-8")
    LOGGER.debug(f"Volttron status output: {output}")
    if returncode == 0:
        return True
    return False


def main():
    # Load environment variables
    try:
        volttron_home = os.environ["VOLTTRON_HOME"]
        volttron_config_file = os.environ["VOLTTRON_CONFIG_FILE"]
    except Exception as e:
        LOGGER.error(f"Unable to load environment: {e}")
        sys.exit(os.EX_CONFIG)
    # Wait for Volttron to start
    while not volttron_running():
        LOGGER.info(f"Waiting for Volttron to start")
        sleep(2)
    LOGGER.info(f"Volttron started")
    # Load configuration
    try:
        config = load_config(volttron_config_file)
        LOGGER.info(f"Config loaded: {config}")
    except Exception as e:
        LOGGER.error(f"Unable to load configuration: {e}")
        sys.exit(os.EX_CONFIG)
    # Configure agents
    try:
        configure_agents(config["agents"])
    except Exception as e:
        LOGGER.error(f"Unable to configure agents: {e}")
        sys.exit(os.EX_CONFIG)
    # Exit
    LOGGER.info(f"Exiting")
    sys.exit(os.EX_OK)


if __name__ == "__main__":
    sys.exit(main())
