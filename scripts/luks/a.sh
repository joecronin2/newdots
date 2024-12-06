doas cryptsetup luksOpen /dev/sda cryptdisk
doas cryptsetup -v status cryptdisk
doas mount /dev/mapper/cryptdisk /mnt/cryptdisk

alacritty -e /mnt/cryptdisk/cuda --config /mnt/cryptdisk/config.kcpps &
alacritty -e sh /mnt/cryptdisk/lvj/start.sh
