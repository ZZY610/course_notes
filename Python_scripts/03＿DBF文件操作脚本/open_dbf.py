#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DBF文件读取脚本
使用方法: python read_dbf.py
"""

import sys
from dbfread import DBF, DBFNotFound


def read_dbf_file(filename, encoding='gbk'):
    """
    读取DBF文件并打印所有记录

    参数:
        filename: DBF文件名（如 'GZ51579.DBF'）
        encoding: 文件编码，默认GBK（可尝试 'utf-8' 或 'gb2312'）
    """
    try:
        # 打开DBF文件
        print(f"正在打开文件: {filename}")
        print("=" * 50)

        table = DBF(filename, encoding=encoding, char_decode_errors='ignore')

        # 打印文件信息
        print(f"记录总数: {len(table)} 条")
        print(f"字段数量: {len(table.field_names)} 个")
        print("-" * 50)

        # 打印字段名（表头）
        print("字段列表:")
        for i, field in enumerate(table.fields, 1):
            print(f"  {i}. {field.name:<15} 类型: {field.type:<4} 长度: {field.length}")
        print("=" * 50)

        # 打印所有记录
        print("\n数据内容:")
        print("=" * 50)

        for index, record in enumerate(table, 1):
            print(f"\n【记录 #{index}】")
            for field_name in table.field_names:
                value = record[field_name]
                # 处理None值和字符串空格
                if value is None:
                    display_value = "NULL"
                elif isinstance(value, str):
                    display_value = value.strip()
                else:
                    display_value = value
                print(f"  {field_name:<15}: {display_value}")

            # 每打印10条记录暂停一次（防止刷屏）
            if index % 10 == 0:
                input("\n--- 按回车键继续显示下一页 ---")

        print("\n" + "=" * 50)
        print(f"✅ 所有 {len(table)} 条记录读取完成！")

    except DBFNotFound:
        print(f"❌ 错误: 文件 '{filename}' 不存在！")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 读取文件时出错: {str(e)}")
        print("\n建议尝试:")
        print("1. 检查文件名是否正确")
        print("2. 尝试修改 encoding 参数为 'utf-8' 或 'gb2312'")
        print("3. 确保文件未被其他程序占用")
        sys.exit(1)


if __name__ == "__main__":
    # DBF文件名（可修改）
    DBF_FILE = "D:\GZ51579.DBF"

    # 尝试读取（优先使用GBK编码）
    read_dbf_file(DBF_FILE, encoding='gbk')