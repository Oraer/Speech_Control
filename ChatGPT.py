# -*- coding: utf-8 -*-
# Copyright (C) 2023 # @version
# @Time    : 2023/6/25 10:26
# @Author  : Oraer
# @File    : ChatGPT.py
import openai
import json
import os

# 设置代理
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"


# 获取 api
def get_api_key():
    # 可以自己根据自己实际情况实现
    # 以我为例子，我是存在一个 openai_key 文件里，json 格式
    '''
    {"api": "你的 api keys"}
    '''
    openai_key_file = './openai_key.json'
    with open(openai_key_file, 'r', encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']


# openai.api_key = get_api_key()
openai.api_key = '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'


class ChatGPT:
    def __init__(self, user):
        # 类实体化时，才执行代理设置

        self.user = user
        self.messages = [{"role": "user", "content": "一个有10年Python开发经验的资深算法工程师"}]
        self.filename = "./config/user_messages.json"

    def ask_gpt(self):
        # q = "用python实现：提示手动输入3个不同的3位数区间，输入结束后计算这3个区间的交集，并输出结果区间"
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return rsp.get("choices")[0]["message"]["content"]

    def writeTojson(self):
        try:
            # 判断文件是否存在
            if not os.path.exists(self.filename):
                with open(self.filename, "w") as f:
                    # 创建文件
                    pass
            # 读取
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                msgs = json.loads(content) if len(content) > 0 else {}

            # 追加
            msgs.update({self.user: self.messages})

            # 写入
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(msgs, f)

        except Exception as e:
            print(f"错误代码：{e}")


def Multi_Round_Dialogue(chat=None, is_chat=False, result_out=None):
    """
    temp
    多轮对话
    Args:
        chat:
        is_chat:
        result_out:

    Returns:

    """
    if is_chat is True:
        if "退出闲聊" in result_out or "退出聊天" in result_out:
            print("退出聊天模式...")
            is_chat = False
            chat.writeTojson()
            return is_chat
        print("等待回答...")
        chat.messages.append({"role": "user", "content": result_out})
        try:
            answer = chat.ask_gpt()
            print("answer: ", answer)
            chat.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            print(f"错误代码：{e}")
            is_chat = False
            print("Oops! 由于不可抗力等原因，聊天模式退出...")
            print("如果想要继续使用Chat模式，请重新进入聊天模式...")
    return is_chat


def main():
    user = input("请输入用户名称: ")
    chat = ChatGPT(user)

    print("-----------------------------")
    print("---------开始对话----------")
    print("0 - 退出程序\n1 - 重置对话")
    print("-----------------------------")

    # 循环
    while 1:
        # 限制对话次数
        if len(chat.messages) >= 30:
            print("---------ChatGPT3.5-----------")
            print("---------强制重置对话----------")
            print("------------------------------")
            # 写入之前信息
            chat.writeTojson()
            user = input("请输入用户名称: ")
            chat = ChatGPT(user)

        # 提问
        q = input(f"\n[{chat.user}]Prompt：")

        # 逻辑判断
        if q == "0" or q == "quit":
            print("---------退出程序----------")
            # 写入之前信息
            chat.writeTojson()
            break
        elif q == "1":
            print("--------------------------")
            print("---------重置对话----------")
            print("--------------------------")
            # 写入之前信息
            chat.writeTojson()
            user = input("请输入用户名称: ")
            chat = ChatGPT(user)
            continue

        # 提问-回答-记录
        chat.messages.append({"role": "user", "content": q})
        answer = chat.ask_gpt()
        #         print(f"\n[Prompt]{q}")
        print(f"\n[Answer]{answer}")
        chat.messages.append({"role": "assistant", "content": answer})


if __name__ == '__main__':
    main()
