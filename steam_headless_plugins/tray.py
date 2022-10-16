#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.tray.py

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
import argparse
import logging
import os
import webbrowser

import psutil

from pystray import MenuItem as item
import pystray
from PIL import Image

from . import common

logger = logging.getLogger('tray')


class LauncherTray:

    def __init__(self, silent=False):
        self.silent = silent
        self.icon = None
        self.other_procs = {}

        self.ui_thread = None

    @staticmethod
    def __terminate_proc_tree(proc: psutil.Process):
        """
        Terminate the process tree (including grandchildren).
        Processes that fail to stop with SIGTERM will be sent a SIGKILL.

        :param proc:
        :return:
        """
        try:
            children = proc.children(recursive=True)
            children.append(proc)
        except psutil.NoSuchProcess:
            return
        for p in children:
            try:
                p.terminate()
            except psutil.NoSuchProcess:
                pass
        gone, alive = psutil.wait_procs(children, timeout=3)
        for p in alive:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
        psutil.wait_procs(alive, timeout=3)

    def display_gui(self):
        """Display the main GUI"""
        if not self.other_procs.get('gui'):
            proc, sp = common.exec_python_module_process(['steam_headless_plugins', 'gui'])
            self.other_procs['gui'] = proc
            return
        # TODO: Add logging - "GUI already open."
        logger.warning("Unable to open GUI. GUI already open.")

    def display_about(self):
        """Display the updater window"""
        pass

    def stop_other_processes(self):
        """Terminate all other processes that may still be running"""
        for proc in self.other_procs:
            self.__terminate_proc_tree(self.other_procs.get(proc))

    def action_exit(self):
        self.icon.visible = False
        self.icon.stop()

    def create_icon_menu(self):
        return pystray.Menu(
            item('Display GUI', self.display_gui),
            # item('About', self.display_about),
            pystray.Menu.SEPARATOR,
            item('Exit', self.action_exit)
        )

    def create_icon(self):
        # When installed, the icon will be up a level
        image = None
        if os.path.exists(os.path.join(common.module_root, 'assets', 'icon.ico')):
            # When running from this script
            image = Image.open(os.path.join(common.module_root, 'assets', 'icon.ico'))
        menu = self.create_icon_menu()
        self.icon = pystray.Icon("Steam Headless Plugins", image, "Steam Headless Plugins", menu)

    def setup(self):
        # Create icon
        self.create_icon()

    def stop(self):
        # Stop all subprocesses and threads
        self.stop_other_processes()

    def run(self):
        # Setup main process
        self.setup()
        # Create tray icon. This must be run last
        self.icon.run()
        # Stop everything
        self.stop()


def main():
    parser = argparse.ArgumentParser(description='Steam Headless Plugins')
    parser.add_argument('--gui', action='store_true',
                        help='Start GUI mode.')
    parser.add_argument('--silent', action='store_true',
                        help='Start in tray only. Do not display the main UI on startup.')
    args = parser.parse_args()

    launcher = LauncherTray(silent=args.silent)
    launcher.run()
