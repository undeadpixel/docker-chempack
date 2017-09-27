#!/usr/bin/env bash


add_user_in_system() {
  useradd -m -s /bin/bash -u $USER_ID -U $USER_NAME
  groupmod -g $GROUP_ID $USER_NAME
}

if [ ! -z $USER_ID ] || [ ! -z $GROUP_ID ] || [ ! -z $USER_NAME ]; then
  # add default values to USER_ID, GROUP_ID and USER_NAME if any of them is set
  
  USER_ID=${USER_ID:-1000}
  GROUP_ID=${GROUP_ID:-1000}
  USER_NAME=${USER_NAME:-"chempack"}

  RUN_GOSU=true
  add_user_in_system

  echo "Using '$USER_NAME' ($USER_ID:$GROUP_ID)."
else
  echo "Using Docker's specified user."
fi

