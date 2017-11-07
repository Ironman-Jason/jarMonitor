#!/usr/bin/env python
#coding=utf-8


import os
import sys
import subprocess
from subprocess import check_output
from subprocess import CalledProcessError
from time import sleep

import logging
import json

CONF_FILE = 'conf.json'
NAME = 'java'
LOG_FILE = 'jarMonitor.log'
lOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s %(message)s'
POLL_INTERVAL = 5

def init_logger():
    logging.basicConfig(filename=LOG_FILE, level=lOG_LEVEL, format=LOG_FORMAT)
    logging.debug('Start java app monitoring.')


def load_data_from_conf():
    try:
        with open(CONF_FILE) as conf:
            data = json.load(conf)
    except IOError as e:
        print("Cannot find config file, Monitor will exit.")
        return None
    except ValueError as e:
        print ("Wrong conf file. Monitor will exit.")
        return None

    global LOG_FILE
    global POLL_INTERVAL
    try:
        LOG_FILE = data["log_file"]
        POLL_INTERVAL = data["polling_interval"]
    except KeyError as e:
        print("Use default log file: jarMonitor.log and default polling interval: 5 seconds.")
    return data


def get_runtime_jar_process_id():
    try:
        list = check_output(["pidof", NAME]).split()
    except CalledProcessError as e:
        logging.error("Cannot find JVM running out there.")
        return None
    return list


def is_process_down(app_name):
    process = get_runtime_jar_process_id()
    if process is None:
        sys.exit(0)

    is_down = True 
    for id in process:
        is_alive = is_process_match_with_app(id=id, app_name=app_name)
        if is_alive is True:
            is_down = False
            logging.info(app_name + " is alive!")
            break

    logging.debug("is process down return: " + str(is_down));
    return is_down


def is_process_match_with_app(id, app_name):
    logging.debug("checking with id:" + id + "app: " + app_name)
    try:
        with open('/proc/{}/cmdline'.format(id), mode='rb') as fd:
            contents = fd.read().decode().split('\x00')
            for item in contents:
                logging.debug("item: " + item);
                if item.find(app_name) is not -1:
                    logging.debug("is process match with id and app_name return True");
                    return True
    except Exception:
        return False

    logging.debug("is process match with id and app_name return False");
    return False


def pull_up_app(cwd, app_name):
    jar_file = cwd + app_name
    logging.info('Pull up app: ' + cwd + app_name)
    subprocess.call(['java', '-jar', jar_file])


def start_monitoring():
    init_logger()
    while(True):
        sleep(POLL_INTERVAL)
        conf = load_data_from_conf()
        try:
            app_list = conf["apps"]
            is_actvivated = conf["activated"]
        except KeyError as e:
            continue

        if is_actvivated is False:
            logging.info('monitor is standby due to the activated is false')
            continue

        for app in app_list:
            try:
                cwd = app["cwd"]
                app_name = app["name"]
                logging.debug('Start checking ' + app_name + " in" + cwd)
                if is_process_down(app_name=app_name) is True:
                   pull_up_app(cwd=cwd, app_name=app_name)
            except KeyError as e:
                logging.error('key error from app "cwd" and "name"')
                continue


if __name__ == '__main__':
    start_monitoring()
