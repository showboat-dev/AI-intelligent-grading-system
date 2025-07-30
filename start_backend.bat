@echo off
echo 启动PMP智能做题平台后端服务...
cd backend

REM 检查虚拟环境是否存在
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo 创建虚拟环境失败，请检查Python是否正确安装
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate
if errorlevel 1 (
    echo 激活虚拟环境失败
    pause
    exit /b 1
)

REM 升级pip
echo 升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 安装项目依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 依赖安装失败，尝试逐个安装...
    pip install Django==4.2.7
    pip install djangorestframework==3.14.0
    pip install django-cors-headers==4.3.1
    pip install PyPDF2==3.0.1
    pip install pdfplumber==0.9.0
    pip install python-dotenv==1.0.0
    pip install Pillow==10.1.0
)

REM 运行数据库迁移
echo 运行数据库迁移...
python manage.py migrate

REM 启动服务器
echo 启动Django服务器...
python manage.py runserver

pause 