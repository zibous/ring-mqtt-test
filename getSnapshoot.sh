#!/bin/bash

## sudo apt-get install fonts-freefont-ttf

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

[[ -z "$1" ]] && { echo "Missing Filename"; exit 1; }

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "LINUX SYSTEM -  Get snapshoot"
    ffmpeg -y \
    -hide_banner  \
    -loglevel quiet  \
    -rtsp_transport tcp \
    -i rtsp://10.1.1.217:8554/54e019cfa225_live \
    -s 640x360  \
    -vframes 1 \
    -vf drawtext="fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:\
                fontcolor=white:fontsize=38:x=40:y=1000: \
                text='Snapshoot  %{localtime\:%Y.%m.%d %H\\\\\:%M\\\\\:%S}'"  \
    $1

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "APPLE OSX SYSTEM -  Get snapshoot"
    ffmpeg -y \
    -hide_banner  \
    -loglevel quiet  \
    -rtsp_transport tcp \
    -i rtsp://10.1.1.217:8554/54e019cfa225_live \
    -s 640x360  \
    -vframes 1 \
    -vf drawtext="fontfile=/Users/petsie1612/Library/Fonts/FreeSans.ttf:\
                fontcolor=white:fontsize=38:x=40:y=1000: \
                text='Snapshoot %{localtime\:%Y.%m.%d %H\\\\\:%M\\\\\:%S}'"  \
    $1
else
   echo "not supported..."
fi


