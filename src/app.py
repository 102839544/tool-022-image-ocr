#!/usr/bin/env python3
"""
图片OCR文字识别工具 - 真实功能
需要安装：pip install pytesseract pillow
并安装 Tesseract-OCR：https://github.com/tesseract-ocr/tesseract
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext
import tkinter as tk

try:
    import pytesseract
    from PIL import Image
    HAS_DEP = True
except ImportError:
    HAS_DEP = False

class App:
    def __init__(self, root):
        self.root = root
        root.title("图片OCR文字识别工具 v1.0")
        root.geometry("750x600")
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#1f538d", height=60)
        f.pack(fill="x")
        tk.Label(f, text="📝 图片OCR文字识别", font=("Arial",16,"bold"),
                 fg="white", bg="#1f538d").pack(pady=15)
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill="both", expand=True)
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="选择图片", command=self.load_image,
                  bg="#1f538d", fg="white", padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="开始识别", command=self.ocr,
                  bg="#5cb85c", fg="white", font=("Arial",10,"bold"),
                  padx=20).pack(side="right", padx=5)
        tk.Label(main, text="识别结果：", font=("Arial",11,"bold")).pack(anchor="w", pady=(10,5))
        self.txt = scrolledtext.ScrolledText(main, font=("Consolas",11),
                                              wrap="word", height=20)
        self.txt.pack(fill="both", expand=True)
        self.status = tk.Label(main, text="请选择一张图片开始OCR识别",
                               font=("Arial",10), fg="gray", anchor="w")
        self.status.pack(fill="x", pady=5)
    
    def load_image(self):
        f = filedialog.askopenfilename(title="选择图片",
             filetypes=[("图片","*.jpg *.jpeg *.png *.bmp *.tiff")])
        if f:
            self.current_image = f
            self.status.config(text=f"已选择：{Path(f).name}")
    
    def ocr(self):
        if not hasattr(self, "current_image"):
            messagebox.showwarning("提示", "请先选择图片")
            return
        if not HAS_DEP:
            messagebox.showerror("缺少依赖",
                "请运行以下命令安装依赖：\n\npip install pytesseract pillow\n\n"
                "并安装 Tesseract-OCR：\n"
                "https://github.com/tesseract-ocr/tesseract/releases")
            return
        try:
            self.status.config(text="正在识别中...")
            self.root.update()
            img = Image.open(self.current_image)
            text = pytesseract.image_to_string(img, lang="chi_sim+eng")
            self.txt.delete(1.0, "end")
            self.txt.insert(1.0, text)
            self.status.config(text="✅ 识别完成！可复制上方文字")
        except Exception as e:
            self.status.config(text="❌ 识别失败")
            messagebox.showerror("错误", f"OCR识别失败：\n{str(e)}\n\n"
                "请确保已安装 Tesseract-OCR 并配置了语言包。")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
