#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flatten_para_u3000_keep_headers.py
全角空格分段 + 合并折行，但保留 ## 标题前的换行（标题独占一行）。
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import pathlib

def flatten_keep_headers(text: str) -> str:
    lines = text.splitlines()
    out = []
    buf = []          # 当前正文段落缓存

    def flush_buf():
        """合并正文段落并输出"""
        if buf:
            out.append(' '.join(' '.join(buf).split()))
            buf.clear()

    for line in lines:
        raw = line.rstrip()
        # 标题行：先flush正文，再直接把标题原样输出
        if raw.startswith('##'):
            flush_buf()
            out.append(raw)
            continue

        # 普通正文
        if raw.startswith('\u3000'):      # 新段落
            flush_buf()
            buf.append(raw)
        else:                             # 折行续接
            if buf:                       # 只在已有段落时续接，防止意外空行
                buf.append(raw)

    flush_buf()  # 收尾
    return '\n'.join(out)

# ----------------- GUI -----------------
def select_file():
    f = filedialog.askopenfilename(
        title='选择 Markdown 文件',
        filetypes=[('Markdown', '*.md'), ('All', '*.*')])
    if f:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, f)

def on_ok():
    path = pathlib.Path(entry_path.get().strip())
    if not path.exists():
        messagebox.showerror('错误', f'文件不存在：{path}')
        return
    try:
        txt = path.read_text(encoding='utf-8')
        flattened = flatten_keep_headers(txt)
        path.write_text(flattened, encoding='utf-8')
        messagebox.showinfo('完成', f'已写回：{path}')
    except Exception as e:
        messagebox.showerror('出错', str(e))

root = tk.Tk()
root.title('折行合并工具（保留 ## 标题换行）')
tk.Label(root, text='文件路径：').grid(row=0, column=0, padx=10, pady=10)
entry_path = tk.Entry(root, width=50)
entry_path.grid(row=0, column=1, padx=5, pady=10)
tk.Button(root, text='浏览…', command=select_file).grid(row=0, column=2, padx=5)
tk.Button(root, text='开始处理', width=15, command=on_ok).grid(row=1, column=0, columnspan=3, pady=10)
entry_path.focus()
root.mainloop()