# -*- coding: utf-8 -*-
# Copyright (C) 2023 # @version
# @Time    : 2023/6/20 9:56
# @Author  : Oraer
# @File    : main.py
import os
import time
import socket
import sys
import pyautogui
import pyperclip
import playsound

from toolkit import write_audio
from toolkit import GetAudioContent       # 语音识别
from toolkit import speech_read           # 简单语音播报
from toolkit import search_web            # 搜索
from toolkit import get_weather           # 天气
from toolkit import translate             # 翻译
from toolkit import get_top_news_list     # 热搜排行榜
from toolkit import get_daily_sentence    # 每日一句
from ChatGPT import ChatGPT               # ChatGPT 闲聊模块
from adb_kits import adb_control          # 控制手机

# playsound.playsound("./audio/***.wav") 会报错，你需要替换成你自己的音频。如果不用，当然也可以注释掉

if __name__ == '__main__':
    path = './audio/test.wav'         # 临时存储音频文件
    is_wakeup = False                 # 是否唤醒
    is_chat = False                   # 是否进入聊天模式
    chat = None                       # ChatGPT 闲聊模块
    is_phone = False                  # 是否控制手机
    is_tcp = False                    # 是否使用TCP连接
    sock = None
    print("欢迎使用小江语音助手...")
    print("请说出唤醒词：小江小江")
    playsound.playsound("./audio/welcome.wav")
    playsound.playsound("./audio/wakeup_word.wav")
    while True:
        print('-' * 30)

        # -----------------------------
        # 录音方法
        write_audio(path, 1)    # 录音
        # 获取录音文件内容并进行识别
        with open(path, 'rb') as f:
            audio_data = f.read()
        # -----------------------------

        sign, result_out = GetAudioContent(audio_data)  # sign=1表示识别成功，result_out为识别结果

        if sign == 1:
            # 识别成功
            # 唤醒词识别
            if is_wakeup is False:
                print("等待唤醒...(唤醒词为：小江小江)")
                print("you say: ", result_out)
                if "小江" in result_out:
                    is_wakeup = True
                    print("唤醒成功...")
                    # speech_read("我在呢")
                    playsound.playsound("./audio/I_am_here.wav")
            else:
                # 唤醒成功 正常识别
                # 退出指令
                print("you say: ", result_out)
                if "结束" in result_out or "再见" in result_out or "退出唤醒" in result_out:
                    print("退出成功...")
                    # print("请重新运行...")
                    playsound.playsound("./audio/out_success.wav")
                    # playsound.playsound("./audio/reset.wav")
                    break

                # -----------------------------
                # Chat聊天模块
                if is_chat is False and ("聊天" in result_out or "闲聊" in result_out or "进入聊天模式" in result_out):
                    print("进入聊天模式...")
                    playsound.playsound("./audio/chat_in.wav")
                    # speech_read("进入聊天模式")
                    is_chat = True
                    chat = ChatGPT("user")
                    # send_keys('^+{TAB}')             # 启动 CFW
                if is_chat is True:
                    if "退出聊天" in result_out or "退出闲聊" in result_out:
                        print("退出聊天模式...")
                        playsound.playsound("./audio/chat_out.wav")
                        # speech_read("退出聊天模式")
                        is_chat = False
                        chat.writeTojson()
                        # send_keys('^+{TAB}')         # 停止 CFW
                        continue
                    print("等待回答...")
                    # playsound.playsound("./audio/chat_wait.wav")
                    chat.messages.append({"role": "user", "content": result_out})
                    try:
                        answer = chat.ask_gpt()
                        print("[answer]: ", answer)
                        chat.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        print(f"错误代码：{e}")
                        is_chat = False
                        print("Oops! 由于不可抗力等原因，聊天模式退出...")
                        playsound.playsound("./audio/chat_error.wav")
                        print("如果想要继续使用Chat，请重新进入聊天模式...")
                    continue
                # -----------------------------

                # -----------------------------
                # 控制手机模块
                """
                通过ADB进行电脑与手机间的通讯
                """
                if is_phone is False and ("控制手机" in result_out or "进入控制手机模式" in result_out):
                    print("进入控制手机模式...")
                    playsound.playsound("./audio/control_phone.wav")
                    # speech_read("进入控制手机模式")
                    is_phone = True
                    continue
                if is_phone is True:
                    if "退出手机" in result_out or "退出控制手机" in result_out:
                        print("退出控制手机...")
                        playsound.playsound("./audio/phone_out.wav")
                        # speech_read("退出控制手机")
                        is_phone = False
                        continue
                    adb_control(result_out)
                    continue
                # -----------------------------

                # -----------------------------
                # Sockect模块
                """
                通过Socket进行电脑之间通讯
                """
                if is_tcp is False and ("TCP" in result_out or "tcp" in result_out or "进入TCP模式" in result_out):
                    print("进入tcp模式...")
                    playsound.playsound("./audio/tcp_in.wav")
                    # speech_read("进入tcp模式")
                    is_tcp = True
                    IP = '192.168.51.175'  # 服务器的ip地址
                    port = 4004  # 服务器的端口号
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        sock.connect((IP, port))
                    except Exception as e:
                        print('服务器端未找到或未打开')
                        playsound.playsound("./audio/tcp_error.wav")
                        # sys.exit()
                        continue
                    continue
                if is_tcp is True:
                    if "退出TCP" in result_out or "退出TCP模式" in result_out:
                        print("退出tcp模式...")
                        playsound.playsound("./audio/tcp_out.wav")
                        # speech_read("退出tcp模式")
                        is_tcp = False
                        try:
                            sock.send("exit".encode('utf-8'))
                            sock.close()
                        except Exception as e:
                            print("服务器端已关闭")
                        continue
                    sock.send(result_out.encode('utf-8'))
                    continue
                # -----------------------------

                # -----------------------------
                # 各种操作指令
                """
                开始各种指令的识别
                """
                # 浏览器搜索
                if "搜索" in result_out:
                    query = result_out.replace('搜索', '')
                    query = query.replace('。', '')
                    search_web(query)
                elif "翻译" in result_out:
                    query = result_out.replace('翻译', '')
                    result = translate(query)
                    print("翻译结果: ", result)
                    speech_read(result)
                elif "天气" in result_out or "天气如何" in result_out:
                    # location = "Changsha,CN"
                    weather = get_weather()
                    print(weather)
                    speech_read(weather)
                elif "每日一句" in result_out:
                    temp = get_daily_sentence()
                    print(temp)
                    speech_read(temp)
                elif "置顶热搜" in result_out or "每日热搜" in result_out or "热搜" in result_out:
                    print("置顶热搜：")
                    print(get_top_news_list())
                elif "时间" in result_out or "几点" in result_out:
                    import time
                    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print(time_now)
                    speech_read(time_now)
                elif "打开记事本" in result_out:
                    os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Notepad.lnk")
                    playsound.playsound("./audio/open_notepad.wav")
                    # speech_read("已打开记事本")
                elif "输入" in result_out:
                    pyperclip.copy(result_out.split('输入')[1])
                    pyautogui.hotkey('ctrl', 'v')
                elif "关闭记事本" in result_out:
                    pyautogui.hotkey('alt', 'f4')
                    # 模拟键盘 右方向
                    pyautogui.press("right")
                    pyautogui.press("enter")
                    playsound.playsound("./audio/close.wav")
                elif "打开网易云音乐" in result_out or "打开网易云" in result_out:
                    os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\网易云音乐.lnk")
                    # speech_read("已打开网易云音乐")
                    time.sleep(3)
                    playsound.playsound("./audio/open_netease.wav")
                    pyautogui.press("space")
                elif "关闭网易云音乐" in result_out or "关闭网易云" in result_out:
                    pyautogui.hotkey('alt', 'f4')
                    time.sleep(1)
                    pyautogui.press("enter")
                    playsound.playsound("./audio/close.wav")
                elif "关闭网页" in result_out:
                    pyautogui.hotkey('ctrl', 'w')
                    playsound.playsound("./audio/close.wav")
                    import win32gui
                    import win32con
                    # 获取活动窗口的句柄
                    hwnd = win32gui.GetForegroundWindow()
                    # 最小化窗口
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                elif "关闭" in result_out:
                    pyautogui.hotkey('alt', 'f4')
                    playsound.playsound("./audio/close.wav")
                    # speech_read("已关闭")
                else:
                    print("未知指令, 请再说一遍")
                    playsound.playsound("./audio/unknown_cmd.wav")
                    pass
                # print("-"*30)
        else:
            # 识别失败
            print("识别失败, 请再说一遍")
            if not is_wakeup:
                print("请先唤醒")
            playsound.playsound("./audio/error.wav")
            # print("-"*30)
