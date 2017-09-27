#!/usr/bin/env bash


# iterate through all the config files: FORMAT: XXX-name.sh
for conf_file in /run/*.sh; do
  echo "Sourcing $conf_file ..."
  source $conf_file
done

# you can use the --user option in docker run, and, if no user_id, group_id and user_name are specified, it will run as the given user, else it will create a user in the system and run the command as that user using gosu. This is specially useful when running Spark or any java stuff inside, as I don't know why, but they require a user in the system to run correctly.


# a horrible HACK, to prevent commands that change the entrypoint to /bin/sh

if [[ $@ == "-c "* ]]; then
  # special case of mesos shelling everything... add quotes to all args
  # the -c is normal, the rest goes in a ''

  COMMAND=""
  i=1
  for arg in $@; do
    if [ $i -ne 1 ]; then
      COMMAND="$COMMAND $arg"
    fi
    i=$((i + 1))
  done
  # trim spaces
  COMMAND=$(echo -e "$COMMAND" | sed -e 's/^[[:space:]]*//')
else
  COMMAND="$@"
fi

echo "Command: $COMMAND"

if [ -z $RUN_GOSU ]; then
  echo "Running as root"
  exec $COMMAND
else
  echo "Running with user $USER_NAME:$USER_ID:$GROUP_ID"

  exec gosu $USER_ID:$GROUP_ID sh -c "$COMMAND"
fi

