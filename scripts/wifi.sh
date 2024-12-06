doas wpa_supplicant -B -i wlo1 -D nl80211 -c /etc/wpa_supplicant/wpa_supplicant.conf
doas dhcpcd wlo1
ping -c 3 google.com
