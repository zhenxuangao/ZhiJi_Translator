# 知己翻译器

## 介绍

知己翻译器是一款基于 Python 的翻译工具，实时监测剪贴板内容并进行翻译，提供快速、准确的翻译服务。

## 功能

1. 自动检测剪贴板内容并进行翻译
2. 支持窗口始终置顶
3. 支持字号大小调整
4. 支持翻译服务选择，当前支持百度翻译和 OpenAI 翻译
   1. 流式传输：OpenAI翻译结果分段返回，翻译过程中可以实时看到翻译结果
5. 支持增量翻译
6. 自动记住应用窗口位置和大小以及选项

## 使用方法

### 方法一：源码运行

1. 配置 config.json 文件中的 API 密钥
2. 安装依赖包
```bash
pip install requests
pip install pyperclip
```
3. 运行 run.bat 文件（需要 Anaconda 环境）

### 方法二：安装包运行

这一方法通过 pyinstaller 打包成安装包，方便没有 python 环境的用户使用。

1. 下载并解压 zip 文件
2. 配置 config.json 文件中的 API 密钥
3. 运行 ZhiJiTranslator.exe 文件