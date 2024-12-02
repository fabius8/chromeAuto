import subprocess
import time
import pyautogui
import os
import psutil
import zipfile

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

def launch_chrome(i, port, window_size, window_position):
    """启动Chrome实例"""
    app = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
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
        "--no-proxy-server",
        window_position,
        user_data_dir,
        remote_debugging_port
    ]
    
    # 如果有扩展，添加到参数中
    if extensions_cmd:
        parameters.append(extensions_cmd)
    
    chrome_args = [app] + parameters
    print(chrome_args)
    subprocess.Popen(chrome_args)
    time.sleep(0.5)  # 等待 Chrome 加载完成

def kill_chrome_processes():
    """精确查找和关闭特定的Chrome实例"""
    search_string = "\\USERDATA\\"
    chrome_procs = []
    filtered_lists = []
    
    print("查找Chrome实例...")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'chrome.exe' in proc.info['name']:
                chrome_procs.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    print(f"找到 {len(chrome_procs)} 个Chrome实例")
    
    # 查找包含特定用户数据目录的实例
    for chrome_proc in chrome_procs:
        try:
            if any(search_string in arg for arg in chrome_proc.cmdline()):
                filtered_list = [item for item in chrome_proc.cmdline() if '--user-data-dir' in item]
                filtered_lists.append(filtered_list)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    filtered_lists = [tuple(x) for x in filtered_lists]
    filtered_lists = list(set(filtered_lists))
    filtered_lists.sort(key=lambda x: x[0])
    
    print(f"\n找到 {len(filtered_lists)} 个包含 '{search_string}' 的Chrome实例:")
    for i, instance in enumerate(filtered_lists, start=1):
        print(f"{i}. {instance[0]}")
        
    # 关闭所有符合条件的Chrome实例
    closed_count = 0
    for chrome_proc in chrome_procs:
        try:
            if any(search_string in arg for arg in chrome_proc.cmdline()):
                chrome_proc.terminate()
                closed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
            
    print(f"已关闭 {closed_count} 个Chrome实例")
    time.sleep(2)  # 等待进程完全关闭

def main():
    screen_width, screen_height = get_screen_size()
    chrome_width, chrome_height = get_chrome_size(screen_width, screen_height)
    window_size = f"--window-size={chrome_width},{chrome_height}"
    
    range_list = get_range_list()
    port_base = 9200
    
    for index, i in enumerate(range_list):
        port = port_base + i
        window_position = "--window-position={},{}".format(*get_window_position(index, chrome_width, chrome_height))
        launch_chrome(i, port, window_size, window_position)

        # 等待10秒
        print(f"等待10秒...")
        time.sleep(10)
        # 关闭Chrome
        print(f"关闭Chrome实例 {i:04}")
        kill_chrome_processes()
        
        # 等待确保进程完全关闭
        time.sleep(2)
    
    print("\n所有Chrome实例处理完成")

if __name__ == "__main__":
    main()