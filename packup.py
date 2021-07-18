# -*- coding: utf-8 -*-
# @Time     : 2021/7/19 0:53
# @Author   : Jinhang
# @File     : packup.py


import os

os.system("pyinstaller main.py -F -i resource/icon.ico --distpath CubeHelper -n CubeHelper")