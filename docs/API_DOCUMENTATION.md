# PMP智能做题平台 API 文档

## 基础信息

- 基础URL: `http://localhost:8000/api/`
- 内容类型: `application/json`
- 文件上传: `multipart/form-data`

## 接口列表

### 1. 文件上传

**POST** `/api/upload/`

上传题目文件和答案解析文件，系统会自动解析并创建题目集合。

**请求参数:**
- `title` (string, required): 题目集合标题
- `questions_file` (file, required): 题目PDF文件
- `answers_file` (file, required): 答案解析PDF文件

**响应示例:**
```json
{
  "message": "文件上传成功",
  "question_set_id": 1,
  "questions_count": 50
}
```

### 2. 获取题目集合列表

**GET** `/api/question-sets/`

获取所有题目集合的列表。

**响应示例:**
```json
[
  {
    "id": 1,
    "title": "PMP项目管理模拟题",
    "created_at": "2024-01-15T10:30:00Z",
    "questions": [
      {
        "id": 1,
        "question_number": 1,
        "question_text": "项目管理的定义是什么？",
        "question_type": "single"
      }
    ]
  }
]
```

### 3. 获取题目集合详情

**GET** `/api/question-sets/{id}/`

获取指定题目集合的详细信息，包括所有题目。

**响应示例:**
```json
{
  "id": 1,
  "title": "PMP项目管理模拟题",
  "created_at": "2024-01-15T10:30:00Z",
  "questions": [
    {
      "id": 1,
      "question_number": 1,
      "question_text": "项目管理的定义是什么？",
      "options": {
        "A": "管理项目的过程",
        "B": "管理团队的过程",
        "C": "管理资源的过程",
        "D": "管理时间的过程"
      },
      "question_type": "single",
      "correct_answers": ["A"],
      "explanation": "项目管理是运用知识、技能、工具和技术来满足项目要求的过程。"
    }
  ]
}
```

### 4. 获取题目详情

**GET** `/api/questions/{id}/`

获取指定题目的详细信息。

**响应示例:**
```json
{
  "id": 1,
  "question_number": 1,
  "question_text": "项目管理的定义是什么？",
  "options": {
    "A": "管理项目的过程",
    "B": "管理团队的过程",
    "C": "管理资源的过程",
    "D": "管理时间的过程"
  },
  "question_type": "single",
  "correct_answers": ["A"],
  "explanation": "项目管理是运用知识、技能、工具和技术来满足项目要求的过程。"
}
```

### 5. 提交单个答案

**POST** `/api/submit-answer/`

提交单个题目的答案。

**请求参数:**
```json
{
  "question_id": 1,
  "user_answers": ["A"]
}
```

**响应示例:**
```json
{
  "message": "答案提交成功",
  "is_correct": true,
  "correct_answers": ["A"],
  "explanation": "项目管理是运用知识、技能、工具和技术来满足项目要求的过程。"
}
```

### 6. 批量提交答案

**POST** `/api/submit-batch-answers/`

批量提交多个题目的答案。

**请求参数:**
```json
{
  "answers": [
    {
      "question_id": 1,
      "user_answers": ["A"]
    },
    {
      "question_id": 2,
      "user_answers": ["B", "C"]
    }
  ]
}
```

**响应示例:**
```json
{
  "message": "批量提交完成",
  "results": [
    {
      "question_id": 1,
      "is_correct": true,
      "correct_answers": ["A"],
      "explanation": "项目管理是运用知识、技能、工具和技术来满足项目要求的过程。"
    },
    {
      "question_id": 2,
      "is_correct": false,
      "correct_answers": ["A", "D"],
      "explanation": "正确答案是A和D。"
    }
  ]
}
```

## 错误响应

当请求失败时，API会返回相应的HTTP状态码和错误信息：

```json
{
  "error": "错误描述信息"
}
```

常见状态码：
- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误

## PDF文件格式要求

### 题目文件格式
```
1. 项目管理的定义是什么？
A. 管理项目的过程
B. 管理团队的过程
C. 管理资源的过程
D. 管理时间的过程

2. 项目生命周期包括哪些阶段？
A. 启动阶段
B. 规划阶段
C. 执行阶段
D. 收尾阶段
```

### 答案解析文件格式
```
1. 答案：A
解析：项目管理是运用知识、技能、工具和技术来满足项目要求的过程。

2. 答案：ABCD
解析：项目生命周期包括启动、规划、执行、监控和收尾五个阶段。
``` 