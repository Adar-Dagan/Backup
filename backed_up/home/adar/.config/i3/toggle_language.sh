#!/bin/bash

# Get the current keyboard layout
layout=$(setxkbmap -query | grep layout | awk '{print $2}')

# Toggle between 'us' and 'il'
if [ "$layout" == "us" ]; then
    setxkbmap il
else
    setxkbmap us
fi
