@echo off
echo 启动PMP智能做题平台后端服务...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
pause 