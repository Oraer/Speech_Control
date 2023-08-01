import os
import pyaudio
import wave
from aip import AipSpeech
import pyttsx3
import webbrowser
import requests
import json

# import soundfile as sf
# import numpy as np
# from scipy.io import wavfile
#
# from SpeechEnh import *


# 声音录制设置
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16位深
CHANNELS = 1  # 1是单声道，2是双声道。
RATE = 16000  # 采样率，调用API一般为8000或16000
RECORD_SECONDS = 6  # 录制时间6s


# 录音文件保存路径
def save_wave_file(pa, filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(data))
    wf.close()


# 录音主体文件
def write_audio(filepath, isstart):
    """
    :param filepath:文件存储路径（'test.wav'）
    :param isstart: 录音启动开关（0：关闭 1：开启）
    """
    if isstart == 1:
        print("start recording...")
        pa = pyaudio.PyAudio()
        stream = pa.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK)

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)  # 读取chunk个字节 保存到data中
            frames.append(data)  # 向列表frames中添加数据data

        stream.stop_stream()
        stream.close()  # 停止数据流
        pa.terminate()  # 关闭PyAudio

        # 写入录音文件
        save_wave_file(pa, filepath, frames)

        # # 报错： AttributeError: module 'numpy' has no attribute 'complex'.
        # # 原因：numpy版本过高
        # # 或者注释以下代码
        # # 将录音数据保存为.wav文件
        # (fs, data) = wavfile.read(filepath)
        #
        # data = data - np.mean(data)
        # data = data / np.max(np.abs(data))  # 幅值归一化
        # IS = 0.25  # 设置前导无话段长度
        # wlen = 200  # 设置帧长为25ms
        # inc = 80  # 设置帧移为10ms
        # SNR = 5  # 设置信噪比SNR
        # N = len(data)  # 信号长度
        # time = [i / fs for i in range(N)]  # 设置时间
        # signal = awgn(data, SNR)  # 叠加噪声
        # NIS = int((IS * fs - wlen) // inc + 1)  # 求前导无话段帧数
        #
        # snr1 = SNR_Calc(data, signal)  # 计算初始信噪比
        # a, b = 4, 0.001
        # output = SpectralSub(signal, wlen, inc, NIS, a, b)  # 谱减法降噪
        #
        # # 将降噪后的数据保存为.wav文件
        # sf.write(filepath, output, fs)

    elif isstart == 0:
        exit()


def get_audio_data():
    pass


# 获取录音文件内容并进行识别
def GetAudioContent(content):
    """
    # :param filename:录音文件路径
    :param content:录音文件内容
    :return: sign-是否获得结果，result_out-返回录音内容
    """
    # 百度语音识别API Key， 请更换为你自己的 API key
    APP_ID = '33278035'
    API_KEY = 'rhbZqV6ep4lAYGnkRRcuDTGE'
    SECRET_KEY = '6bKTez79pUZGFX1POgClDHteNAG3Ken7'

    dirs = "./audio/"
    if not os.path.exists(dirs):
        print("audio文件夹不存在,已自动创建audio文件夹")
        os.makedirs(dirs)

    # 读取录音文件内容
    # with open(filename, 'rb') as f:
    #     content = f.read()

    # 调用Baidu-api实现语音识别
    sign = 1    # 识别成功标志
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.asr(content, 'wav', 16000, {'dev_pid': 1537, })
    # print(result)
    if 'result' not in result.keys():
        sign = 0
        result_out = None
    elif result['result'] == ['']:
        sign = 0
        result_out = None
    else:
        result_out = "".join(result['result'])
    return [sign, result_out]


# 语音播报函数
def speech_read(content):
    """
    :param content:待播报的字符串
    :return: None
    """
    # 模块初始化
    engine = pyttsx3.init()
    engine.say(content)
    # 等待语音播报完毕
    engine.runAndWait()


def search_web(query):
    # url = f"https://www.google.com/search?q={query}"
    # url = f"https://www.baidu.com/s?wd={query}"
    url = f"https://bing.com/search?q={query}"
    webbrowser.open(url)


def translate(query, from_lang='zh', to_lang='en'):
    # 初始化翻译客户端
    from translate import Translator
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    result = translator.translate(query)
    return result


def get_weather2(location="Changsha,CN"):
    # 初始化天气客户端
    from pyowm import OWM
    owm = OWM('4685a2921b74cda6f2ebca3a83d05d0b')  # 可以更换为你自己的API Key
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(location)
    weather = observation.weather
    temperature = weather.temperature('celsius')['temp']
    status = weather.status
    return f"{location}的天气是{status}, 温度为{temperature}摄氏度"


def get_weather():
    """
    获取天气信息
    更加详细的获取天气信息
    Returns:

    """
    url = "http://d1.weather.com.cn/sk_2d/101250101.html?_=1687950308754"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
              'Referer': 'http://www.weather.com.cn/weather1d/101010100.shtml',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              'Connection': 'keep-alive',
              'Cookie': 'Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1687950268; f_city=%E5%8C%97%E4%BA%AC%7C101010100%7C; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1687950287'}
    requests_url = requests.get(url, headers=header)
    message = json.loads(requests_url.text.encode("latin1").decode("utf8").replace("var dataSK=", ""))
    cityname = message['cityname']
    aqi = int(message['aqi'])
    sd = message['sd']
    wd = message['WD']
    ws = message['WS']
    temp = message['temp']
    weather = message['weather']
    if aqi <= 50:
        airQuality = "优"
    elif aqi <= 100:
        airQuality = "良"
    elif aqi <= 150:
        airQuality = "轻度污染"
    elif aqi <= 200:
        airQuality = "中度污染"
    elif aqi <= 300:
        airQuality = "重度污染"
    else:
        airQuality = "严重污染"
    return cityname + " " + '今日天气：' + weather + ' 温度：' + temp + ' 摄氏度 ' + wd + ws + ' 相对湿度：' + sd + ' 空气质量：' \
           + str(aqi) + "（" + airQuality + "）"


def get_top_news_list():
    # 百度热搜榜地址
    url = 'https://top.baidu.com/api/board?platform=wise&tab=realtime'
    # 构造请求头
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36',
        'Host': 'top.baidu.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://top.baidu.com/board?tab=novel',
    }
    # 发送请求
    r = requests.get(url, header)
    # 用json格式接收请求数据
    json_data = r.json()
    # 爬取置顶热搜
    pin_content_list = json_data['data']['cards'][0]['topContent']
    pin_title = pin_content_list[0]['query']
    # 爬取普通热搜
    top_content_list = json_data['data']['cards'][0]['content']
    top_title_list = [one['query'] for one in top_content_list]
    # 拼接 置顶热搜和普通热搜
    top_list = [pin_title] + top_title_list
    # 将列表转换为字符串
    top_list = '\n'.join(top_list[:10])
    # print("置顶热搜：")
    # print(top_list)
    return top_list


def get_daily_sentence():
    """
    获取每日一句
    Returns:

    """
    url = "http://open.iciba.com/dsapi/"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        }
    r = requests.get(url, headers=header)
    r = json.loads(r.text)
    content = r["content"]
    note = r["note"]
    daily_sentence = content + "\n" + note
    return daily_sentence

