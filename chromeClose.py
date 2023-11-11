import psutil
import time

# 要查找的字符串
search_string = "\\USERDATA\\" 
chrome_procs = []

for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    if 'chrome.exe' in proc.info['name']:
        chrome_procs.append(proc)

for chrome_proc in chrome_procs:
    if any(search_string in arg for arg in chrome_proc.cmdline()):
        #print(chrome_proc.cmdline())
        chrome_proc.terminate()