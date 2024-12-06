#!/bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
    xrdb -merge $sysresources
fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"
fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi

# Set key repeat rate
xset r rate 180 100

# Display configuration
xrandr --output eDP-1 --mode 1920x1080
xrandr --output HDMI-1 --mode 2560x1440 --rate 120.00 --set "Broadcast RGB" "Full"

# Set wallpaper
xwallpaper --maximize /home/joe/Wallpapers/dark_mountain.jpg &
setxkbmap dvcustom -option caps:swapescape

# Start background services
# dbus-run-session --sh-syntax --exit-with-session &
unclutter --timeout 5 &
dwmblocks &
# qbittorrent &
picom &
# oneko -tofocus -speed 30 &
alacritty &
gentoo-pipewire-launcher &
wpctl set-volume @DEFAULT_AUDIO_SINK@ 0% &
exec dbus-launch --exit-with-session dwm
