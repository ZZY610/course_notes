from pathlib import Path
def remove_prefix_and_suffix(directory_path, prefix='', suffix=''):
    # 创建Path对象
    directory = Path(directory_path)
    # 获取目录下所有文件
    files = directory.glob('*')
    # 遍历文件
    for file in files:
        # 获取文件名
        filename = file.name
        # 检查是否有前缀需要删除
        if prefix and filename.startswith(prefix):
            new_name = filename[len(prefix):]  # 删除前缀
            file.rename(directory / new_name)
        # 检查是否有后缀需要删除
        if suffix and filename.endswith(suffix):
            new_name = filename[:-len(suffix)]  # 删除后缀
            file.rename(directory / new_name)
if __name__ == "__main__":
    # 输入目录路径
    directory_path = input("请输入目录的路径：")

    # 输入要删除的前缀和后缀
    prefix = input("请输入要删除的前缀（如果没有，请直接按回车键）：")
    suffix = input("请输入要删除的后缀（如果没有，请直接按回车键）：")

    # 调用函数删除前缀和后缀
    remove_prefix_and_suffix(directory_path, prefix, suffix)
