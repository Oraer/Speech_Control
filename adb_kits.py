# -*- coding: utf-8 -*-
# Copyright (C) 2023 # @version
# @Time    : 2023/6/24 23:00
# @Author  : Oraer
# @File    : adb_kits.py
#   _*_ coding:utf-8 _*_
import os
import time
import cv2
import pyautogui

"""
# 获取当前界面的应用包名和Activity
adb shell dumpsys window w |findstr \/ |findstr name=

"""


def execute(cmd):
    adb_str = 'adb shell {}'.format(cmd)
    print(adb_str)
    os.system(adb_str)


def unlock_phone(code="123456"):
    # 开启电源键
    execute('input keyevent 26')
    # 滑动屏幕进入输入密码界面
    execute('input swipe 100 600 100 100  300')
    time.sleep(1)
    # 输入密码
    execute('input text {}'.format(code))
    time.sleep(1)
    print("手机解锁成功...")


def open_app(package, activity):
    execute('am start -n {}/{}'.format(package, activity))


def open_salt():
    open_app('com.salt.music', 'com.salt.music.ui.MainActivity')
    time.sleep(1)
    execute("input tap 204 2193")
    execute('input keyevent KEYCODE_MEDIA_PLAY')    # 播放
    execute('input keyevent KEYCODE_VOLUME_DOWN')   # 音量-
    execute('input keyevent KEYCODE_VOLUME_UP')     # 音量+
    print("已打开...")


def get_screen():
    execute("screencap -p /sdcard/Afile/screen.png")
    cur_dir = os.path.dirname(os.path.abspath(__file__)) + "\images"
    os.system("adb pull /sdcard/Afile/screen.png {}".format(cur_dir))
    img = cv2.imread(cur_dir + "\screen.png")
    width, height = img.shape[:2]
    print(height, width)
    img = cv2.resize(img, (int(height/3.5), int(width/3.5)), interpolation=cv2.INTER_CUBIC)
    cv2.imshow("screen", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def adb_control(result_out):
    if "解锁" in result_out or "解锁手机" in result_out:
        code = '123456'
        unlock_phone(code)
    elif "打开椒盐音乐" in result_out or "打开音乐" in result_out:
        open_salt()
    elif "暂停音乐" in result_out or "暂停" in result_out:
        execute('input keyevent KEYCODE_MEDIA_PAUSE')  # 暂停
    elif "播放音乐" in result_out or "播放" in result_out:
        execute('input keyevent KEYCODE_MEDIA_PLAY')   # 播放
    elif "返回" in result_out:
        print("返回...")
        execute("input keyevent 4")
    elif "主页" in result_out:
        print("主页...")
        execute("input keyevent 3")
    elif "上滑" in result_out:
        print("上滑...")
        execute("input swipe 100 1000 100 100  300")
    elif "下滑" in result_out:
        print("下滑...")
        execute("input swipe 100 100 100 1000  300")
    elif "左滑" in result_out:
        print("左滑...")
        execute("input swipe 1000 1000 100 1000  300")
    elif "右滑" in result_out:
        print("右滑...")
        execute("input swipe 100 1000 1000 1000  300")
    elif "截屏" in result_out:
        print("截屏...")
        get_screen()
    elif "锁屏" in result_out:
        print("锁屏...")
        execute("input keyevent 26")
        print("锁屏成功...")
    else:
        pass
    return None


def main():
    unlock_phone(code='123456')   # 解锁手机 code 你的解锁密码
    # com.salt.music/com.salt.music.ui.MainActivity
    open_app('com.salt.music', 'com.salt.music.ui.MainActivity')
    execute("input tap 204 2193")     # 点击详细信息
    # execute('input keyevent KEYCODE_MEDIA_STOP')      # 停止播放
    # execute('input keyevent KEYCODE_MEDIA_PAUSE')    # 暂停
    # execute('input keyevent KEYCODE_MEDIA_PLAY')      # 播放
    # execute('input keyevent KEYCODE_MEDIA_NEXT')      # 下一首
    # execute('input keyevent KEYCODE_MEDIA_PREVIOUS')  # 上一首
    execute('input keyevent KEYCODE_VOLUME_UP')       # 音量+
    execute('input keyevent KEYCODE_VOLUME_DOWN')     # 音量-

if __name__ == '__main__':
    # main()
    print(os.path.dirname(os.path.abspath(__file__)) + "\images")