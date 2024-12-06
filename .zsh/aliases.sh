# school
blok1_dir=/home/joe/projects/vootiizaavii86/webapp/dashboard
alias fl="USERS_CSV=$blok1_dir/db/users.csv DB_DIR=$blok1_dir/db/users flask --app $blok1_dir run --debug"
alias fld="cd $blok1_dir/..; USERS_CSV=$blok1_dir/users.csv DB_DIR=$blok1_dir/db/ gunicorn secretsapp:app"
alias ct="oneko -tofocus -speed 30 & disown"

###
alias ophost="joe@192.168.4.133"

openproject () {
	project=$(ls $PROJECT_DIR | xargs -I {} zoxide query --score {} 2>/dev/null | sed 's./home/joe/projects/..' | sort | awk '{print $2}' | fzf)
	if [ -z "$project" ]; then
		exit 1;
	else # only cd to project_dir if an option was selected
		cd "$PROJECT_DIR/$project"
	fi
}

# essential
alias br="librewolf"
alias sosh="source ~/.zshrc"
alias m="make"
alias u="nvim"
alias te="tar -xvf"
alias a="eza --icons --group-directories-first -lahrMg "
alias at="a -T"
alias b="cd .."
alias reb="doas reboot"
alias c="clear"
alias shd="doas poweroff"
alias alg="ls | rg"
alias ag="a | rg"
alias ff="fastfetch"

# git aliases
alias gcl="git clone"
alias gdf="git diff"
alias gcm="git commit -m"
alias gpl="git pull"
alias gst="git status"
alias ga="git add"
alias gpsh="git push"
alias glg="git log"
alias grlg="git reflog"
alias gdfc="git diff --cached"

alias dcu="docker compose up --build"

# task stuff
alias tp="task +p"
alias ts="task +s"

alias kl="ps --no-headers -Ao pid,comm | fzf | awk '{print \$1}' | xargs -I{} kill -9 {}"

alias nt="aplay /home/joe/sounds/notification.wav &> /dev/null &"

alias ctbloody="figlet -f Bloody.flf"
alias ctansi="figlet -f 'ANSI Regular.flf'"
alias ctansishadow="figlet -f 'ANSI Shadow.flf'"

alias i="openproject && nvim"

# debug
alias delcores="fd core /tmp -x rm -v"
alias lcore="fd core /tmp | sort -r | fzf"

alias start_ssh_agent="eval \"$(ssh-agent -s)\"; ssh-add ~/.ssh/sshkey"

alias kb_us="setxkbmap us -option caps:escape"
alias kb_dvorak="setxkbmap us dvorak -option caps:swapescape"
alias kb_dvp="setxkbmap us dvp -option caps:swapescape"
#alias kb_dvorak="setxkbmap us dvp -option caps:escape"
alias asdf="kb_dvorak"
alias aoeu="kb_us"

alias getbattery="cat /sys/class/power_supply/BAT1/capacity"
alias xrate="xset r rate 180 100"

alias snap="doas btrfs subvolume snapshot / /.snapshots/$(date -Iminutes) && doas grub-mkconfig -o /boot/grub/grub.cfg"

alias cpssh="keepassxc-cli clip /home/joe/Passwords.kdbx 'SSH key'"

# clipboard
alias clp="xclip -selection clipboard"

# portage
alias emav="doas emerge --ask --verbose"

# alias sudo="doas"
alias sx="startx"

alias npu="doas nvim /etc/portage/package.use"

alias cm="cmatrix"
alias cb="cbonsai -l"

alias mac="make clean"
alias md="make debug"
alias mi="make image"
alias mci="make clean; c; make image"
alias mn="make clean; make -j12 >> /dev/null"

alias rkp="killall plasmashell && kstart plasmashell"
alias alconf="nvim ~/.zsh/aliases.sh"
alias resh="c; source ~/.zshrc"
alias alssh="ssh root@192.168.4.55"
alias vim="nvim"
alias pi="paru -S"
alias pu="paru -R"
alias q="qalc"
alias hyprconf="u ~/.config/hypr/hyprland.conf"
alias vconf="u ~/.config/nvim/init.lua"
alias crt="cool-retro-term"

export EDITOR=nvim
eval "$(zoxide init zsh)"

alias o="z"
ao() {
	o $1 && eza --icons -- $2
}

ou() {
	o $1 && u -- $2
}

mnl() {
	man -Tpdf $1 | zathura - & disown
}

alias resw='xwallpaper --stretch Wallpapers/forest2.jpg'
