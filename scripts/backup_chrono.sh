#!/bin/sh

if [ `whoami` != "root" ]; then
	echo "You must be root to execute this script!"
	exit 0
fi

backupdir=/data/gamebackups/$(date +"%Y-%m-%d_%H:%M")
# make temporary mountpoint for disk
mntpoint=$(mktemp -d /tmp/tmpmount_XXXXXXX)
# use the partition label to identify the drive
part=$(blkid -L EASYROMS)

if [ "$part" == "" ]; then
	echo "No drive found!"
	exit 1
fi

mount -o ro $part $mntpoint

# make the backup directory
mkdir $backupdir
# find state files and copy them to backupdir
fd "\.state" $mntpoint -x cp {} $backupdir

# unmount
umount $mntpoint
rm --dir $mntpoint

echo "Backup successful!"
echo ""
echo "Files copied:"
ls $backupdir

echo ""
echo "the sd card is unmounted, so you can safely remove it"
