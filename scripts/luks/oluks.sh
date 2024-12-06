doas cryptsetup luksOpen /dev/sda cryptdisk
doas cryptsetup -v status cryptdisk
doas mount /dev/mapper/cryptdisk /mnt/cryptdisk
