#!/bin/zsh

file_name=$1
if [ "$file_name" == "" ]; then
	echo "Not enough arguments. Usage:"
	echo "mountloop [img_file] [mount_point]"
	exit 
fi

mountpoint=$2
if [ "$mountpoint" == "" ]; then
	echo "No mountpoint provided. Use `pwd`? (y/n)"
	if [ read == "y" ]; then
		mountpoint=`pwd`
	else
		echo "Invalid mount point. Exiting..."
		exit
	fi

echo "Mounting `realpath $file_name` to `realpath $mountpoint`"

# losetup -f gets an available loop device
doas losetup $(losetup -f) "$file_name"
losetup -a
