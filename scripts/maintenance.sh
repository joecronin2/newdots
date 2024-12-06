#!/bin/zsh

dialog_options=(
    "BTRFS scrub" "btrfs scrub start /" off
    "Create snapshot" "timeshift --create" off
    "Backup GPT" "doas sfdisk --backup --backup-file=/home/joe/dotfiles/backup /dev/nvme0n1" off
		"Update system" "emerge -avuDV" off
		"Commit and push dots" "pushd && cd /home/joe/dotfiles && git commit "autocommit" && git push && popd" off
)

dialog  --checklist "Select system maintenance options" 0 0 0 $dialog_options


