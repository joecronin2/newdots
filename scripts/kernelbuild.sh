#!/bin/bash

set -x

# delete old joekernel image
rm /boot/vmlinuz-joekernel
# copy image to /boot
cp /home/joe/Desktop/linux/arch/x86_64/boot/bzImage /boot/vmlinuz-joekernel

# make initramdisk
mkinitcpio -P joekernel

# regerate grub config
grub-mkconfig -o /boot/grub/grub.cfg
