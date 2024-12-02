import psutil
import time

# 要查找的字符串
search_string = "\\USERDATA\\"
chrome_procs = []
filtered_lists = []

print("Searching for Chrome instances...")

for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    if 'chrome.exe' in proc.info['name']:
        chrome_procs.append(proc)

print(f"Found {len(chrome_procs)} Chrome instances.")

for chrome_proc in chrome_procs:
    if any(search_string in arg for arg in chrome_proc.cmdline()):
        filtered_list = [item for item in chrome_proc.cmdline() if '--user-data-dir' in item]
        filtered_lists.append(filtered_list)

filtered_lists = [tuple(x) for x in filtered_lists]
filtered_lists = list(set(filtered_lists))

# 对结果按照用户数据目录进行排序
filtered_lists.sort(key=lambda x: x[0])

print(f"\nFound {len(filtered_lists)} Chrome instances with '{search_string}' in the command line:")
for i, instance in enumerate(filtered_lists, start=1):
    print(f"{i}. {instance[0]}")

# 直接关闭所有符合条件的 Chrome 实例
for chrome_proc in chrome_procs:
    if any(search_string in arg for arg in chrome_proc.cmdline()):
        chrome_proc.terminate()

print("Closing all Chrome instances...")
time.sleep(2)
print("All Chrome instances closed.")
