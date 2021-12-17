#!/bin/sh

# Environment
set -e
:   ${VOLTTRON_LOG_FILE:="${VOLTTRON_ROOT}/volttron.log"}
:   ${VOLTTRON_CONFIG_FILE:="${VOLTTRON_ROOT}/configuration.yml"}
:   ${CONFIGURE_VOLTTRON:="./configure-volttron.py"}

# Create and tail log file
touch $VOLTTRON_LOG_FILE
tail -F $VOLTTRON_LOG_FILE --max-unchanged-stats=5 &

# Activate Volttron virtual environment
. ${VOLTTRON_ROOT}/env/bin/activate

# Start Volttron configuration
# NOTE: This will wait in the background until Volttron is started.
export VOLTTRON_CONFIG_FILE
export VOLTTRON_CONFIG_DIR
echo "Starting Volttron configuration with VOLTTRON_CONFIG_FILE=${VOLTTRON_CONFIG_FILE}"
python -u $CONFIGURE_VOLTTRON >> ${VOLTTRON_LOG_FILE} 2>&1 &

# Start Volttron
# NOTE: The examples/rotatinglog.py logging config hard-codes volttron.log
echo "Starting Volttron with VOLTTRON_HOME=${VOLTTRON_HOME}"
exec volttron -vv -L examples/rotatinglog.py 
