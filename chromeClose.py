import psutil
import os
from concurrent.futures import ThreadPoolExecutor
import time

def kill_proc(pid):
    """强制结束单个进程"""
    try:
        os.kill(pid, 9)
        return True
    except:
        return False

def find_and_kill_chrome():
    search_string = "\\USERDATA\\"
    chrome_processes = []
    
    # 查找符合条件的Chrome进程
    print("查找Chrome进程...")
    start_time = time.time()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'chrome.exe' in proc.info['name']:
                cmdline = proc.cmdline()
                if any(search_string in arg for arg in cmdline):
                    # 找到包含USERDATA的参数
                    userdata_path = next((arg for arg in cmdline if search_string in arg), None)
                    chrome_processes.append({
                        'pid': proc.pid,
                        'userdata': userdata_path
                    })
        except:
            continue
    
    count = len(chrome_processes)
    if count == 0:
        print("未找到Chrome进程")
        return
    
    print(f"\n找到 {count} 个Chrome进程:")
    for i, proc in enumerate(chrome_processes, 1):
        print(f"{i}. PID: {proc['pid']} - UserData: {proc['userdata']}")
    
    # 并行关闭进程
    print("\n开始关闭进程...")
    pids = [p['pid'] for p in chrome_processes]
    with ThreadPoolExecutor(max_workers=min(count, 10)) as executor:
        results = list(executor.map(kill_proc, pids))
    
    closed = sum(1 for r in results if r)
    end_time = time.time()
    
    print(f"\n成功关闭 {closed}/{count} 个Chrome进程")
    print(f"耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    try:
        find_and_kill_chrome()
    except Exception as e:
        print(f"发生错误: {str(e)}")
