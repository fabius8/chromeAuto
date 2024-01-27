import psutil
import time

# 要查找的字符串
search_string = "\\USERDATA\\" 
chrome_procs = []
filtered_lists = []
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    if 'chrome.exe' in proc.info['name']:
        chrome_procs.append(proc)

for chrome_proc in chrome_procs:
    if any(search_string in arg for arg in chrome_proc.cmdline()):
        filtered_list = [item for item in chrome_proc.cmdline() if '--user-data-dir' in item]

        filtered_lists.append(filtered_list)
        chrome_proc.terminate()

filtered_lists = [tuple(x) for x in filtered_lists]
filtered_lists = list(set(filtered_lists))
print("close...")
print(filtered_lists)