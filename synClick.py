import win32gui
import win32con
import win32api
import psutil
import win32process
import re
import time
import json
import win32clipboard

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

# 定义变量来保存上一次点击的位置
last_click_position = (0, 0)


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
    #wParam = win32api.MAKELONG(0, 120)
    #lParam = win32api.MAKELONG(x + w // 2, y + h // 2)  # 计算鼠标位置参数
    #win32api.SendMessage(hwnd, win32con.WM_PASTE, 0, 0)


""" for handle in sorted_chrome_windows:
    print("handle", handle)
    print("follow scroll", -1 * 120)
    win32gui.SetForegroundWindow(handle)
    win32api.SendMessage(handle, win32con.WM_MOUSEWHEEL, 120, 0) """



# 定义鼠标点击监听函数
def on_click(x, y, button, pressed):
    global last_click_position
    if pressed:
        last_click_position = (x, y)
        print(f"Clicked at {last_click_position}")

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

            #win32gui.SetForegroundWindow(handle)
            lParam = win32api.MAKELONG(x_related, y_related)  # 计算鼠标位置参数
            #win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
            win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32api.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

            #time.sleep(1)
        
        #win32api.SetCursorPos((x_related, y_related))

# 定义键盘监听函数
def on_press(key):
    if isinstance(key, keyboard.KeyCode):

        rect = win32gui.GetWindowRect(sorted_chrome_windows[0])
        rx = rect[0]
        ry = rect[1]
        rw = rect[2] - rx
        rh = rect[3] - ry
        
        # 对位置和大小进行150%缩放
        x_scaled = int(last_click_position[0] / k)
        y_scaled = int(last_click_position[1] / k)
        print(rx, ry, rw, rh, x_scaled, y_scaled)
        if (x_scaled < rx) or (x_scaled > (rx + rw)) or (y_scaled < ry) or (y_scaled > (ry + rh)):
            print("not win#1, skip")
            return
        
        # 普通按键
        print('普通按键:', key.char)
        vk_code = ord(key.char)   # 获取按键对应的虚拟键码
        print('键码', vk_code)
        for handle in sorted_chrome_windows:
            #print("handle", handle)
            if handle == sorted_chrome_windows[0]:
                continue
            win32api.SendMessage(handle, win32con.WM_CHAR, vk_code, 0)  # 发送按键按下消息
            #win32api.SendMessage(handle, win32con.WM_KEYUP, vk_code, 0)  # 发送按键释放消息
        
        # 
        if str(key) == r"'\x16'": # ctrl + v
            print("ctrl+v paste press")
            for handle in sorted_chrome_windows:
                print("handle", handle)
                if handle == sorted_chrome_windows[0]:
                    continue
                #win32gui.SetForegroundWindow(handle)
                # win32clipboard.OpenClipboard()
                # data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                # print(data)
                # win32clipboard.CloseClipboard()
                # win32gui.SendMessage(handle, win32con.WM_PASTE, 0, "data")

                win32api.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)  # 发送按键按下消息
                win32api.SendMessage(handle, win32con.WM_KEYDOWN, 0x56, 0)
                win32api.SendMessage(handle, win32con.WM_KEYUP, 0x56, 0)
                win32api.SendMessage(handle, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)  # 发送按键按下消息
                #time.sleep(0.5)




    elif key in [Key.enter, Key.shift, Key.ctrl_l, Key.alt_l, Key.f9, Key.backspace]:
        # 特殊按键
        print('special key {0} pressed'.format(key))
        if key == Key.f9:  # 监听F9键按下事件
            # 退出程序
            print("exit...")
            mouse_listener.stop()
            keyboard_listener.stop()
            return False

        if key == Key.backspace or key == Key.enter:
            rect = win32gui.GetWindowRect(sorted_chrome_windows[0])
            rx = rect[0]
            ry = rect[1]
            rw = rect[2] - rx
            rh = rect[3] - ry
            
            # 对位置和大小进行150%缩放
            x_scaled = int(last_click_position[0] / k)
            y_scaled = int(last_click_position[1] / k)
            print(rx, ry, rw, rh, x_scaled, y_scaled)
            if (x_scaled < rx) or (x_scaled > (rx + rw)) or (y_scaled < ry) or (y_scaled > (ry + rh)):
                print("not win#1, skip")
                return

        for handle in sorted_chrome_windows:
            #print("handle", handle)
            if handle == sorted_chrome_windows[0]:
               continue
            if key == Key.enter:
                win32api.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  # 发送按键按下消息
                win32api.SendMessage(handle, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送按键释放消息
            if key == Key.backspace:
                win32api.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_BACK, 0)  # 发送按键按下消息
                win32api.SendMessage(handle, win32con.WM_KEYUP, win32con.VK_BACK, 0)  # 发送按键释放消息

    else:
        # 其他按键
        print('其他按键')



def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y, dx, dy)))
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
    
    for handle in sorted_chrome_windows:
        print("handle", handle)
        if handle == sorted_chrome_windows[0]:
            continue
        rect = win32gui.GetWindowRect(handle)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        print("follow scroll", dy * 120)
        win32gui.SetForegroundWindow(handle)
        wParam = win32api.MAKELONG(0, dy*120)
        lParam = win32api.MAKELONG(x + x_related, y + y_related)
        win32api.SendMessage(handle, win32con.WM_MOUSEWHEEL, wParam, lParam)

# 创建鼠标监听器
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
mouse_listener.start()

# 创建键盘监听器
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# 进入消息循环
mouse_listener.join()
keyboard_listener.join()