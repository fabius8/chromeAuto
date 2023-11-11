import subprocess
import time
import pyautogui
import os

# 获取屏幕大小
screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

# 4K显示器设置一般放大到150%，这里有微调
x_change = 0.65
y_change = 0.64

screenWidth = screenWidth * x_change
screenHeight = screenHeight * y_change
print(screenWidth, screenHeight)

# 设置Chrome浏览器窗口大小
chromeWidth = int(screenWidth / 5)
chromeHeight = int(screenHeight / 2)
window_size_str = "--window-size={},{}".format(chromeWidth, chromeHeight)
print(window_size_str)
#os.exit()

rangeList = []
# 从第1个到第10个
range_A = input("请输入一个或多个整数（以空格分隔）：").strip().split()

if len(range_A) == 1:
    # 如果只有一个元素，则将它转换成整数
    range_A = [int(range_A[0])]
    print(range_A)
    range_B = input("请输入结束范围：")
    if range_B:
        range_B = int(range_B)
    else:
        range_B = range_A[0]
    print(range_B)
    rangeList = list(range(range_A[0], range_B + 1))
else:
    # 如果有多个元素，则将它们全部转换成整数
    rangeList = [int(i) for i in range_A]


portbase = 9200


app = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
parameter = [
    window_size_str,
    "--no-message-box",
    "--no-first-run",
    "--no-default-browser-check",
    "--no-restore-session-state",
    "--disable-session-crashed-bubble",
    "--hide-crash-restore-bubble"
]

for index, i  in enumerate(rangeList):
    n = index
    if n <= 4:
        windows_x_position = n * chromeWidth
        windows_y_position = 0
    else:
        windows_x_position = (n - 5) * chromeWidth
        windows_y_position = chromeHeight
    window_positon_str = "--window-position={},{}".format(windows_x_position, windows_y_position)
    print(window_positon_str)

    port = portbase + i
    cwd = os.getcwd()  # 获取当前工作目录
    usedatadir = "--user-data-dir=" + cwd +  "\\USERDATA\\" + f'{i:04}'
    print(usedatadir)
    debugport = f"--remote-debugging-port={port}"

    chrome_args = f"{app} {usedatadir} {debugport} {' '.join(parameter)} {window_positon_str}"
    subprocess.Popen(chrome_args)
    time.sleep(0.5)   # 等待 Chrome 加载完成
    #pyautogui.hotkey('alt', 'shift', 'o')  # 模拟按下 Alt+Shift+O 快捷键
    #pyautogui.hotkey('s')  # 模拟键盘输入数字 切换到正常
