loopdev=`doas losetup -f`
img=$1

# setup loop device
doas losetup $loopdev $img

# note: format like this:
# doas cryptsetup luksFormat /dev/loop0

doas cryptsetup luksOpen $loopdev cryptdev
doas mount /dev/mapper/cryptdev /mnt/cryptdisk
cd /mnt/crypdisk
# ./run

# mkfs.ext4 /dev/mapper/cryptdev

