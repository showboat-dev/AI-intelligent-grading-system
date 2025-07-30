@echo off
echo 安装项目依赖...
cd backend

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate

REM 升级pip和setuptools
echo 升级pip和setuptools...
python -m pip install --upgrade pip setuptools wheel

REM 逐个安装依赖，避免版本冲突
echo 安装Django...
pip install Django==4.2.7

echo 安装Django REST Framework...
pip install djangorestframework==3.14.0

echo 安装CORS headers...
pip install django-cors-headers==4.3.1

echo 安装PDF处理库...
pip install PyPDF2==3.0.1
pip install pdfplumber==0.9.0

echo 安装其他依赖...
pip install python-dotenv==1.0.0
pip install Pillow==10.1.0

echo 验证安装...
python -c "import django; print('Django版本:', django.get_version())"
python -c "import rest_framework; print('DRF已安装')"
python -c "import corsheaders; print('CORS headers已安装')"

echo 依赖安装完成！
pause 