#!/bin/bash

echo "Setup and configure server"

file_name=config.yaml

config_dir=$1

if [ -d "$config_dir" ]
then
	echo "reading config dir contents"
	config_files=$(ls "$config_dir")
else
	echo "no config dir, creating one"
	mkdir "$config_dir"
	touch "$config_dir/config.sh"
fi

user_group=$2
echo "user group is $user_group"

if [ "$user_group" == "max" ]
then
	echo "configure the server"
elif [ "$user_group" == "admin" ]
then
	echo "administer the server"
else
	echo "No permission to configure server."
fi

echo "contents of config folder $config_files"

