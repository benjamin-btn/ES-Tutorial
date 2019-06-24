#!/bin/bash

tmux new-session -d -s mytmux-$(hexdump -n 2 -v -e '/1 "%02X"' /dev/urandom)

HOSTS=$@
KEY="ES-Key-7th.pem"

for i in $HOSTS
do
        tmux split-window -h "ssh -i $KEY -l ec2-user -o StrictHostKeyChecking=no $i"
        tmux select-layout tiled > /dev/null
done

tmux select-pane -t 0
tmux set-window-option synchronize-panes on > /dev/null
