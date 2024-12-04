import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import threading
import pygetwindow as gw
import json
import os
# 在文件开头添加导入
import keyboard

google_minimized = False

class UndoEntry(tk.Entry):
    """支持撤销/重做的Entry控件"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # 绑定按键事件
        self.bind('<Control-z>', self.undo)
        self.bind('<Control-y>', self.redo)
        self.bind('<Key>', self.record_change)
        
        # 初始化撤销/重做栈
        self.undo_stack = []
        self.redo_stack = []
        self.last_value = ''
        
    def record_change(self, event=None):
        """记录变更"""
        if event.keysym not in ('Control_L', 'Control_R', 'z', 'y'):  # 忽略控制键
            current = self.get()
            if current != self.last_value:
                self.undo_stack.append(self.last_value)
                self.last_value = current
                self.redo_stack.clear()  # 有新输入时清空重做栈
    
    def undo(self, event=None):
        """撤销"""
        if self.undo_stack:
            current = self.get()
            self.redo_stack.append(current)
            previous = self.undo_stack.pop()
            self.delete(0, tk.END)
            self.insert(0, previous)
            self.last_value = previous
        return 'break'  # 防止事件继续传播
    
    def redo(self, event=None):
        """重做"""
        if self.redo_stack:
            current = self.get()
            self.undo_stack.append(current)
            next_value = self.redo_stack.pop()
            self.delete(0, tk.END)
            self.insert(0, next_value)
            self.last_value = next_value
        return 'break'

def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)

def run_command(command, success_msg, error_msg):
    def execute():
        try:
            log_message(f"执行命令: {command}")
            subprocess.run(command, check=True, shell=True)
            log_message(success_msg)
        except subprocess.CalledProcessError as e:
            log_message(f"{error_msg}: {e}")
    threading.Thread(target=execute).start()

# 加载和保存配置的函数
config_file = 'settings.json'  # 合并后的配置文件名称

# 修改加载配置函数
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return (
                config.get('base_path', ""), 
                config.get('urls', {}),
                config.get('custom_commands', ['', '', ''])  # 加载自定义命令
            )
    return "", {}, ['', '', '']

# 修改保存配置函数
def save_config(base_path, urls, custom_commands):
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump({
            'base_path': base_path, 
            'urls': urls,
            'custom_commands': custom_commands
        }, f, ensure_ascii=False, indent=4)

# 修改 select_path 函数
def select_path():
    path = filedialog.askdirectory()
    if path:
        global base_path
        base_path = path
        save_config(base_path, urls, custom_commands)  # 添加 custom_commands 参数
        log_message(f"路径已设置为: {base_path}")

# 初始化路径变量
base_path, urls, custom_commands = load_config()

# 在其他函数定义的地方添加
def press_f9():
    keyboard.press_and_release('F9')
    log_message("已触发F9按键")

# 修改 command_custom 函数以记录最后使用的命令
def command_custom(cmd, index=None):
    run_command(f"cd /d {base_path} && node chromeAuto.js {cmd}", "网页已打开", "打开网页失败")
    
    # 如果提供了索引，更新对应的命令
    if index is not None:
        custom_commands[index] = cmd
        save_config(base_path, urls, custom_commands)

def open_vpn():
    run_command(f"powershell -File {base_path}\\v2rayN-With-Core\\bin\\v2fly_v5\\run_v2ray.ps1", "VPN已打开", "打开VPN失败")

def open_google():
    run_command(f"cd /d {base_path} && python chromeStart_v2.py", "谷歌已打开", "打开谷歌失败")

def close_google():
    run_command(f"cd /d {base_path} && python chromeClose.py", "谷歌已关闭", "关闭谷歌失败")

def login_okx():
    run_command(f"cd /d {base_path} && node chromeAuto.js okLogin", "网页已打开", "打开网页失败")

def sync_window():
    run_command(f"cd /d {base_path} && python synClickV2.py", "窗口同步已完成", "窗口同步失败")

def incognito_mode():
    run_command(f"cd /d {base_path} && python chromeStart_incognito.py", "无痕模式已启动", "启动无痕模式失败")

# 修改 open_web 函数
def open_web(url, key):
    if not url:
        log_message("URL不能为空")
        messagebox.showwarning("Warning", "URL不能为空")
        return
    
    urls[key] = url
    save_config(base_path, urls, custom_commands)  # 添加 custom_commands 参数
    
    run_command(f"cd /d {base_path} && node chromeAuto.js open {url}", "网页已打开", "打开网页失败")

def close_web(url):
    if not url:
        log_message("URL不能为空")
        messagebox.showwarning("Warning", "URL不能为空")
        return
    
    run_command(f"cd /d {base_path} && node chromeAuto.js close {url}", "网页已关闭", "关闭网页失败")

def zoom_google():
    global google_minimized
    try:
        windows = gw.getWindowsWithTitle('Google Chrome')
        if windows:
            if google_minimized:
                for window in windows:
                    window.restore()
                log_message("所有谷歌窗口已还原")
                google_minimized = False
            else:
                for window in windows:
                    window.minimize()
                log_message("所有谷歌窗口已缩小")
                google_minimized = True
        else:
            log_message("未找到谷歌浏览器窗口")
    except Exception as e:
        log_message(f"缩小/还原谷歌失败: {e}")

def close_all_google():
    run_command("taskkill /F /IM chrome.exe", "所有谷歌浏览器已关闭", "关闭所有谷歌浏览器失败")

def extract_query_id():
    run_command(f"cd /d {base_path} && node chromeAuto.js tgQueryId", "queryID提取成功", "提取queryID失败")

def create_url_frame(parent, url_key, default_url, row):
    frame = tk.Frame(parent)
    frame.pack(anchor='w')

    btn_open = tk.Button(frame, text=f"打开网页{row}", command=lambda: open_web(url_entries[row].get(), url_key))
    btn_open.pack(side=tk.LEFT)

    # 使用新的 UndoEntry 替代原来的 Entry
    url_entry = UndoEntry(frame, width=40)
    url_entry.insert(0, urls.get(url_key, default_url))
    url_entry.pack(side=tk.LEFT)
    url_entries[row] = url_entry

    btn_close = tk.Button(frame, text=f"关闭网页{row}", command=lambda: close_web(url_entries[row].get()))
    btn_close.pack(side=tk.LEFT)

# 创建主窗口
root = tk.Tk()
root.title("Google助手v1.0")

# 添加选择路径按钮
btn_select_path = tk.Button(root, text="选择文件路径", command=select_path)
btn_select_path.pack(anchor='w')

# 创建按钮
frame1 = tk.Frame(root)
frame1.pack(anchor='w')

buttons = [
    ("打开VPN", open_vpn),
    ("打开谷歌", open_google),
    ("关闭谷歌", close_google),
    ("登录okx", login_okx),
    ("窗口同步", sync_window),
    ("同步停止/F9", press_f9),
    ("无痕模式", incognito_mode),
    ("缩小恢复谷歌", zoom_google),
    ("提取TG TOKEN", extract_query_id),
]

for text, command in buttons:
    btn = tk.Button(frame1, text=text, command=command)
    btn.pack(side=tk.LEFT)

# 修改创建命令框架的函数
def create_command_frame(parent):
    command_frame = tk.Frame(parent)
    command_frame.pack(anchor='w')

    # 创建标题标签
    title_label = tk.Label(command_frame, text="自定义命令：")
    title_label.pack(anchor='w')

    # 创建命令输入框和按钮的列表，用于后续保存
    cmd_entries = []

    # 创建三组命令输入框和按钮
    for i in range(3):
        frame = tk.Frame(command_frame)
        frame.pack(anchor='w')
        
        # 命令输入框
        cmd_entry = UndoEntry(frame, width=40)
        cmd_entry.insert(0, custom_commands[i])  # 从加载的配置中设置默认值
        cmd_entry.pack(side=tk.LEFT)
        cmd_entries.append(cmd_entry)
        
        # 执行按钮
        def create_command(entry, index):
            return lambda: command_custom(entry.get(), index)
        
        btn_execute = tk.Button(
            frame,
            text=f"执行命令{i+1}",
            command=create_command(cmd_entry, i)
        )
        btn_execute.pack(side=tk.LEFT)

    # 保存按钮
    def save_custom_commands():
        # 获取三个命令输入框的值
        cmds = [entry.get() for entry in cmd_entries]
        save_config(base_path, urls, cmds)
        log_message("自定义命令已保存")

    btn_save_commands = tk.Button(command_frame, text="保存命令", command=save_custom_commands)
    btn_save_commands.pack(anchor='w')

# 在创建 URL 输入框之前调用这个函数
create_command_frame(root)

# ... 其余代码保持不变 ...


# 创建URL输入框和按钮
url_entries = [None] * 10
default_urls = [
    'https://web.telegram.org/k/#777000',
    'https://web.telegram.org/k/#@birdx2_bot',
    'https://web.telegram.org/k/#@Tomarket_ai_bot',
    '', '', '', '', '', '', ''
]

for i in range(10):
    create_url_frame(root, f'url{i}', default_urls[i], i)

# 添加关闭所有谷歌浏览器按钮
btn_close_all_google = tk.Button(root, text="关闭所有谷歌", command=close_all_google)
btn_close_all_google.pack(anchor='w')

# 日志框
log_frame = tk.Frame(root)
log_frame.pack(fill=tk.BOTH, expand=True)

log_text = tk.Text(log_frame, state=tk.NORMAL, wrap=tk.WORD)
log_text.pack(fill=tk.BOTH, expand=True)

# 运行主循环
root.mainloop()
