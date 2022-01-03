#!/bin/sh

# Environment
set -e
:   ${VOLTTRON_LOG_FILE:="${VOLTTRON_ROOT}/volttron.log"}
:   ${VOLTTRON_AGENT_CONFIG_FILE:="${VOLTTRON_ROOT}/configuration.yml"}
:   ${CONFIGURE_VOLTTRON:="./configure-volttron.py"}

# Create and tail log file
touch $VOLTTRON_LOG_FILE
tail -F $VOLTTRON_LOG_FILE --max-unchanged-stats=5 &

# Activate Volttron virtual environment
. ${VOLTTRON_ROOT}/env/bin/activate

# Start Volttron agent configuration
# NOTE: This will wait in the background until Volttron is started.
export VOLTTRON_AGENT_CONFIG_FILE
echo "Starting Volttron configuration with VOLTTRON_AGENT_CONFIG_FILE=${VOLTTRON_AGENT_CONFIG_FILE}"
python -u $CONFIGURE_VOLTTRON >> ${VOLTTRON_LOG_FILE} 2>&1 &

# Create the Volttron config file and pre-populate it with any required config.
# NOTE: Additional config will be added by Volttron on first boot:
#       https://volttron.readthedocs.io/en/develop/deploying-volttron/platform-configuration.html
echo "[volttron]" > ${VOLTTRON_HOME}/config
if test -n "${VOLTTRON_BIND_WEB_ADDRESS-}"; then
 echo "bind-web-address = ${VOLTTRON_BIND_WEB_ADDRESS}" >> ${VOLTTRON_HOME}/config
fi

# Start Volttron
# NOTE: The examples/rotatinglog.py logging config hard-codes volttron.log
echo "Starting Volttron with VOLTTRON_HOME=${VOLTTRON_HOME}"
exec volttron -vv -L examples/rotatinglog.py 
