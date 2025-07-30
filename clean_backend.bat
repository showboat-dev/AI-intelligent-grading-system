@echo off
echo 清理后端环境...
cd backend

REM 删除虚拟环境
if exist "venv" (
    echo 删除现有虚拟环境...
    rmdir /s /q venv
)

REM 删除数据库文件（可选）
if exist "db.sqlite3" (
    echo 删除数据库文件...
    del db.sqlite3
)

REM 删除Python缓存文件
if exist "__pycache__" (
    echo 删除Python缓存文件...
    rmdir /s /q __pycache__
)

echo 清理完成！现在可以重新运行 start_backend.bat
pause 