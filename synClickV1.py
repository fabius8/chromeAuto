import pyautogui
import time
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
import json

config = json.load(open('config.json'))
# 获取屏幕大小

screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)

# 4K显示器设置一般放大到150%，因为下面的菜单需要再缩小一部分
x_change = config["x_change"]
y_change = config["y_change"]
k = config["k"]

screenWidth = screenWidth * x_change
screenHeight = screenHeight * y_change
print(screenWidth, screenHeight)

# 设置Chrome浏览器窗口大小
chromeWidth = int(screenWidth / 5)
chromeHeight = int(screenHeight / 2)


# 假设每个窗口之间像素的间距, 4K显示器设置一般放大到150%
x_offset = int(chromeWidth * k)
y_offset = int(chromeHeight * k)
print("window size: ", x_offset, y_offset)
mymouse = Controller()

class MyListener(mouse.Listener, keyboard.Listener):
    def __init__(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.paused = False

    def on_click(self, x, y, button, pressed):
        #self.mouse_listener.stop()
        if self.paused:
            print("it is paused!")
            return
        print("on_click", x, y, button, pressed)
        if (x > x_offset) or (y > y_offset):
            print("skip")
            return True
        #time.sleep(0.1)
        if button == mouse.Button.left and not pressed:
            print("follow left click!", x, y)
            # 在所有窗口上点击相同的位置
            for i in range(1, 10):
                click_x = x + (i % 5) * x_offset
                click_y = y + (i // 5) * y_offset
                #print(click_x, click_y)
                mymouse.position = (click_x, click_y)
                mymouse.click(Button.left)
                #mymouse.release(Button.left)
                time.sleep(0.05)
                print(i, "click", click_x, click_y)
            mymouse.position = (x, y)
            

    def on_press(self, key): # 选择ESC作为暂停、继续键
        if key == keyboard.Key.esc:
            self.paused = not self.paused
            if self.paused:
                print("Paused")
            else:
                print("Resumed")

        elif key == keyboard.Key.f9:  # 选择F9作为退出键
            print("Exiting")
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            return False

    def start(self):
        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.keyboard_listener.join()
        self.mouse_listener.join()

if __name__ == "__main__":
    MyListener().start()