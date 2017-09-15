#!/usr/bin/env bash


# env variables that can be set:
#
# CURRENT_IP: The IP used for Spark to communicate with the executors and also important to Mesos.
#

if [ -z $USER_ID ] || [ -z $GROUP_ID ] || [ -z $USER_NAME ]; then
  echo "NOTE: Spark needs a valid user in the system to work, so the --user option in Docker run **MUST NOT** be used. Specify the USER_ID, the GROUP_ID and the USER_NAME using the env variables explained in chempack and run again everything, unless you are running as root (not recommended)."
fi

# add to path spark bins
export PATH="$PATH:/usr/local/spark/bin"

# IMPORTANT: detect current IP. As default, we detect using hostname, but it may be different.
CURRENT_IP="${CURRENT_IP:-$(hostname -i)}"
echo "CURRENT_IP: $CURRENT_IP"
echo "Remember that it should be an external interface for spark mesos to work"

# important for Mesos...
export LIBPROCESS_IP=$CURRENT_IP

# update default spark conf
sed -i 's;CURRENT_IP;'$CURRENT_IP';g' "$SPARK_HOME/conf/spark-defaults.conf"

# change ownership of everything
chown -R $USER_ID:$GROUP_ID $SPARK_HOME

