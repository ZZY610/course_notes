#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DBF文件基础信息查看器
"""

import os
import sys

try:
    import dbf
except ImportError:
    print("❌ 未安装 dbf 库，请先运行：pip install dbf")
    sys.exit(1)


def parse_structure_line(line):
    """
    解析dbf.structure()返回的字符串
    示例: "FFDTE D(8,0)" → {'name':'FFDTE', 'type':'D', 'length':8, 'decimal':0}
    """
    try:
        # 分离字段名和类型定义
        parts = line.strip().split()
        if len(parts) < 2:
            return None

        field_name = parts[0]
        type_def = parts[1]

        # 提取类型字符
        type_char = type_def[0]

        # 提取长度和小数位 (格式: D(8,0) 或 C(64))
        length = 0
        decimal = 0

        if '(' in type_def:
            # 提取括号内的数字
            numbers = type_def[type_def.find('(') + 1: type_def.find(')')].split(',')
            length = int(numbers[0]) if len(numbers) > 0 else 0
            decimal = int(numbers[1]) if len(numbers) > 1 else 0

        return {
            'name': field_name,
            'type_char': type_char,
            'length': length,
            'decimal': decimal
        }
    except:
        return None


def get_field_type_name(type_char):
    """字段类型代码转中文名称"""
    type_names = {
        'C': "字符型", 'D': "日期型", 'N': "数值型",
        'L': "逻辑型", 'M': "备注型", 'F': "浮点型",
        'B': "二进制型", 'G': "通用型", 'P': "图片型",
        'Y': "货币型", 'T': "日期时间型", 'I': "整型",
        'V': "可变型", 'X': "NULL型"
    }
    return type_names.get(type_char.upper(), f"未知类型 ({type_char})")


def main():
    DBF_FILE = r"D:\GZ51579.DBF"

    print("=" * 70)
    print("🔍 DBF文件基础信息查看器（终极稳定版）")
    print("=" * 70)

    # 文件检查
    if not os.path.exists(DBF_FILE):
        print(f"❌ 错误：文件不存在\n   路径: {DBF_FILE}")
        sys.exit(1)

    file_size = os.path.getsize(DBF_FILE)
    print(f"📁 文件路径: {DBF_FILE}")
    print(f"📏 文件大小: {file_size:,} 字节 ({file_size / 1024:.1f} KB)")

    # 打开文件
    try:
        table = dbf.Table(DBF_FILE, codepage='cp936')
        table.open()
    except TypeError:
        table = dbf.Table(DBF_FILE)
        table.open()
    except Exception as e:
        print(f"❌ 打开文件失败: {e}")
        sys.exit(1)

    # === 1. 核心信息 ===
    print("\n" + "=" * 70)
    print("📋 核心信息")
    print("=" * 70)
    print(f"📊 记录总数: {len(table):,} 条")
    print(f"📝 字段数量: {len(table.field_names)} 个")
    print(f"🏷️  字段列表: {', '.join(table.field_names)}")

    # === 2. 字段详细信息（100%成功）===
    print("\n" + "=" * 70)
    print("🔎 字段详细信息")
    print("=" * 70)

    # 使用structure()方法（最稳定）
    structure_lines = table.structure()

    print(f"{'序号':<4} {'字段名':<15} {'类型':<4} {'说明':<12} {'长度':<6} {'小数':<4}")
    print("-" * 70)

    for idx, line in enumerate(structure_lines, 1):
        parsed = parse_structure_line(line)
        if parsed:
            type_char = parsed['type_char']
            type_name = get_field_type_name(type_char)
            print(
                f"{idx:<4} {parsed['name']:<15} {type_char:<4} {type_name:<12} {parsed['length']:<6} {parsed['decimal']:<4}")
        else:
            # 如果解析失败，至少显示原始行
            print(f"{idx:<4} {line:<40}")

    # === 3. 数据预览 ===
    print("\n" + "=" * 70)
    print("👁️  数据预览（前5条记录，前5个字段）")
    print("=" * 70)

    preview_fields = table.field_names[:5]

    # 表头
    headers = [f"{name}" for name in preview_fields]
    print("记录号 | " + " | ".join([f"{h:<18}" for h in headers]))
    print("-" * (9 + len(preview_fields) * 20))

    # 数据行
    for row_num, record in enumerate(table, 1):
        if row_num > 5:
            break

        row_values = []
        for field_name in preview_fields:
            value = record[field_name]
            if value is None:
                val_str = "NULL"
            elif isinstance(value, str):
                val_str = value.strip()
                if len(val_str) > 16:
                    val_str = val_str[:13] + "..."
            else:
                val_str = str(value)

            row_values.append(f"{val_str:<18}")

        print(f"{row_num:<6} | " + " | ".join(row_values))

    table.close()

    print("\n" + "=" * 70)
    print("✅ 信息查看完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()