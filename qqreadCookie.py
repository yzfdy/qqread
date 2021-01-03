# -*- coding: utf-8 -*-
# @Time    : 2020-12-10
# @Author  : water008@github
# @File    : qqreadCookie.py

import requests
import json
import time
import os
import re
import ast
import notification


####################################
# 方案2 GitHub action 自动运行    各参数读取自secrets


if "QQREADHEADERS" and "QQREADBODYS" and "QQREADTIMEURL" in os.environ:
    qqreadheaders = os.environ["QQREADHEADERS"].split('\n')
    qqreadbodys = os.environ["QQREADBODYS"].split('\n')
    qqreadtimeurl = os.environ["QQREADTIMEURL"].split('\n')
    qqreadLists = []
    if len(qqreadheaders) == len(qqreadbodys) and len(qqreadbodys) == len(qqreadtimeurl):
        qqreadLists = list(
            zip(qqreadheaders, qqreadbodys, qqreadtimeurl))
    else:
        print("各项Secrets数量不符，请修改！")
    


#######################################


def valid(qqheaders):
    headers = ast.literal_eval(qqheaders[0])
    response = requests.get(
        'https://mqqapi.reader.qq.com/mqq/user/init', headers=headers)
    if response.json()["data"]['isLogin'] == False:
        QQNUM = re.findall(r'ywguid=(.*?);ywkey', headers['Cookie'])[0]
        print(f"""## {QQNUM}: headers过期""")
        notification.notify(
            f"""## QQ账号【{QQNUM}】 headers过期""", f"""## 账号【{QQNUM}】 headers过期 ，及时修改""")
        return False
    return True


def get_cookies():
    return [i for i in qqreadLists if valid(i)]


if __name__ == "__main__":
    print(">>>检查有效性")
    for i in get_cookies():
        print(i)
