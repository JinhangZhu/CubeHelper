# -*- coding: utf-8 -*-
# @Time     : 2021/7/18 23:29
# @Author   : Jinhang
# @File     : main.py

from PyQt5.QtWidgets import QApplication
from RunDictator import MainPanel
import logging

if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s  - %(levelname)s - %(message)s')

    app = QApplication(sys.argv)
    main_panel = MainPanel()
    main_panel.show()
    sys.exit(app.exec_())
