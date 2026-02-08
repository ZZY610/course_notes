#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
项目名称: 文件统计工具
模块名称: 文件统计模块
文件名称: file_stats.py
作者: [你的姓名]
创建日期: 2024-11-11
版本: 1.0
描述: 统计文件的行数、字数和字符数。
"""

import os
import sys
import logging
import argparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_stats.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='统计文件的行数、字数和字符数')
    parser.add_argument('file_path', type=str, help='要统计的文件路径')
    return parser.parse_args()

def count_lines_words_chars(file_path):
    """统计文件的行数、字数和字符数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            line_count = len(content.splitlines())
            word_count = len(content.split())
            char_count = len(content)
            return line_count, word_count, char_count
    except Exception as e:
        logger.error(f'读取文件出错: {e}')
        sys.exit(1)


def main(args):
    """主函数"""
    try:
        logger.info(f'开始统计文件: {args.file_path}')
        if not os.path.exists(args.file_path):
            logger.error(f'文件不存在: {args.file_path}')
            sys.exit(1)

        line_count, word_count, char_count = count_lines_words_chars(args.file_path)
        logger.info(f'统计完成: 行数={line_count}, 字数={word_count}, 字符数={char_count}')
    except Exception as e:
        logger.error(f'脚本执行出错: {e}')
        sys.exit(1)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)