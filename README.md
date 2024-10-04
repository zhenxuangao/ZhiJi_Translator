# 知己翻译

## 介绍

知己翻译是一款基于 Python 的翻译工具，实时监测剪贴板内容并进行翻译，提供快速、准确的翻译服务。

## 功能

- 基本功能：自动检测剪贴板内容并进行翻译，用户仅需复制待翻译文本，翻译结果便会自动显示在窗口中
- 翻译服务：提供百度翻译与 ChatGPT 翻译（流式传输）两种翻译方式
- 窗口适配：窗口自动适配屏幕显示缩放
- 字号调整：支持字号大小调整
- 增量翻译：点击按钮，下一次翻译的结果将自动添加到此次翻译结果之后
- 窗口置顶：窗口始终置顶，方便用户随时查看翻译结果
- 记住选项：自动记住应用窗口位置和大小以及应用选项

## 使用方法

### 方法一：源码运行

1. 在根目录下新建 config.json 文件，写入以下内容：
```json
{
    "baidu": {
        "appid": "你的百度翻译 appid",
        "appkey": "你的百度翻译 appkey"
    },
    "openai": {
        "api_url": "OpenAI API 地址",
        "api_key": "你的 OpenAI api key"
    }
}
```
2. 安装依赖包
```bash
pip install requests
pip install pyperclip
```
3. 运行以下指令（若有 anaconda 环境，运行 run.bat 文件即可）
```bash
python ZhiJiTranslator.py
```

### 方法二：.exe 文件运行

这一方法通过 pyinstaller 打包成安装包，方便没有 python 环境的用户使用。

1. 下载 dist 文件夹以及其中的文件
2. 在 dist 目录下新建 config.json 文件，写入以下内容：
```json
{
    "baidu": {
        "appid": "你的百度翻译 appid",
        "appkey": "你的百度翻译 appkey"
    },
    "openai": {
        "api_url": "OpenAI API 地址",
        "api_key": "你的 OpenAI api key"
    }
}
```
3. 运行 ZhiJiTranslator.exe 文件
