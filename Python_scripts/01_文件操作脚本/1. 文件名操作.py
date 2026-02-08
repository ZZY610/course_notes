import pathlib as pb
from pathlib import Path
import os

def list_functions():
    """列出所有功能"""
    print("1. 获取指定目录下所有文件的绝对路径并写入指定文件")
    print("2. 批量按照指定简单规则修改某目录下文件名")
    print("3. 确认目标目录下是否存在目标文件")
    # 添加其他功能...

def get_absolute_paths(directory, output_file):
    """获取指定目录下所有文件的绝对路径并写入指定文件"""
    # 指定目标目录的路径
    # directory_path = input("输入目标路径：")
    # target_path = input("你想把这个文件存在哪里？输入目标路径：")
    # 打开文本文件以写入绝对路径
    # "with" 块用于自动关闭文件，无论是否出现异常
    # "w" 表示以写入模式打开文件，如果文件已存在，将会被覆盖
    with open(Path(output_file+r"\fileList.txt").resolve(), "w",encoding="utf-8") as file:
        # 递归遍历目录及其子目录中的文件
        # os.walk() 返回一个生成器，每次迭代返回一个元组(root, dirs, files)
        # root 是当前目录的路径
        # dirs 是当前目录下的子目录列表
        # files 是当前目录下的文件列表
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                # 获取文件的绝对路径
                file_path = os.path.join(root, file_name)

                # 将文件的绝对路径写入文本文件，并添加换行符
                file.write(file_path + "\n")

    # 打印一条消息，指示文件路径已保存到 "fileList.txt" 中
    print("文件路径已保存到fileList.txt")

def batch_rename_files(directory, rule):
    """批量按照指定简单规则修改某目录下文件名"""

def confirm_target_file(directory:Path, file:str) -> bool:
# 确认目标目录下是否存在目标文件
    if Path(directory/file).exists() == True:
        print('存在')
    else:
        print('不存在')
    return 0

def main():
    print("欢迎使用目录文件名操作脚本！")

    while True:
        list_functions()
        choice = input("请输入功能号 (输入 q 退出): ")

        if choice == '1':
            directory = input("请输入目录路径: ")
            output_file = input("请输入输出文件路径: ")
            get_absolute_paths(directory, output_file)
        elif choice == '2':
            directory = input("请输入目录路径: ")
            rule = input("请输入修改规则: ")
            batch_rename_files(directory, rule)
        elif choice == '3':
            print("你想使用当前目录的路径吗？如果是，请按1，否则按2")
            directory = input("请输入目录路径: ")
            file=input("请输入文件名: ")
            confirm_target_file(Path(directory),file)
        elif choice.lower() == 'q':
            print("感谢使用，再见！")
            break
        else:
            print("无效的功能号，请重新输入。")

if __name__ == "__main__":
    main()
