import subprocess
import time
import pyautogui
import os
import psutil
import zipfile
import tkinter as tk
from tkinter import messagebox
import sys
import json
import socket

def cleanup_port_mapping():
    """清理无效的端口映射"""
    port_mapping = load_port_mapping()
    invalid_ports = []
    
    print("检查端口映射有效性...")
    for chrome_id, port in port_mapping.items():
        # 检查端口是否真正被使用
        if not is_port_in_use(port):
            invalid_ports.append(chrome_id)
            print(f"发现无效端口映射 - Chrome ID: {chrome_id}, Port: {port}")
    
    # 删除无效的端口映射
    for chrome_id in invalid_ports:
        del port_mapping[chrome_id]
        print(f"已删除无效端口映射 - Chrome ID: {chrome_id}")
    
    if invalid_ports:
        save_port_mapping(port_mapping)
        print(f"已清理 {len(invalid_ports)} 个无效端口映射")
    else:
        print("所有端口映射都有效")

def is_port_in_use(port):
    """检查端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except socket.error:
            return True

def get_available_port(chrome_id):
    """获取可用端口"""
    port_mapping = load_port_mapping()
    
    # 检查现有映射
    if str(chrome_id) in port_mapping:
        existing_port = port_mapping[str(chrome_id)]
        if is_port_in_use(existing_port):
            return existing_port
        else:
            # 端口未使用，删除旧映射
            del port_mapping[str(chrome_id)]
            save_port_mapping(port_mapping)
    
    # 获取系统分配的随机可用端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # 绑定到随机可用端口
        s.listen(1)
        port = s.getsockname()[1]
        
    # 保存新的端口映射
    port_mapping[str(chrome_id)] = port
    save_port_mapping(port_mapping)
    return port

def load_port_mapping():
    """从JSON文件加载端口映射"""
    try:
        with open('chrome_ports.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_port_mapping(port_mapping):
    """保存端口映射到JSON文件"""
    with open('chrome_ports.json', 'w') as f:
        json.dump(port_mapping, f, indent=4)

def release_port(chrome_id):
    """释放指定用户的端口"""
    port_mapping = load_port_mapping()
    if str(chrome_id) in port_mapping:
        del port_mapping[str(chrome_id)]
        save_port_mapping(port_mapping)

def get_screen_size():
    """获取屏幕大小并根据缩放比例调整"""
    screen_width, screen_height = pyautogui.size()
    x_change = 0.7
    y_change = 0.7
    screen_width *= x_change
    screen_height *= y_change
    return int(screen_width), int(screen_height)

def calculate_layout(num_windows, screen_width, screen_height):
    """计算最优的窗口布局"""
    min_width = 400
    min_height = 300
    margin = 10
    
    best_layout = None
    min_wasted_space = float('inf')
    
    for cols in range(1, num_windows + 1):
        rows = (num_windows + cols - 1) // cols
        
        window_width = (screen_width - (cols + 1) * margin) // cols
        window_height = (screen_height - (rows + 1) * margin) // rows
        
        if window_width < min_width or window_height < min_height:
            continue
            
        wasted_space = (screen_width * screen_height) - (num_windows * window_width * window_height)
        
        if wasted_space < min_wasted_space:
            min_wasted_space = wasted_space
            best_layout = {
                'rows': rows,
                'cols': cols,
                'window_width': window_width,
                'window_height': window_height
            }
    
    return best_layout

def get_window_position(index, layout, margin=10):
    """计算每个窗口的位置"""
    cols = layout['cols']
    window_width = layout['window_width']
    window_height = layout['window_height']
    
    row = index // cols
    col = index % cols
    
    x = margin + col * (window_width + margin)
    y = margin + row * (window_height + margin)
    
    return x, y

def get_range_list():
    """获取用户输入的范围列表"""
    if len(sys.argv) > 1:
        try:
            number = int(sys.argv[1])
            return [number]
        except ValueError:
            print("无效的命令行参数，请输入有效的数字")
            return []
    
    range_input = input("请输入一个或多个整数（以空格分隔）：").strip().split()
    if len(range_input) == 1:
        start = int(range_input[0])
        end = int(input("请输入结束范围：") or start)
        return list(range(start, end + 1))
    else:
        return [int(i) for i in range_input]

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
    cwd = os.getcwd()
    user_data_dir = f"--user-data-dir={cwd}\\USERDATA\\{i:04}"
    remote_debugging_port = f"--remote-debugging-port={port}"

    plugins_dir = os.path.join(cwd, 'plugins')
    extracted_plugins_dir = os.path.join(cwd, 'extracted_plugins')
    os.makedirs(extracted_plugins_dir, exist_ok=True)
    
    extension_paths = []
    if os.path.exists(plugins_dir):
        for plugin_file in os.listdir(plugins_dir):
            if plugin_file.endswith('.crx'):
                crx_path = os.path.join(plugins_dir, plugin_file)
                plugin_extract_dir = os.path.join(extracted_plugins_dir, os.path.splitext(plugin_file)[0])
                os.makedirs(plugin_extract_dir, exist_ok=True)
                
                if extract_crx(crx_path, plugin_extract_dir):
                    extension_paths.append(plugin_extract_dir)
    
    extensions_cmd = f"--load-extension={','.join(extension_paths)}" if extension_paths else ""
    
    parameters = [
        window_size,
        "--no-message-box",
        "--no-first-run", 
        "--no-default-browser-check",
        "--no-restore-session-state",
        "--disable-session-crashed-bubble",
        "--hide-crash-restore-bubble",
        "--disable-features=Translate",
        window_position,
        user_data_dir,
        remote_debugging_port
    ]

    if proxy:
        proxy_cmd = f"--proxy-server={proxy}"
        parameters.append(proxy_cmd)

    if extensions_cmd:
        parameters.append(extensions_cmd)
    
    chrome_args = [app] + parameters
    print(chrome_args)
    subprocess.Popen(chrome_args)
    time.sleep(0.8)

def main():
    # 在程序开始时清理无效的端口映射
    cleanup_port_mapping()

    screen_width, screen_height = get_screen_size()
    range_list = get_range_list()
    if not range_list:
        return
    
    layout = calculate_layout(len(range_list), screen_width, screen_height)
    if not layout:
        messagebox.showerror("错误", "无法找到合适的窗口布局！")
        return
    
    window_size = f"--window-size={layout['window_width']},{layout['window_height']}"

    proxies = read_proxies()
    warning_shown = False

    for index, i in enumerate(range_list):
        port = get_available_port(i)
        x, y = get_window_position(index, layout)
        window_position = f"--window-position={x},{y}"
        
        if 0 < i <= len(proxies):
            proxy = proxies[i - 1]
        else:
            if not warning_shown:
                root = tk.Tk()
                root.withdraw()
                messagebox.showwarning("警告", "代理服务器未配置！")
                root.destroy()
                warning_shown = True
            proxy = None
        
        launch_chrome(i, port, window_size, window_position, proxy)

if __name__ == "__main__":
    main()
