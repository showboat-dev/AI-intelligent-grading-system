# PMP 智能做题平台

一个基于Web的智能做题和判卷系统，支持PDF题目文件上传、在线答题和自动判卷。

## 功能特性

- 📂 PDF文件上传（题目文件和答案解析文件）
- 📄 智能题目解析（题干、选项、题型识别）
- 🖥️ 在线答题界面（单选/多选支持）
- 🧠 自动判卷和答案解析
- 💻 响应式设计，支持移动端

## 项目结构

```
AI-Judge System/
├── frontend/          # React前端应用
├── backend/           # Django后端API
├── docs/             # 项目文档
└── README.md         # 项目说明
```

## 技术栈

- **前端**: React + TypeScript + Tailwind CSS
- **后端**: Django + Django REST Framework
- **PDF处理**: PyPDF2 / pdfplumber
- **数据格式**: JSON

## 快速开始

### 后端设置
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 前端设置
```bash
cd frontend
npm install
npm start
```

## 开发计划

- [x] 项目结构搭建
- [ ] 后端API开发
- [ ] 前端界面开发
- [ ] PDF解析功能
- [ ] 答题判卷逻辑
- [ ] 界面优化和测试 