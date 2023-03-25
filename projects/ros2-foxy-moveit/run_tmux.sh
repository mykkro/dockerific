#!/bin/bash


tmux new-session \; \
     send-keys 'source /opt/ros/foxy/setup.bash; source /home/rosdemos/workspace/install/setup.bash' C-m \; \
     split-window -h \; \
     send-keys  'source /opt/ros/foxy/setup.bash;  source /home/rosdemos/workspace/install/setup.bash' C-m \;  \
     split-window -v  \;  \
     send-keys  'mc' C-m \; set-option -g mouse on