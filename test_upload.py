#!/usr/bin/env python
"""
上传API测试脚本
"""
import os
import sys
import django
import tempfile

# 设置Django环境
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmp_platform.settings')
django.setup()

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from questions.views import FileUploadView
from rest_framework.test import APIRequestFactory
from rest_framework import status

def create_test_pdf():
    """创建测试PDF文件"""
    # 创建一个简单的PDF内容（这里只是示例）
    pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF'
    
    return SimpleUploadedFile(
        "test_questions.pdf",
        pdf_content,
        content_type="application/pdf"
    )

def test_upload_api():
    """测试上传API"""
    factory = APIRequestFactory()
    
    # 创建测试文件
    questions_file = create_test_pdf()
    answers_file = create_test_pdf()
    
    # 创建请求数据
    data = {
        'title': '测试题目集合',
        'questions_file': questions_file,
        'answers_file': answers_file,
    }
    
    # 创建请求
    request = factory.post('/api/upload/', data, format='multipart')
    
    # 创建视图实例
    view = FileUploadView.as_view()
    
    try:
        # 调用视图
        response = view(request)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.data}")
        
        if response.status_code == status.HTTP_201_CREATED:
            print("✅ 上传成功！")
        else:
            print("❌ 上传失败！")
            
    except Exception as e:
        print(f"❌ 发生异常: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    test_upload_api() 