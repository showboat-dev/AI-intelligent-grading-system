@echo off
echo 调试后端服务...
cd backend

REM 激活虚拟环境
call venv\Scripts\activate

REM 检查Django设置
echo 检查Django设置...
python manage.py check

REM 检查数据库迁移
echo 检查数据库迁移...
python manage.py showmigrations

REM 运行迁移
echo 运行数据库迁移...
python manage.py migrate

REM 创建超级用户（可选）
echo 是否创建超级用户？(y/n)
set /p create_super=
if /i "%create_super%"=="y" (
    python manage.py createsuperuser
)

REM 启动服务器（详细模式）
echo 启动Django服务器（详细模式）...
python manage.py runserver --verbosity=2

pause 