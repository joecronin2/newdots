doas cryptsetup -v status cryptdisk

if [ $? -eq 0 ]; then
	cp cryptbak.tar.gz cryptbak_old.tar.gz
	doas tar -czf cryptbak.tar.gz /mnt/cryptdisk
else
	echo "cryptdisk must be mounted"
fi
