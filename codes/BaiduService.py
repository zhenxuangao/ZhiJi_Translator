# -*- coding: utf-8 -*-

# 注意：当前百度翻译服务仅能自动检测待翻译语言并将其翻译为中文。
# 如需其他语言组合，请修改 from_lang 和 to_lang 参数。

import requests
import random
import json
from hashlib import md5

def translate(query):
    # 从配置文件中读取百度翻译 API 设置
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    # 设置您的appid/appkey
    appid = config['baidu']['appid']
    appkey = config['baidu']['appkey']

    # 语言代码，请参考 `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'auto'
    to_lang = 'zh'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    # 生成salt和sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # 构建请求
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # 发送请求
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # 获取翻译结果
    if 'trans_result' in result:
        translated_text = ''
        for item in result['trans_result']:
            translated_text += item['dst'] + '\n' + '\n'
        return translated_text.strip()
    else:
        return f'翻译失败，错误信息:\n{json.dumps(result, indent=4, ensure_ascii=False)}'

# 使用示例
if __name__ == '__main__':
    query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'
    result = translate(query)
    print(result)