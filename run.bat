@echo off
:: 激活 Anaconda 环境
call D:\anaconda3\Scripts\activate.bat ZhiJi_Translator

:: 运行 ZhijiTranslator.py
python codes/ZhijiTranslator.py

:: 退出 Anaconda 环境
call conda deactivate