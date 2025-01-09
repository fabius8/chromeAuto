import win32gui
import win32con
import time
import re
import win32process
import psutil


class WindowArranger:
    def __init__(self):
        # 窗口布局配置
        self.WINDOW_WIDTH = 525
        self.WINDOW_HEIGHT = 741
        self.MARGIN_X = 10
        self.START_X = 10
        self.START_Y = 10
        self.ROWS = 2
        self.COLS = 5
        
        self.positions = self._calculate_positions()
        print("初始化位置列表:")
        for pos in self.positions:
            print(f"位置: x={pos[0]}, y={pos[1]}, row={pos[2]}, col={pos[3]}")

    def _calculate_positions(self):
        """计算所有窗口位置，按行优先排列"""
        positions = []
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = self.START_X + col * (self.WINDOW_WIDTH + self.MARGIN_X)
                y = self.START_Y + row * self.WINDOW_HEIGHT + (row * 20)
                positions.append((x, y, row, col))
        return positions

    def _get_userdata_from_pid(self, pid):
        """从进程ID获取UserData编号"""
        try:
            proc = psutil.Process(pid)
            cmdline = proc.cmdline()
            print(f"进程 {pid} 的命令行: {cmdline}")
            
            for arg in cmdline:
                if '--user-data-dir=' in arg:
                    match = re.search(r'USERDATA[/\\](\d{4})', arg)
                    if match:
                        num = int(match.group(1))
                        print(f"找到UserData编号: {num}")
                        return num
            print(f"进程 {pid} 未找到UserData编号")
            return 9999
        except Exception as e:
            print(f"获取进程 {pid} 信息时出错: {str(e)}")
            return 9999

    def _window_enum_callback(self, hwnd, windows):
        """枚举窗口回调函数"""
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Chrome" in title and title != "":
                # 获取窗口对应的进程ID
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                userdata_num = self._get_userdata_from_pid(pid)
                windows.append((hwnd, title, userdata_num))
                print(f"找到Chrome窗口: hwnd={hwnd}, pid={pid}, userdata={userdata_num}, title={title}")

    def get_chrome_windows(self):
        """获取所有Chrome窗口并按UserData编号排序"""
        windows = []
        win32gui.EnumWindows(self._window_enum_callback, windows)
        sorted_windows = sorted(windows, key=lambda x: x[2])
        print("\n排序后的窗口列表:")
        for hw, title, num in sorted_windows:
            print(f"UserData={num:04d}, hwnd={hw}, title={title}")
        return sorted_windows

    def arrange_windows(self):
        """重新排列所有Chrome窗口"""
        windows = self.get_chrome_windows()
        print(f"\n找到 {len(windows)} 个Chrome窗口，开始重新排列...")

        # 计算每行应该放置的窗口数量
        windows_per_row = self.COLS

        for i, (hwnd, title, userdata_num) in enumerate(windows):
            # 计算当前窗口应该在的行和列
            row = i // windows_per_row
            col = i % windows_per_row
            
            # 计算窗口位置
            x = self.START_X + col * (self.WINDOW_WIDTH + self.MARGIN_X)
            y = self.START_Y + row * self.WINDOW_HEIGHT + (row * 20)
            
            print(f"\n准备移动窗口: UserData={userdata_num:04d}")
            print(f"位置计算: index={i}, row={row}, col={col}, x={x}, y={y}")
            
            try:
                # 设置窗口位置和大小
                win32gui.SetWindowPos(
                    hwnd,
                    win32con.HWND_TOP,
                    x, y,
                    self.WINDOW_WIDTH,
                    self.WINDOW_HEIGHT,
                    win32con.SWP_SHOWWINDOW
                )
                print(f"✓ 已移动窗口到 [{x}, {y}] (行{row+1},列{col+1}): UserData {userdata_num:04d} - {title}")
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"移动窗口失败 (UserData {userdata_num:04d}): {str(e)}")

if __name__ == "__main__":
    print("开始重新排列Chrome窗口...")
    
    try:
        arranger = WindowArranger()
        arranger.arrange_windows()
        print("重排完成！")
    except Exception as e:
        print(f"发生错误: {str(e)}")