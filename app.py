#!/usr/bin/env python3
# -*- coding: utf-8 -*-


## -------------------------------------------------------
## simple testcase for ring-mqtt
## @call:  python3 app.py -l DEBUG
## -------------------------------------------------------

from os import sys, path
sys.path.append(path.dirname(path.abspath(__file__)))


"""simple check if python 3 is used"""
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

try:
    import argparse
    import time
    from datetime import datetime
    import json
    import paho.mqtt.client as paho

except Exception as e:
    print(f"Import error: {str(e)} line {sys.exc_info()[-1].tb_lineno}, check requirements.txt")
    sys.exit(1)

try:
    from lib import logger
    import config

except Exception as e:
    print('Application Configuration error {}, check config.py'.format(e))
    sys.exit(1)

"""the application logger"""
log = logger.Log(__name__)


def setLogger(args: list = "Info"):
    """ set logger"""
    if args:
        logging_argparse = argparse.ArgumentParser(
            prog=__file__, add_help=False)
        logging_argparse.add_argument('-l', '--log-level', default='NONE', help='set log level')
        logging_args, _ = logging_argparse.parse_known_args(args)
        config.LOGGER_LEVEL_SET = logging_args.log_level
        try:
            if not logging_args.log_level in log.LOGLEVELMAP or logging_args.log_level == "NONE":
                log.loglevel = log.LOGLEVELMAP["NOLOG"]
                log.setLoglevel(level=log.LOGLEVELMAP["NOLOG"])
            else:
                log.loglevel = log.LOGLEVELMAP[logging_args.log_level]
                log.setLoglevel(level=log.LOGLEVELMAP[logging_args.log_level])

            config.LOGGER_LEVEL = log.loglevel
            print("Loglevel", config.LOGGER_LEVEL_SET,
                  logging_args.log_level, config.LOGGER_LEVEL)
            log.info("Logger Loglevel:{}".format(config.LOGGER_LEVEL))

        except ValueError:
            log.error("Invalid log level: {}".format(logging_args.log_level))
            sys.exit(1)

def saveinfo(topic:str="", message:str=""):
    try:
        with open("logs/ring_mqtt.txt", "a+") as file_object:
            file_object.write("{}\t{}: {}\n".format(time.strftime("%Y%m%d-%H%M%S"),topic, message))
    except BaseException as e:
        print(
            f"Error {__package__}:{__name__}.{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")

def on_message(client, userdata, message):
    log.info("Topic: {}".format(message.topic))
    try:
        if (message.topic == config.RING_MOTION):
            log.info("Motion topic: {}".format(message.payload))
            saveinfo("MOTION", message.payload)

        if (message.topic == config.RING_TIME):
            log.info("Ring time topic: {}".format(message.payload))
            data = json.loads(message.payload)
            saveinfo("TIMESTAMP", datetime.fromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S.%f'))

        if (message.topic == config.RING_IMAGE):
            filename = time.strftime("images/image_%Y%m%d-%H%M%S.jpg")
            saveinfo("IMAGE",filename)
            save_payload(message.payload, filename)
    except BaseException as e:
        print(
            f"Error {__package__}:{__name__}.{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")


def save_payload(payload, filename):
    try:
        print("Saving file: " + filename)
        log.info("Filename: {}".format(filename))
        f = open(filename, "wb")
        f.write(payload)
        f.close()
    except BaseException as e:
        print(
            f"Error {__package__}:{__name__}.{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return False


def run_mqttwatch():
    try:
        log.info("Start mqtt watch")
        c = paho.Client()
        c.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
        c.connect(config.MQTT_HOST, config.MQTT_PORT,keepalive=config.MQTT_KEEPALIVE)
        c.subscribe(config.RING_IMAGE)
        c.subscribe(config.RING_TIME)
        c.subscribe(config.RING_MOTION)
        c.on_message = on_message
        c.loop_forever()
    except BaseException as e:
        print(f"Application error: {str(e)} line {sys.exc_info()[-1].tb_lineno}, check requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    setLogger(sys.argv[1:])
    run_mqttwatch()
