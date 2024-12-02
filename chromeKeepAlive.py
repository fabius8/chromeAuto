# chrome_loop.py
import subprocess
import time
import sys

def run_chrome(number):
    print(f"正在启动 Chrome {number}")
    # 启动 Chrome
    subprocess.run(['python', 'chromeStart_v2.py', str(number)])
    
    # 等待10秒
    print(f"等待10秒...")
    time.sleep(10)
    
    # 关闭 Chrome
    print(f"正在关闭 Chrome {number}")
    subprocess.run(['python', 'chromeClose.py'])
    
    # 额外等待2秒确保完全关闭
    time.sleep(2)

def main():
    # 如果提供了命令行参数，使用参数作为起始数字
    start_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    end_num = 100
    
    for num in range(start_num, end_num + 1):
        print(f"\n=== 处理第 {num} 个Chrome ===")
        run_chrome(num)
        print(f"=== 完成第 {num} 个Chrome ===\n")

if __name__ == "__main__":
    main()
