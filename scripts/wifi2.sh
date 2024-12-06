killall NetworkManager
killall networkmanager
killall wpa_supplicant
ip link set wlo1 up
doas wpa_supplicant -i wlo1 -D nl80211 -c /etc/wpa_supplicant/hotspot.conf -B
dhcpcd wlo1
