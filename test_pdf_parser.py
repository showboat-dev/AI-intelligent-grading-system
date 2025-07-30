#!/usr/bin/env python
"""
PDF解析器测试脚本
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmp_platform.settings')
django.setup()

from questions.pdf_parser import PDFParser

def test_pdf_parser():
    """测试PDF解析器"""
    parser = PDFParser()
    
    # 测试文本解析
    test_text = """
    1. 项目管理中，以下哪个过程组负责制定项目章程？
    A. 启动过程组
    B. 规划过程组
    C. 执行过程组
    D. 监控过程组
    答案：A
    解析：项目章程是在启动过程组中制定的。
    
    2. 项目范围说明书包含以下哪些内容？
    A. 项目目标
    B. 项目可交付成果
    C. 项目约束条件
    D. 项目假设条件
    答案：ABCD
    解析：项目范围说明书包含项目目标、可交付成果、约束条件和假设条件。
    """
    
    print("测试题目解析...")
    questions = parser.parse_questions(test_text)
    print(f"解析到 {len(questions)} 道题目")
    
    for question in questions:
        print(f"题目 {question['question_number']}: {question['question_text'][:50]}...")
        print(f"选项: {question['options']}")
        print(f"正确答案: {question['correct_answers']}")
        print(f"题目类型: {question['question_type']}")
        print(f"解析: {question['explanation']}")
        print("-" * 50)
    
    # 测试答案解析
    test_answers_text = """
    1. 答案：A
    解析：项目章程是在启动过程组中制定的。
    
    2. 答案：ABCD
    解析：项目范围说明书包含项目目标、可交付成果、约束条件和假设条件。
    """
    
    print("\n测试答案解析...")
    answers = parser.parse_answers(test_answers_text)
    print(f"解析到 {len(answers)} 个答案")
    
    for question_number, answer in answers.items():
        print(f"题目 {question_number}: {answer['correct_answers']}")
        print(f"解析: {answer['explanation']}")
        print("-" * 30)

if __name__ == '__main__':
    test_pdf_parser() 