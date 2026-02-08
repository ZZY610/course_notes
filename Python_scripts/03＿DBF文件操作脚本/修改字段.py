#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DBF文件字段批量修改脚本（终极版）
功能：将指定字段的所有值改为固定日期
使用方法：python modify_dbf_date_ultimate.py
"""

import os
import sys
from datetime import date

try:
    import dbf
except ImportError:
    print("❌ 未安装 dbf 库，请先运行：pip install dbf")
    sys.exit(1)


def backup_dbf_file(filepath):
    """创建备份文件"""
    backup_path = filepath + '.backup'
    if not os.path.exists(backup_path):
        with open(filepath, 'rb') as src, open(backup_path, 'wb') as dst:
            dst.write(src.read())
        print(f"✅ 已创建备份文件: {backup_path}")
    else:
        print(f"⚠️  备份文件已存在，跳过备份: {backup_path}")


def get_field_type_char(field_info):
    """
    从FieldInfo对象中提取字段类型字符
    支持多种返回格式：FieldInfo命名元组、元组、整数ASCII码
    """
    # 如果是FieldInfo命名元组
    if hasattr(field_info, 'type'):
        type_value = field_info.type
    # 如果是普通元组/列表
    elif isinstance(field_info, (tuple, list)):
        type_value = field_info[0]
    else:
        type_value = field_info

    # 转换ASCII码整数为字符（68 -> 'D'）
    if isinstance(type_value, int):
        return chr(type_value)

    return str(type_value)


def modify_dbf_date_field(filepath, field_name, new_date):
    """
    批量修改DBF文件中指定日期字段的值
    """

    # 检查文件是否存在
    if not os.path.exists(filepath):
        print(f"❌ 错误：文件不存在 - {filepath}")
        sys.exit(1)

    # 创建备份
    backup_dbf_file(filepath)

    print(f"\n🎯 开始修改文件: {filepath}")
    print(f"📅 目标字段: {field_name}")
    print(f"📝 新日期值: {new_date}")
    print("=" * 50)

    try:
        # 以读写模式打开DBF文件
        table = dbf.Table(filepath)
        table.open(dbf.READ_WRITE)

        # 检查字段是否存在（不区分大小写）
        field_name_upper = field_name.upper()
        field_names_upper = [f.upper() for f in table.field_names]

        if field_name_upper not in field_names_upper:
            print(f"❌ 错误：字段 '{field_name}' 不存在！")
            print(f"可用字段: {', '.join(table.field_names)}")
            table.close()
            sys.exit(1)

        # 获取实际字段名（保留原始大小写）
        actual_field_name = table.field_names[field_names_upper.index(field_name_upper)]

        # 获取字段信息并判断类型
        field_info = table.field_info(actual_field_name)
        field_type = get_field_type_char(field_info)

        if field_type != 'D':
            print(f"❌ 错误：字段 '{field_name}' 不是日期类型（当前类型: {field_type} - {field_info}）")
            table.close()
            sys.exit(1)

        print(f"✅ 字段验证通过: {field_name} 是日期类型")

        # 统计修改记录数
        modified_count = 0

        # 遍历并修改所有记录
        for record in table:
            # 修改记录的值
            with record as r:
                r[actual_field_name] = new_date
                modified_count += 1

        # 关闭表（自动保存）
        table.close()

        print(f"✅ 修改成功！共 {modified_count} 条记录被更新")
        print("=" * 50)

        # 验证修改结果
        print("\n🔍 验证修改结果（显示前3条记录）：")
        verify_table = dbf.Table(filepath)
        verify_table.open()
        for i, record in enumerate(verify_table, 1):
            if i > 3:
                break
            print(f"  记录 #{i}: {field_name} = {record[field_name]}")
        verify_table.close()

    except Exception as e:
        print(f"❌ 修改失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # 配置参数
    DBF_FILE = r"D:\GZ51579.DBF"  # 文件路径
    TARGET_FIELD = "Ffdate"  # 要修改的字段名
    NEW_DATE = date(2025, 12, 2)  # 新日期值

    # 执行修改
    modify_dbf_date_field(DBF_FILE, TARGET_FIELD, NEW_DATE)