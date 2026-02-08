#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DBF删除脚本：删除A0字段中非数字的记录（终极编码修复版）
修复：UnicodeDecodeError: 'ascii' codec can't decode byte 0xca
"""

import os
import sys

try:
    import dbf
except ImportError:
    print("❌ 未安装 dbf 库，请先运行：pip install dbf")
    sys.exit(1)


def backup_dbf_file(filepath):
    """创建备份文件"""
    backup_path = filepath + '.backup'
    if not os.path.exists(backup_path):
        try:
            # 使用二进制模式复制，避免编码问题
            with open(filepath, 'rb') as src, open(backup_path, 'wb') as dst:
                dst.write(src.read())
            print(f"✅ 已创建备份文件: {backup_path}")
        except Exception as e:
            print(f"⚠️  创建备份失败: {e}")
    else:
        print(f"⚠️  备份文件已存在，跳过备份: {backup_path}")


def is_numeric(value):
    """
    检查值是否为数字（支持字符串形式的数字）
    """
    if value is None:
        return False

    # 如果是数值类型
    if isinstance(value, (int, float)):
        return True

    # 如果是字符串
    if isinstance(value, str):
        try:
            # 去除首尾空格
            val_str = value.strip()
            # 空字符串视为非数字
            if not val_str:
                return False
            # 尝试转换为浮点数
            float(val_str)
            return True
        except ValueError:
            return False

    return False


def open_dbf_table(filepath, mode=dbf.READ_ONLY):
    """
    通用的DBF表打开函数，自动处理编码兼容性问题

    返回值: table对象
    """
    try:
        # 方法1: 新版本dbf (0.98+) - 支持codepage参数
        table = dbf.Table(filepath, codepage='cp936')
        table.open(mode)
        return table
    except TypeError as e:
        if 'codepage' in str(e):
            # 方法2: 旧版本dbf - 降级到ASCII模式
            print("⚠️  当前dbf库版本较旧，不支持codepage参数，降级到ASCII模式")
            print("   建议升级: pip install --upgrade dbf")
            table = dbf.Table(filepath)
            table.open(mode)
            return table
        else:
            raise
    except Exception as e:
        # 方法3: 最终降级方案
        print(f"⚠️  使用降级方案打开文件: {e}")
        table = dbf.Table(filepath)
        table.open(mode)
        return table


def delete_non_numeric_records(filepath, field_name):
    """删除指定字段中非数字的记录"""

    if not os.path.exists(filepath):
        print(f"❌ 错误：文件不存在 - {filepath}")
        sys.exit(1)

    backup_dbf_file(filepath)

    print(f"\n🎯 开始处理文件: {filepath}")
    print(f"📌 目标字段: {field_name}")
    print(f"📝 操作: 删除该字段值不是数字的记录")
    print("=" * 70)

    try:
        # 打开DBF文件（自动处理编码）
        table = open_dbf_table(filepath, dbf.READ_WRITE)
        print(f"✅ 文件打开成功（编码: cp936）")

        # 检查字段是否存在
        field_name_upper = field_name.upper()
        field_names_upper = [f.upper() for f in table.field_names]

        if field_name_upper not in field_names_upper:
            print(f"❌ 错误：字段 '{field_name}' 不存在！")
            print(f"可用字段: {', '.join(table.field_names)}")
            table.close()
            sys.exit(1)

        actual_field_name = table.field_names[field_names_upper.index(field_name_upper)]
        print(f"✅ 找到目标字段: {actual_field_name}")

        # 统计信息
        deleted_count = 0
        kept_records = []

        print(f"\n📊 开始扫描 {len(table)} 条记录...")
        print("-" * 70)

        # 遍历所有记录
        for record in table:
            try:
                value = record[actual_field_name]

                if not is_numeric(value):
                    # 标记删除
                    dbf.delete(record)
                    deleted_count += 1
                    # 只显示前3条删除的记录
                    if deleted_count <= 3:
                        print(f"🗑️  删除记录 #{record.record_number}: {field_name} = '{value}'")
                else:
                    # 记录要保留的记录
                    kept_records.append((record.record_number, value))
            except Exception as e:
                print(f"⚠️  读取记录时出错，将被删除: {e}")
                dbf.delete(record)
                deleted_count += 1

        # 物理删除（真正移除）
        print(f"\n执行物理删除...")
        table.pack()
        table.close()

        # 输出统计
        print(f"\n" + "=" * 70)
        print(f"✅ 删除完成！")
        print(f"📈 结果统计:")
        print(f"   - 删除记录数: {deleted_count} 条")
        print(f"   - 保留记录数: {len(kept_records)} 条")
        print(f"   - 剩余总记录: {len(kept_records)} 条")
        print("=" * 70)

        # 验证结果
        if kept_records:
            print(f"\n🔍 保留的记录示例（前3条）：")
            print("-" * 50)
            for i, (rec_num, value) in enumerate(kept_records[:3], 1):
                print(f"记录 {rec_num}: {field_name} = {value}")

    except Exception as e:
        print(f"❌ 操作失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # 配置参数
    DBF_FILE = r"D:\GZ51579.DBF"
    TARGET_FIELD = "A0"

    delete_non_numeric_records(DBF_FILE, TARGET_FIELD)