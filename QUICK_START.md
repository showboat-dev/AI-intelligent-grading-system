# PMP智能做题平台 - 快速启动指南

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Node.js**: 16+
- **操作系统**: Windows 10/11, macOS, Linux

### 一键启动（Windows）

1. **启动后端服务**
   ```bash
   # 双击运行
   start_backend.bat
   ```
   或手动执行：
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

2. **启动前端服务**
   ```bash
   # 双击运行
   start_frontend.bat
   ```
   或手动执行：
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **访问系统**
   - 前端地址：http://localhost:3000
   - 后端API：http://localhost:8000

## 📋 使用流程

### 1. 准备PDF文件

准备两个PDF文件：
- **题目文件**：包含题目的PDF
- **答案解析文件**：包含答案和解析的PDF

**文件格式要求：**
- 必须是文本型PDF（可复制文本）
- 题目格式：`1. 题目内容` + `A. 选项A` + `B. 选项B` ...
- 答案格式：`1. 答案：A` + `解析：解析内容`

### 2. 上传文件

1. 访问 http://localhost:3000
2. 填写题目集合标题
3. 上传题目PDF文件
4. 上传答案解析PDF文件
5. 点击"上传文件"

### 3. 开始答题

1. 系统自动跳转到答题页面
2. 使用题目导航选择题目
3. 根据题目类型选择答案（单选/多选）
4. 完成所有题目后点击"提交答案"

### 4. 查看结果

- 系统自动判卷并显示结果
- 查看每道题的正确答案和解析
- 查看答题统计信息

## 🔧 开发模式

### 后端开发

```bash
cd backend
# 激活虚拟环境
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

### 前端开发

```bash
cd frontend
# 安装依赖
npm install

# 启动开发服务器
npm start

# 构建生产版本
npm run build
```

## 📁 项目结构

```
AI-Judge System/
├── backend/                 # Django后端
│   ├── pmp_platform/       # Django项目配置
│   ├── questions/          # 题目应用
│   ├── manage.py           # Django管理脚本
│   └── requirements.txt    # Python依赖
├── frontend/               # React前端
│   ├── src/               # 源代码
│   ├── public/            # 静态文件
│   └── package.json       # Node.js依赖
├── docs/                  # 文档
├── start_backend.bat      # 后端启动脚本
├── start_frontend.bat     # 前端启动脚本
└── README.md             # 项目说明
```

## 🐛 故障排除

### 常见问题

**1. 后端启动失败**
```bash
# 检查Python版本
python --version

# 重新安装依赖
pip install -r requirements.txt

# 检查端口占用
netstat -ano | findstr :8000
```

**2. 前端启动失败**
```bash
# 清除缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules
npm install

# 检查端口占用
netstat -ano | findstr :3000
```

**3. PDF解析失败**
- 确保PDF是文本型（非扫描版）
- 检查PDF格式是否符合要求
- 查看后端日志获取详细错误信息

**4. 数据库问题**
```bash
# 重置数据库
python manage.py flush

# 重新迁移
python manage.py makemigrations
python manage.py migrate
```

## 📞 技术支持

如果遇到问题：

1. 查看控制台错误信息
2. 检查网络连接
3. 确认文件格式正确
4. 查看项目文档

## 🎯 下一步

- 查看 [API文档](docs/API_DOCUMENTATION.md)
- 阅读 [用户指南](docs/USER_GUIDE.md)
- 了解 [PDF格式要求](docs/SAMPLE_PDF_FORMAT.md)

---

**祝您使用愉快！** 🎉 