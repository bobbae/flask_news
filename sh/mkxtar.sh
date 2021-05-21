#!/bin/bash -x
tar zcf x.tar.gz .ssh .vim .vimrc .tmux.conf .shextra .zshrc .zsh .oh-my-zsh scripts .gitconfig  ENV*.txt CMD*txt Hist*txt NOTES.txt  justfile .bashrc .bash_profile
gpg -c x.tar.gz
