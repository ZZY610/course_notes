import os

# 指定目标目录
directory_path = r"C:\Users\zhuzy51567\Desktop\ZGV201902.04.000脚本"

# 打开文本文件以写入绝对路径
with open("../fileList.txt", "w") as file:
    # 递归遍历目录及其子目录中的文件
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            # 获取文件的绝对路径并写入文本文件
            file_path = os.path.join(root, file_name)
            file.write(file_path + "\n")

print("文件路径已保存到fileList.txt")
