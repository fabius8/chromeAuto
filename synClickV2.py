import win32api
import win32gui
import win32process
import win32con
import psutil
import re
from pynput import mouse, keyboard
import threading
from typing import Dict, Optional
import time

class ChromeWindowMonitor:
    def __init__(self):
        self.windows: Dict[int, dict] = {}
        self.running = True
        self.mouse_listener = None
        self.keyboard_listener = None
        self.refresh_thread = None
        self.active_window = None
        
        # 添加日志控制 - 默认只开启错误日志
        self.logging = {
            'system': True,   # 系统日志开关
            'info': True,     # 信息日志开关
            'error': True,     # 错误日志开关
            'debug': True     # 调试日志开关
        }

    def log(self, level: str, message: str):
        """统一的日志输出函数"""
        if self.logging.get(level.lower(), False):
            level_upper = level.upper()
            print(f"[{level_upper}] {message}")

    def set_log_level(self, level: str, enabled: bool):
        """设置日志级别开关"""
        if level.lower() in self.logging:
            self.logging[level.lower()] = enabled
            self.log('system', f"日志级别 {level} 已{'启用' if enabled else '禁用'}")

    def toggle_all_logs(self, enabled: bool):
        """统一设置所有日志开关"""
        for level in self.logging:
            self.logging[level] = enabled
        self.log('system', f"所有日志已{'启用' if enabled else '禁用'}")

    def get_process_cmdline(self, pid: int) -> list:
        try:
            process = psutil.Process(pid)
            return process.cmdline()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []

    def get_window_at_point(self, x: int, y: int) -> Optional[dict]:
        hwnd = win32gui.WindowFromPoint((x, y))
        while hwnd:
            if hwnd in self.windows:
                return self.windows[hwnd]
            hwnd = win32gui.GetParent(hwnd)
        return None

    def get_window_rect(self, hwnd):
        try:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            return {'left': left, 'top': top, 'right': right, 'bottom': bottom,
                   'width': right - left, 'height': bottom - top}
        except:
            return None

    def get_first_child_window(self, hwnd):
        try:
            child_windows = self.windows[hwnd]['child_windows']
            return child_windows[0] if child_windows else None
        except (KeyError, IndexError):
            return None

    def is_matching_window(self, source_window, target_window):
        # 如果是父窗口(parent_handle == 0)，只需要检查是否都是父窗口
        if source_window['parent_handle'] == 0 and target_window['parent_handle'] == 0:
            return True
            
        # 如果是子窗口，则需要检查class是否相同
        if (source_window['parent_handle'] != 0 and 
            target_window['parent_handle'] != 0 and 
            source_window['class'] == target_window['class']):
            return True
            
        return False

    def simulate_click(self, hwnd, rel_x, rel_y):
        try:
            lParam = win32api.MAKELONG(int(rel_x), int(rel_y))
            win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
        except Exception as e:
            self.log('error', f"模拟点击失败: {e}")

    def mirror_click(self, source_window, x, y):
        if not source_window:
            return
                
        source_rect = self.get_window_rect(source_window['handle'])
        if not source_rect:
            return
                
        rel_x_percent = (x - source_rect['left']) / source_rect['width']
        rel_y_percent = (y - source_rect['top']) / source_rect['height']
        source_userdata = source_window['userdata_number']
        
        for hwnd, window in self.windows.items():
            if window['userdata_number'] == source_userdata:
                continue
                
            target_window = window
            if (source_window['parent_handle'] != 0 and 
                target_window['parent_handle'] == 0):
                child = self.get_first_child_window(hwnd)
                if child:
                    target_window = child
                    
            if self.is_matching_window(source_window, target_window):
                target_rect = self.get_window_rect(target_window['handle'])
                if target_rect:
                    target_x = int(target_rect['width'] * rel_x_percent)
                    target_y = int(target_rect['height'] * rel_y_percent)
                    self.log('info', f"同步点击: 窗口 {target_window['title']} (USERDATA: {window['userdata_number']})")
                    self.simulate_click(target_window['handle'], target_x, target_y)

    def simulate_right_click(self, hwnd, rel_x, rel_y):
        try:
            lParam = win32api.MAKELONG(int(rel_x), int(rel_y))
            win32api.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
            win32api.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, lParam)
        except Exception as e:
            self.log('error', f"模拟右键点击失败: {e}")

    def mirror_right_click(self, source_window, x, y):
        if not source_window:
            return
                
        source_rect = self.get_window_rect(source_window['handle'])
        if not source_rect:
            return
                
        rel_x_percent = (x - source_rect['left']) / source_rect['width']
        rel_y_percent = (y - source_rect['top']) / source_rect['height']
        source_userdata = source_window['userdata_number']
        
        for hwnd, window in self.windows.items():
            if window['userdata_number'] == source_userdata:
                continue
                
            target_window = window
            if (source_window['parent_handle'] != 0 and 
                target_window['parent_handle'] == 0):
                child = self.get_first_child_window(hwnd)
                if child:
                    target_window = child
                    
            if self.is_matching_window(source_window, target_window):
                target_rect = self.get_window_rect(target_window['handle'])
                if target_rect:
                    target_x = int(target_rect['width'] * rel_x_percent)
                    target_y = int(target_rect['height'] * rel_y_percent)
                    self.log('info', f"同步右键: 窗口 {target_window['title']} (USERDATA: {window['userdata_number']})")
                    self.simulate_right_click(target_window['handle'], target_x, target_y)

    def simulate_scroll(self, hwnd, rel_x, rel_y, delta):
        """模拟鼠标滚轮操作"""
        try:
            # 获取窗口位置
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            
            # 构造消息参数，参考老代码的方式
            wParam = win32api.MAKELONG(0, delta * 120)
            lParam = win32api.MAKELONG(x + rel_x, y + rel_y)
            
            # 直接发送到主窗口
            win32api.SendMessage(hwnd, win32con.WM_MOUSEWHEEL, wParam, lParam)
            
        except Exception as e:
            self.log('error', f"模拟滚轮失败: {e}")

    def mirror_scroll(self, source_window, x, y, delta):
        """镜像滚轮操作到其他窗口"""
        if not source_window:
            return
                
        source_rect = self.get_window_rect(source_window['handle'])
        if not source_rect:
            return
                
        rel_x_percent = (x - source_rect['left']) / source_rect['width']
        rel_y_percent = (y - source_rect['top']) / source_rect['height']
        source_userdata = source_window['userdata_number']
        
        for hwnd, window in self.windows.items():
            if window['userdata_number'] == source_userdata:
                continue
                
            target_window = window
            if (source_window['parent_handle'] != 0 and 
                target_window['parent_handle'] == 0):
                child = self.get_first_child_window(hwnd)
                if child:
                    target_window = child
                    
            if self.is_matching_window(source_window, target_window):
                target_rect = self.get_window_rect(target_window['handle'])
                if target_rect:
                    target_x = int(target_rect['width'] * rel_x_percent)
                    target_y = int(target_rect['height'] * rel_y_percent)
                    self.log('info', f"同步滚轮: 窗口 {target_window['title']} (USERDATA: {window['userdata_number']})")
                    self.simulate_scroll(target_window['handle'], target_x, target_y, delta)

    def on_scroll(self, x, y, dx, dy):
        """处理鼠标滚轮事件"""
        window = self.get_window_at_point(x, y)
        if not window:
            return
            
        min_window = self.get_min_userdata_window()
        if not min_window:
            return
            
        if window['userdata_number'] == min_window['userdata_number']:
            self.log('info', f"检测到滚轮: {window['title']}")
            self.mirror_scroll(window, x, y, dy)

    def simulate_key(self, hwnd, key, is_press):
        try:
            special_keys = {
                keyboard.Key.backspace: win32con.VK_BACK,
                keyboard.Key.tab: win32con.VK_TAB,
                keyboard.Key.enter: win32con.VK_RETURN,
                keyboard.Key.shift: win32con.VK_SHIFT,
                keyboard.Key.ctrl: win32con.VK_CONTROL,
                keyboard.Key.alt: win32con.VK_MENU,
                keyboard.Key.caps_lock: win32con.VK_CAPITAL,
                keyboard.Key.esc: win32con.VK_ESCAPE,
                keyboard.Key.space: win32con.VK_SPACE,
                keyboard.Key.page_up: win32con.VK_PRIOR,
                keyboard.Key.page_down: win32con.VK_NEXT,
                keyboard.Key.end: win32con.VK_END,
                keyboard.Key.home: win32con.VK_HOME,
                keyboard.Key.left: win32con.VK_LEFT,
                keyboard.Key.up: win32con.VK_UP,
                keyboard.Key.right: win32con.VK_RIGHT,
                keyboard.Key.down: win32con.VK_DOWN,
                keyboard.Key.insert: win32con.VK_INSERT,
                keyboard.Key.delete: win32con.VK_DELETE,
            }

            # 添加调试日志
            self.log('debug', f"模拟按键: key={key}, is_press={is_press}, hwnd={hwnd}")

            # 处理特殊键
            if isinstance(key, keyboard.Key):
                vk_code = special_keys.get(key)
                if vk_code is None:
                    self.log('debug', f"未找到特殊键映射: {key}")
                    return
                char_code = None
            # 处理普通按键
            elif hasattr(key, 'vk'):
                vk_code = key.vk
                # 对于普通字符，获取对应的字符
                if hasattr(key, 'char') and key.char:
                    char_code = ord(key.char)
                else:
                    char_code = vk_code
            # 处理直接输入的字符
            else:
                char = str(key)
                vk_code = ord(char.upper())
                char_code = ord(char)

            # 获取扫描码
            scan_code = win32api.MapVirtualKey(vk_code, 0)
            # 构造基础lparam
            lparam = (scan_code << 16) | 1

            # 检查窗口状态
            if not win32gui.IsWindow(hwnd):
                self.log('error', f"无效窗口句柄: {hwnd}")
                return

            # 获取窗口标题用于日志
            try:
                title = win32gui.GetWindowText(hwnd)
            except:
                title = "未知窗口"

            if is_press:
                # 发送按键按下消息
                self.log('debug', f"发送按键按下: vk_code={vk_code}, hwnd={hwnd}, title={title}")
                win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, vk_code, lparam)
                
                # 对于普通字符，发送WM_CHAR消息
                if char_code is not None and not isinstance(key, keyboard.Key):
                    self.log('debug', f"发送字符消息: char_code={char_code}, hwnd={hwnd}")
                    win32api.SendMessage(hwnd, win32con.WM_CHAR, char_code, lparam)
            else:
                # 按键释放时设置相应的标志位
                lparam |= (1 << 31)  # 按键释放标志
                self.log('debug', f"发送按键释放: vk_code={vk_code}, hwnd={hwnd}, title={title}")
                win32api.SendMessage(hwnd, win32con.WM_KEYUP, vk_code, lparam)

            # 处理组合键（Ctrl+C, Ctrl+V等）
            if hasattr(key, 'char') and key.char:
                ctrl_pressed = win32api.GetKeyState(win32con.VK_CONTROL) < 0
                if ctrl_pressed:
                    self.log('debug', f"检测到组合键: Ctrl + {key.char}")
                    # 对于复制粘贴操作可以添加额外延时
                    if key.char.lower() == 'v':
                        time.sleep(0.1)

        except Exception as e:
            self.log('error', f"模拟按键失败: hwnd={hwnd}, key={key}, error={str(e)}")

    def mirror_key(self, key, is_press):
        if not self.active_window:
            return
                
        source_userdata = self.active_window['userdata_number']
        min_window = self.get_min_userdata_window()
        if not min_window or self.active_window['userdata_number'] != min_window['userdata_number']:
            return
                
        for hwnd, window in self.windows.items():
            if window['userdata_number'] == source_userdata:
                continue
                
            target_window = window
            if (self.active_window['parent_handle'] != 0 and 
                target_window['parent_handle'] == 0):
                child = self.get_first_child_window(hwnd)
                if child:
                    target_window = child
                    
            if self.is_matching_window(self.active_window, target_window):
                if is_press:
                    self.log('info', f"同步按键: {key} -> 窗口 {target_window['title']}")
                self.simulate_key(target_window['handle'], key, is_press)

    def get_min_userdata_window(self):
        if not self.windows:
            return None
        return min(self.windows.values(), key=lambda w: int(w['userdata_number']))

    def refresh_windows(self):
        new_windows = {}
        
        def enum_window_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                class_name = win32gui.GetClassName(hwnd)
                
                if class_name == "Chrome_WidgetWin_1":
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    cmdline = self.get_process_cmdline(pid)
                    
                    userdata_cmd = next((cmd for cmd in cmdline 
                                    if 'USERDATA' in cmd and '--user-data-dir=' in cmd), None)
                    
                    if userdata_cmd:
                        match = re.search(r'USERDATA\\(\d+)', userdata_cmd)
                        if match:
                            placement = win32gui.GetWindowPlacement(hwnd)
                            child_windows = []
                            
                            def enum_child_callback(child_hwnd, child_list):
                                child_list.append({
                                    'handle': child_hwnd,
                                    'class': win32gui.GetClassName(child_hwnd),
                                    'title': win32gui.GetWindowText(child_hwnd),
                                    'parent_handle': hwnd
                                })
                                return True
                            
                            win32gui.EnumChildWindows(hwnd, enum_child_callback, child_windows)
                            
                            new_windows[hwnd] = {
                                'handle': hwnd,
                                'class': class_name,
                                'title': win32gui.GetWindowText(hwnd),
                                'pid': pid,
                                'userdata_number': match.group(1),
                                'userdata_path': userdata_cmd,
                                'parent_handle': win32gui.GetParent(hwnd),
                                'child_windows': child_windows,
                                'is_enabled': win32gui.IsWindowEnabled(hwnd),
                                'is_visible': win32gui.IsWindowVisible(hwnd),
                                'is_minimized': placement[1] == win32con.SW_SHOWMINIMIZED,
                                'is_maximized': placement[1] == win32con.SW_SHOWMAXIMIZED
                            }
                return True

        win32gui.EnumWindows(enum_window_callback, None)
        
        if not self.windows and new_windows:
            self.log('system', "Chrome窗口同步工具已启动")
            self.log('system', f"已检测到 {len(new_windows)} 个Chrome窗口")
            self.log('system', "按F9退出程序")
        
        self.windows = new_windows

    def refresh_thread_func(self):
        while self.running:
            self.refresh_windows()
            time.sleep(1)

    def on_click(self, x, y, button, pressed):
        if not pressed:
            return
            
        window = self.get_window_at_point(x, y)
        if not window:
            return
            
        min_window = self.get_min_userdata_window()
        if not min_window:
            return
            
        if window['userdata_number'] == min_window['userdata_number']:
            action = "左键" if button == mouse.Button.left else "右键"
            self.log('info', f"检测到{action}点击: {window['title']}")
            
            if button == mouse.Button.left:
                self.mirror_click(window, x, y)
            elif button == mouse.Button.right:
                self.mirror_right_click(window, x, y)

    def on_key_press(self, key):
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd in self.windows:
                self.active_window = self.windows[hwnd]
                self.log('debug', f"按键按下: key={key}, window={self.active_window['title']}")
                self.mirror_key(key, True)
        except Exception as e:
            self.log('error', f"按键处理失败: {e}")

    def on_key_release(self, key):
        try:
            if key == keyboard.Key.f9:
                self.log('system', "正在退出程序...")
                self.stop()
                import sys
                sys.exit(0)
                
            hwnd = win32gui.GetForegroundWindow()
            if hwnd in self.windows:
                self.active_window = self.windows[hwnd]
                self.log('debug', f"按键释放: key={key}, window={self.active_window['title']}")
                self.mirror_key(key, False)
        except Exception as e:
            self.log('error', f"按键处理失败: {e}")

    def start(self):
        self.refresh_windows()
        
        self.refresh_thread = threading.Thread(target=self.refresh_thread_func)
        self.refresh_thread.daemon = True
        self.refresh_thread.start()
        
        # 更新鼠标监听器，添加滚轮事件
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        self.mouse_listener.start()
        
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release)
        self.keyboard_listener.start()
        
        self.log('system', "开始监控Chrome窗口...")
        
        try:
            self.keyboard_listener.join()
            self.mouse_listener.join()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.refresh_thread:
            self.refresh_thread.join()
        self.log('system', "程序已停止运行")

if __name__ == "__main__":
    monitor = ChromeWindowMonitor()
    # 默认只开启错误日志，其他都关闭
    monitor.start()
