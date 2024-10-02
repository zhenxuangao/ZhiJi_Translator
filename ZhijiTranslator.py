import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import time
from BaiduService import translate as baidu_translate
from OpenAiService import translate as openai_translate
import ctypes

class ZhijiTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("知己翻译器")
        
        # 获取系统DPI缩放
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scale_factor = user32.GetDpiForSystem() / 96.0
        
        # 根据缩放调整窗口大小
        width = int(400 * scale_factor)
        height = int(350 * scale_factor)
        self.root.geometry(f"{width}x{height}")

        # 调整控件大小
        self.default_font_size = int(10 * scale_factor)
        self.text = tk.Text(root, height=10, width=40, font=("TkDefaultFont", self.default_font_size))
        self.text.pack(pady=int(10*scale_factor))

        self.service_var = tk.StringVar()
        self.service_var.set("Baidu")
        self.service_menu = ttk.Combobox(root, textvariable=self.service_var, values=["Baidu", "OpenAI"], font=("TkDefaultFont", self.default_font_size))
        self.service_menu.pack(pady=int(5*scale_factor))
        self.service_menu.bind("<<ComboboxSelected>>", self.on_service_change)

        # 添加字号大小选项
        self.font_size_var = tk.StringVar()
        self.font_size_var.set(str(self.default_font_size))
        self.font_size_label = tk.Label(root, text="字号大小:", font=("TkDefaultFont", self.default_font_size))
        self.font_size_label.pack(side=tk.LEFT, padx=(int(10*scale_factor), 0))
        self.font_size_menu = ttk.Combobox(root, textvariable=self.font_size_var, values=[str(i) for i in range(8, 25)], width=3, font=("TkDefaultFont", self.default_font_size))
        self.font_size_menu.pack(side=tk.LEFT, padx=(0, int(10*scale_factor)))
        self.font_size_menu.bind("<<ComboboxSelected>>", self.change_font_size)

        self.topmost = tk.BooleanVar()
        self.topmost_button = tk.Checkbutton(root, text="窗口置顶", variable=self.topmost, command=self.toggle_topmost, font=("TkDefaultFont", self.default_font_size))
        self.topmost_button.pack(pady=int(5*scale_factor))

        self.last_clipboard = ""
        self.check_clipboard()

    def check_clipboard(self):
        current_clipboard = pyperclip.paste()
        if current_clipboard != self.last_clipboard:
            self.last_clipboard = current_clipboard
            self.translate_text(current_clipboard)
        self.root.after(1000, self.check_clipboard)

    def translate_text(self, text):
        try:
            if self.service_var.get() == "Baidu":
                translated = baidu_translate(text)
            else:
                translated = openai_translate(text)
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, translated)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = ZhijiTranslator(root)
    root.mainloop()
