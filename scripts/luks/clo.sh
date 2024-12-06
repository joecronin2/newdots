#!/bin/zsh

doas umount -vl /mnt/cryptdisk
doas cryptsetup luksClose cryptdev
doas losetup -D
