import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import time
from BaiduService import translate as baidu_translate
from OpenAiService import translate as openai_translate
import ctypes
import json
import os

class ZhijiTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("知己翻译器")
        
        # 获取系统DPI缩放
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scale_factor = user32.GetDpiForSystem() / 96.0
        
        # 加载配置
        self.config = self.load_config()
        
        # 设置窗口最小大小
        min_width = int(400 * scale_factor)
        min_height = int(250 * scale_factor)
        self.root.minsize(min_width, min_height)
        
        # 根据配置设置窗口大小和位置
        width = max(self.config.get('width', min_width), min_width)
        height = max(self.config.get('height', min_height), min_height)
        x = self.config.get('x', 100)
        y = self.config.get('y', 100)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # 创建工具栏
        toolbar = tk.Frame(root, pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # 调整控件大小
        self.default_font_size = int(10 * scale_factor)

        # 服务选择
        self.service_var = tk.StringVar()
        self.service_var.set(self.config.get('service', "Baidu"))
        self.service_label = tk.Label(toolbar, text="翻译服务：", font=("TkDefaultFont", self.default_font_size))
        self.service_label.pack(side=tk.LEFT, padx=(5, 0))
        self.service_menu = ttk.Combobox(toolbar, textvariable=self.service_var, values=["Baidu", "OpenAI"], width=10, font=("TkDefaultFont", self.default_font_size))
        self.service_menu.pack(side=tk.LEFT, padx=(0, 5))
        self.service_menu.bind("<<ComboboxSelected>>", self.on_service_change)

        # 添加字号大小选项
        self.font_size_var = tk.StringVar()
        self.font_size_var.set(str(self.config.get('font_size', self.default_font_size)))
        self.font_size_label = tk.Label(toolbar, text="字号:", font=("TkDefaultFont", self.default_font_size))
        self.font_size_label.pack(side=tk.LEFT, padx=(5, 0))
        self.font_size_menu = ttk.Combobox(toolbar, textvariable=self.font_size_var, values=[str(i) for i in range(8, 25)], width=3, font=("TkDefaultFont", self.default_font_size))
        self.font_size_menu.pack(side=tk.LEFT, padx=(0, 5))
        self.font_size_menu.bind("<<ComboboxSelected>>", self.change_font_size)

        # 置顶功能
        self.topmost = tk.BooleanVar()
        self.topmost.set(self.config.get('topmost', False))
        self.topmost_button = tk.Checkbutton(toolbar, text="置顶", variable=self.topmost, command=self.toggle_topmost, font=("TkDefaultFont", self.default_font_size))
        self.topmost_button.pack(side=tk.LEFT, padx=(5, 5))

        # 增量翻译功能
        self.incremental_button = tk.Button(toolbar, text="增量翻译", command=self.start_incremental_translation, font=("TkDefaultFont", self.default_font_size))
        self.incremental_button.pack(side=tk.LEFT, padx=(5, 5))

        self.text = tk.Text(root, height=10, width=40, font=("TkDefaultFont", int(self.font_size_var.get())))
        self.text.pack(expand=True, fill=tk.BOTH, pady=int(10*scale_factor))

        self.last_clipboard = ""
        self.incremental_mode = False
        self.text1 = ""
        self.check_clipboard()

        # 设置初始置顶状态
        self.toggle_topmost()

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        if os.path.exists('translator_config.json'):
            with open('translator_config.json', 'r') as f:
                return json.load(f)
        return {}

    def save_config(self):
        config = {
            'width': self.root.winfo_width(),
            'height': self.root.winfo_height(),
            'x': self.root.winfo_x(),
            'y': self.root.winfo_y(),
            'service': self.service_var.get(),
            'font_size': int(self.font_size_var.get()),
            'topmost': self.topmost.get()
        }
        with open('translator_config.json', 'w') as f:
            json.dump(config, f)

    def check_clipboard(self):
        current_clipboard = pyperclip.paste()
        if current_clipboard != self.last_clipboard:
            self.last_clipboard = current_clipboard
            if not self.incremental_mode:
                self.translate_text(current_clipboard)
            else:
                self.text2 = current_clipboard
                combined_text = self.text1 + ' ' + self.text2
                pyperclip.copy(combined_text)
                self.translate_text(combined_text)
                self.incremental_mode = False
                self.incremental_button.config(state=tk.NORMAL)
        self.root.after(1000, self.check_clipboard)

    def translate_text(self, text):
        try:
            self.text.delete(1.0, tk.END)
            if self.service_var.get() == "Baidu":
                translated = baidu_translate(text)
                self.text.insert(tk.END, translated)
            else:
                for chunk in openai_translate(text):
                    self.text.insert(tk.END, chunk)
                    self.text.see(tk.END)
                    self.root.update()
        except Exception as e:
            messagebox.showerror("翻译错误", str(e))

    def toggle_topmost(self):
        self.root.attributes("-topmost", self.topmost.get())

    def change_font_size(self, event):
        new_size = int(self.font_size_var.get())
        self.text.configure(font=("TkDefaultFont", new_size))

    def on_service_change(self, event):
        current_clipboard = pyperclip.paste()
        self.translate_text(current_clipboard)

    def start_incremental_translation(self):
        self.text1 = pyperclip.paste()
        self.incremental_mode = True
        self.incremental_button.config(state=tk.DISABLED)

    def on_closing(self):
        self.save_config()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ZhijiTranslator(root)
    root.mainloop()
