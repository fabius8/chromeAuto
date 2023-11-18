import win32gui
import win32con
import win32api
import psutil
import win32process
import re
import time
import json
#import pyautogui

config = json.load(open('config.json'))

k = config["k"]

def sort_by_port(cmdline):
    port_str = next((param for param in cmdline if param.startswith('--remote-debugging-port=')), None)
    if port_str:
        port = int(re.search(r'\d+', port_str).group())
        return port
    else:
        return 0 


def enum_chrome_windows(hwnd, _):
    classname = win32gui.GetClassName(hwnd)
    title = win32gui.GetWindowText(hwnd)
    if classname == 'Chrome_WidgetWin_1' and title:
        #print(title)
        chrome_windows.append(hwnd)


# def click(x, y):
#     print(x, y)
#     win32api.SetCursorPos((x, y))
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

chrome_windows = []
win32gui.EnumWindows(enum_chrome_windows, None)

my_chrome_windows = []
ports = []
for hwnd in chrome_windows:
    print(hwnd)
    process = psutil.Process(win32process.GetWindowThreadProcessId(hwnd)[1])
    if any("--remote-debugging-port" in arg for arg in process.cmdline()):
        print(process.cmdline())
        port_str = next((param for param in process.cmdline() if param.startswith('--remote-debugging-port=')), None)
        if port_str:
            port = int(re.search(r'\d+', port_str).group())
            ports.append(port)
            my_chrome_windows.append(hwnd)
        else:
            continue

print(ports, my_chrome_windows)

sorted_chrome_windows = [x for _, x in sorted(zip(ports, my_chrome_windows))]

print(sorted_chrome_windows)
    
from pynput import mouse, keyboard
from pynput.keyboard import Key, Controller
kb = Controller()

for hwnd in sorted_chrome_windows:
    # 将焦点设置到Chrome窗口
    print(hwnd)
    win32gui.SetForegroundWindow(hwnd)

    # 获取窗口的位置和大小
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print(rect)
    kb.press(Key.alt)
    kb.release(Key.alt)

    #click(x + w // 2, y + h // 2)
    #time.sleep(1)


# 定义鼠标点击监听函数
def on_click(x, y, button, pressed):
    if button == mouse.Button.left and not pressed:  # 监听鼠标左键按下事件
        print('鼠标左键按下，位置:', x, y)
        rect = win32gui.GetWindowRect(sorted_chrome_windows[0])
        rx = rect[0]
        ry = rect[1]
        rw = rect[2] - rx
        rh = rect[3] - ry
        
        # 对位置和大小进行150%缩放
        x_scaled = int(x / k)
        y_scaled = int(y / k)
        print(rx, ry, rw, rh, x_scaled, y_scaled)
        if (x_scaled < rx) or (x_scaled > (rx + rw)) or (y_scaled < ry) or (y_scaled > (ry + rh)):
            print("not win#1, skip")
            return
        
        # 相对窗口位置
        x_related = x_scaled - rx
        y_related = y_scaled - ry

        # 在其他9个窗口相对位置执行鼠标按键操作
        for handle in sorted_chrome_windows:
            print("handle", handle)
            if handle == sorted_chrome_windows[0]:
                continue

            win32gui.SetForegroundWindow(handle)
            lParam = win32api.MAKELONG(x_related, y_related)  # 计算鼠标位置参数
            #win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
            win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32api.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

            #time.sleep(1)
        
        #win32api.SetCursorPos((x_related, y_related))

# 定义键盘监听函数
def on_press(key):
    if key == keyboard.Key.f9:  # 监听F9键按下事件
        # 退出程序
        print("exit...")
        mouse_listener.stop()
        keyboard_listener.stop()
        return False

# 创建鼠标监听器
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

# 创建键盘监听器
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# 进入消息循环
mouse_listener.join()
keyboard_listener.join()