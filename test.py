#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from os import sys, path
sys.path.append(path.dirname(path.abspath(__file__)))

"""simple check if python 3 is used"""
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

try:
    import time
    import ffmpeg
    import sys
    import paho.mqtt.client as paho
    import subprocess

except Exception as e:
    print(f"Import error: {str(e)} line {sys.exc_info()[-1].tb_lineno}, check requirements.txt")
    sys.exit(1)

try:
    import config
except Exception as e:
    print('Application Configuration error {}, check config.py'.format(e))
    sys.exit(1)


def snapshoot_image(filename: str = "", mode: int = 1):
    if filename and mode > 0:
        if mode == 1:
            subprocess.call(["{}/getSnapshoot.sh".format(config.ROOTPATH), filename])
        else:
            try:
                (
                    ffmpeg
                    .input(config.RTSP_URL, ss=0)
                    .filter('scale', config.IMG_SIZE, -1)
                    # .filter("drawtext", "fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontcolor=white:fontsize=36:x=40:y=1000:text='%{localtime\:%Y.%m.%d %H\\\\\:%M\\\\\:%S}'")
                    .output(filename, vframes=config.IMG_FRAME)
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                )
            except ffmpeg.Error as e:
                print(e.stderr.decode(), file=sys.stderr)
                sys.exit(1)


def on_message(client, userdata, message):
    try:
        if (message.topic == config.RING_MOTION):
            filename = "{}lastmotion_{}.{}".format(config.IMG_DIR, time.strftime(config.IMG_TIME), config.IMG_EXT)
            snapshoot_image(filename, 1)
        if (message.topic == config.RING_DING):
            filename = "{}lastding_{}.{}".format(config.IMG_DIR, time.strftime(config.IMG_TIME), config.IMG_EXT)
            snapshoot_image(filename, 1)
    except BaseException as e:
        print(
            f"Error {__package__}:{__name__}.{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")


def run_mqttwatch():
    try:
        c = paho.Client()
        c.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
        c.connect(config.MQTT_HOST, config.MQTT_PORT, keepalive=config.MQTT_KEEPALIVE)
        c.subscribe(config.RING_MOTION)
        c.subscribe(config.RING_DING)
        c.on_message = on_message
        c.loop_forever()
    except BaseException as e:
        print(f"Application error: {str(e)} line {sys.exc_info()[-1].tb_lineno}, check requirements.txt")
        sys.exit(1)


if __name__ == '__main__':
    run_mqttwatch()
