#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from .tray import main


def run():
    if 'gui' in sys.argv:
        print("HERE")
        print(sys.argv)
        from .config_window import show_window
        show_window()
        return
    main()


if __name__ == "__main__":
    run()
