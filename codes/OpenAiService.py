import requests
import json

def translate(query):
    # 从配置文件中读取 OpenAI API 设置
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
    # OpenAI API 中转地址
    api_url = config['openai']['api_url']
    
    # 设置 API 密钥
    api_key = config['openai']['api_key']
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 构建请求体
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "你是一个翻译助手。请将用户输入的文本翻译成中文。不要输出除了翻译结果之外的任何内容。"},
            {"role": "user", "content": f"请将以下文本翻译成中文：\n{query}"}
        ],
        "stream": True
    }
    
    try:
        # 发送请求
        response = requests.post(api_url, headers=headers, json=data, stream=True)
        response.raise_for_status()
        
        # 解析流式响应
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    json_str = line[6:]
                    if json_str != '[DONE]':
                        chunk = json.loads(json_str)
                        if 'choices' in chunk and len(chunk['choices']) > 0:
                            content = chunk['choices'][0].get('delta', {}).get('content', '')
                            if content:
                                yield content
    except requests.exceptions.RequestException as e:
        yield f"翻译失败，错误信息：\n{str(e)}"
    except json.JSONDecodeError as e:
        yield f"解析响应失败，错误信息：\n{str(e)}"

# 使用示例
if __name__ == '__main__':
    query = "Hello World! This is 1st paragraph.\nThis is 2nd paragraph."
    for chunk in translate(query):
        print(chunk, end='', flush=True)