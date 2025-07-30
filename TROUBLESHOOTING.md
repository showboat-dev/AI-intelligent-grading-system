# 故障排除指南

## 常见问题及解决方案

### 1. 依赖安装失败

**错误信息：**
```
Getting requirements to build wheel did not run successfully
KeyError: '__version__'
```

**解决方案：**
1. 运行 `clean_backend.bat` 清理环境
2. 重新运行 `start_backend.bat`
3. 如果仍然失败，尝试手动安装：
   ```bash
   cd backend
   python -m venv venv
   call venv\Scripts\activate
   pip install --upgrade pip
   pip install Django==4.2.7
   pip install djangorestframework==3.14.0
   pip install django-cors-headers==4.3.1
   pip install PyPDF2==3.0.1
   pip install pdfplumber==0.9.0
   pip install python-dotenv==1.0.0
   pip install Pillow==10.1.0
   ```

### 2. Django模块未找到

**错误信息：**
```
ModuleNotFoundError: No module named 'django'
```

**解决方案：**
1. 确保虚拟环境已激活
2. 检查Python版本（建议使用Python 3.8+）
3. 重新安装Django：
   ```bash
   pip install Django==4.2.7
   ```

### 3. 数据库迁移失败

**解决方案：**
1. 删除 `backend/db.sqlite3` 文件
2. 重新运行迁移：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### 4. 端口被占用

**解决方案：**
1. 查找占用端口的进程：
   ```bash
   netstat -ano | findstr :8000
   ```
2. 终止进程或使用不同端口：
   ```bash
   python manage.py runserver 8001
   ```

### 5. 权限问题

**解决方案：**
1. 以管理员身份运行命令提示符
2. 检查文件夹权限
3. 确保有足够的磁盘空间

## 系统要求

- Python 3.8 或更高版本
- Windows 10/11
- 至少 2GB 可用内存
- 至少 1GB 可用磁盘空间

## 验证安装

运行以下命令验证安装：
```bash
cd backend
call venv\Scripts\activate
python -c "import django; print(django.get_version())"
```

如果显示Django版本号，说明安装成功。 