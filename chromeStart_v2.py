import subprocess
import time
import pyautogui
import os
import psutil
import zipfile
import tkinter as tk
from tkinter import messagebox

import sys  # 添加到文件开头的导入部分



def get_screen_size():
    """获取屏幕大小并根据缩放比例调整"""
    screen_width, screen_height = pyautogui.size()
    x_change = 0.65
    y_change = 0.64
    screen_width *= x_change
    screen_height *= y_change
    return int(screen_width), int(screen_height)

def get_chrome_size(screen_width, screen_height):
    """计算Chrome浏览器窗口大小"""
    chrome_width = screen_width // 5
    chrome_height = screen_height // 2
    return chrome_width, chrome_height

def get_range_list():
    """获取用户输入的范围列表"""
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        try:
            # 将命令行参数转换为整数
            number = int(sys.argv[1])
            return [number]
        except ValueError:
            print("无效的命令行参数，请输入有效的数字")
            return []
    
    # 原有的交互式输入逻辑
    range_input = input("请输入一个或多个整数（以空格分隔）：").strip().split()
    if len(range_input) == 1:
        start = int(range_input[0])
        end = int(input("请输入结束范围：") or start)
        return list(range(start, end + 1))
    else:
        return [int(i) for i in range_input]

def get_window_position(index, chrome_width, chrome_height):
    """计算窗口位置"""
    n = index % 10
    if n <= 4:
        x = n * chrome_width
        y = 0
    else:
        x = (n - 5) * chrome_width
        y = chrome_height
    return x, y

def extract_crx(crx_path, extract_dir):
    """解压 .crx 文件"""
    try:
        with zipfile.ZipFile(crx_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"成功解压: {crx_path}")
        return True
    except Exception as e:
        print(f"解压失败: {crx_path}, 错误: {e}")
        return False

def read_proxies():
    """读取所有代理配置"""
    proxy_file = 'proxy.txt'
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            # 过滤空行和去除空白
            proxies = [line.strip() for line in f if line.strip()]
            return proxies
    except FileNotFoundError:
        print(f"未找到 {proxy_file} 文件。将不使用代理。")
        return []
    except Exception as e:
        print(f"读取代理文件错误: {e}")
        return []

def launch_chrome(i, port, window_size, window_position, proxy):
    """启动Chrome实例"""
    app = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    #app = "D:\\tools\chrome-win\\chrome.exe"
    cwd = os.getcwd()
    user_data_dir = f"--user-data-dir={cwd}\\USERDATA\\{i:04}"
    remote_debugging_port = f"--remote-debugging-port={port}"

    # 插件目录
    plugins_dir = os.path.join(cwd, 'plugins')
    extracted_plugins_dir = os.path.join(cwd, 'extracted_plugins')
    os.makedirs(extracted_plugins_dir, exist_ok=True)
    
    # 收集所有插件的路径
    extension_paths = []
    if os.path.exists(plugins_dir):
        for plugin_file in os.listdir(plugins_dir):
            if plugin_file.endswith('.crx'):
                crx_path = os.path.join(plugins_dir, plugin_file)
                plugin_extract_dir = os.path.join(extracted_plugins_dir, os.path.splitext(plugin_file)[0])
                os.makedirs(plugin_extract_dir, exist_ok=True)
                
                if extract_crx(crx_path, plugin_extract_dir):
                    extension_paths.append(plugin_extract_dir)
    
    # 使用 join 方法合并扩展路径
    extensions_cmd = f"--load-extension={','.join(extension_paths)}" if extension_paths else ""
    
    parameters = [
        window_size,
        "--no-message-box",
        "--no-first-run", 
        "--no-default-browser-check",
        "--no-restore-session-state",
        "--disable-session-crashed-bubble",
        "--hide-crash-restore-bubble",
        #"--no-proxy-server",
        "--disable-features=Translate",
        #"--proxy-server=http://127.0.0.1:10971",
        window_position,
        user_data_dir,
        remote_debugging_port
    ]

    # 如果有代理，添加代理参数
    if proxy:
        proxy_cmd = f"--proxy-server={proxy}"
        parameters.append(proxy_cmd)

    # 如果有扩展，添加到参数中
    if extensions_cmd:
        parameters.append(extensions_cmd)
    
    chrome_args = [app] + parameters
    print(chrome_args)
    subprocess.Popen(chrome_args)
    time.sleep(0.8)  # 等待 Chrome 加载完成

def main():
    screen_width, screen_height = get_screen_size()
    chrome_width, chrome_height = get_chrome_size(screen_width, screen_height)
    window_size = f"--window-size={chrome_width},{chrome_height}"
    
    range_list = get_range_list()
    if not range_list:  # 如果range_list为空（可能是因为无效的命令行参数），直接返回
        return
    
    port_base = 9200
    
    proxies = read_proxies()
    
    warning_shown = False  # 添加标志变量

    for index, i in enumerate(range_list):
        port = port_base + i
        window_position = "--window-position={},{}".format(*get_window_position(index, chrome_width, chrome_height))
        
        # 使用 if-else 判断，超出范围则弹窗
        if 0 < i <= len(proxies):
            proxy = proxies[i - 1]  # 正常获取代理
        else:
            if not warning_shown:  # 检查是否已经弹出过警告
                # 弹出警告窗口
                root = tk.Tk()
                root.withdraw()  # 隐藏主窗口
                messagebox.showwarning("警告", "代理服务器未配置！")
                root.destroy()  # 销毁窗口
                warning_shown = True  # 设置标志为 True
            proxy = None  # 设置为 None
        
        launch_chrome(i, port, window_size, window_position, proxy)

if __name__ == "__main__":
    main()