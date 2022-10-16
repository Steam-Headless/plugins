#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.common.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     16 Oct 2022, (3:28 PM)

    Copyright:
           Copyright (C) Josh Sunnex - All Rights Reserved

           THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
           EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
           MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
           IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
           DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
           OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
           OR OTHER DEALINGS IN THE SOFTWARE.

"""
import json
import logging
import os
import shutil
import subprocess

import psutil

logging_format = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=logging_format)

module_root = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
# Set path to Python executable
if os.name == "nt":
    python_exe = os.path.join(project_root, 'Python', 'python.exe')
else:
    python_exe = shutil.which("python")

all_services = {
    "sunshine": {
        "name":  "Sunshine",
        "multi": False,
    },
    "steam":    {
        "name":  "Additional Steam Installations",
        "multi": True,
    },
}
default_config = {
    "services": {
        "sunshine": {
            "enabled": False,
        },
        "steam":    {
            "enabled": False,
        },
    },
}


def get_home_dir():
    return os.path.expanduser("~")


def get_config_path():
    config_path = os.path.join(get_home_dir(), '.config', 'steam-headless', 'plugins')
    # Ensure the config path exists
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    return config_path


def read_config():
    """
    Read the config from a JSON file
    :return:
    """
    config_path = get_config_path()
    settings_file = os.path.join(config_path, 'settings.json')
    data = {}
    if os.path.exists(settings_file):
        with open(settings_file) as infile:
            data = json.load(infile)
    return {**default_config, **data}


def write_config(data: dict):
    """
    Write the config out to a JSON file
    :param data:
    :return:
    """
    config_path = get_config_path()
    settings_file = os.path.join(config_path, 'settings.json')
    with open(settings_file, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)


def exec_process(subprocess_command: list):
    """
    Start a subprocess and return the psutil Process object

    :param subprocess_command:
    :return:
    """
    subprocess_kwargs = {}
    if os.name == "nt":
        # For Windows, prevent the subprocess opening its own terminal
        si = subprocess.STARTUPINFO()
        # si.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess_kwargs = {
            'shell':       True,
            'startupinfo': si,
        }
        # creation_flags= subprocess.CREATE_NO_WINDOW
    new_process = subprocess.Popen(subprocess_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       universal_newlines=True, errors='replace',
                                       **subprocess_kwargs)
    # Fetch process using psutil for control (sending SIGSTOP on Windows will not work)
    return psutil.Process(pid=new_process.pid), new_process


def exec_python_module_process(module_command: list):
    """
    Start a python subprocess

    :param module_command:
    :return:
    """
    subprocess_command = [python_exe, '-m'] + module_command
    proc, sp = exec_process(subprocess_command)
    return proc, sp
