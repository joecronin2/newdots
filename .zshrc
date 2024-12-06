source /opt/python_venv/main/bin/activate
source /home/joe/.zsh/init.sh
source /home/joe/.zsh/aliases.sh
# source /home/joe/.zsh/prompt.sh

export PROJECT_DIR=/home/joe/projects

path+=(~/scripts)
path+=(~/scripts/slots)
path+=(/home/joe/.cargo/bin)

export HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000

# export NVM_DIR="$HOME/.nvm"
# [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
# [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

_direnv_hook() {
  trap -- '' SIGINT;
  eval "$("/usr/bin/direnv" export zsh)";
  trap - SIGINT;
}
typeset -ag precmd_functions;
if [[ -z "${precmd_functions[(r)_direnv_hook]+1}" ]]; then
  precmd_functions=( _direnv_hook ${precmd_functions[@]} )
fi
typeset -ag chpwd_functions;
if [[ -z "${chpwd_functions[(r)_direnv_hook]+1}" ]]; then
  chpwd_functions=( _direnv_hook ${chpwd_functions[@]} )
fi
fastfetch
