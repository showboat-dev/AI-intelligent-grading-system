import re
import json
import os
import requests
import PyPDF2
import pdfplumber
from typing import List, Dict, Tuple
from django.conf import settings


class GeminiPDFParser:
    """使用HTTP请求直接调用Gemini API的PDF解析工具类"""
    
    def __init__(self):
        # 从环境变量获取API密钥
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("请设置GEMINI_API_KEY环境变量")
        
        # Gemini API配置
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        self.headers = {
            "Content-Type": "application/json",
        }
        
        # 备用正则表达式解析器
        self.question_pattern = re.compile(r'(\d+)[\.、]\s*(.+)')
        self.option_pattern = re.compile(r'([A-D])[\.、]\s*(.+)')
        self.answer_pattern = re.compile(r'答案[：:]\s*([A-D]+)')
        self.explanation_pattern = re.compile(r'解析[：:]\s*(.+)')
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """从PDF文件中提取文本"""
        try:
            # 尝试使用pdfplumber（更好的文本提取）
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            # 备用方案：使用PyPDF2
            try:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
            except Exception as e2:
                raise Exception(f"无法解析PDF文件: {str(e2)}")
    
    def call_gemini_api(self, prompt: str) -> str:
        """直接调用Gemini API"""
        try:
            # 构建请求数据
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "topP": 0.8,
                    "topK": 40,
                    "maxOutputTokens": 2048,
                }
            }
            
            # 发送请求
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            # 检查响应
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']
                    if 'parts' in content and len(content['parts']) > 0:
                        return content['parts'][0]['text']
                    else:
                        raise Exception("API响应格式异常：缺少parts")
                else:
                    raise Exception("API响应格式异常：缺少candidates")
            else:
                error_msg = f"API请求失败: {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            raise Exception("API请求超时")
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求错误: {str(e)}")
        except Exception as e:
            raise Exception(f"API调用失败: {str(e)}")
    
    def parse_with_gemini(self, text: str) -> List[Dict]:
        """使用Gemini API解析题目文本"""
        try:
            # 限制文本长度 - 减少到更安全的长度
            if len(text) > 15000:  # 减少到15000字符
                text = text[:15000]
                print("警告：文本过长，已截断到15000字符")
            
            # 构建更明确的提示
            prompt = f"""
请解析以下题目文本，返回JSON格式的题目列表。

要求：
1. 识别每个题目的题号、题干、选项、正确答案和解析
2. 判断题目类型（单选/多选）
3. 只返回JSON格式，不要任何其他文字

题目文本：
{text}

请严格按照以下JSON格式返回：
[
  {{
    "question_number": 1,
    "question_text": "题目内容",
    "options": {{"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"}},
    "question_type": "single",
    "correct_answers": ["A"],
    "explanation": "解析内容"
  }}
]
"""
            
            print(f"正在调用Gemini API，文本长度: {len(text)}")
            
            # 调用API
            ai_response = self.call_gemini_api(prompt)
            
            print(f"Gemini API完整响应: {ai_response}")
            
            # 改进的JSON提取逻辑
            json_data = self.extract_json_from_response(ai_response)
            
            if json_data:
                print(f"成功解析 {len(json_data)} 道题目")
                return json_data
            else:
                print("未找到有效的JSON格式，使用备用解析")
                return self.parse_with_regex(text)
                
        except Exception as e:
            print(f"Gemini解析失败: {str(e)}")
            return self.parse_with_regex(text)

    def extract_json_from_response(self, response_text: str) -> List[Dict]:
        """从API响应中提取JSON数据"""
        try:
            # 方法1：直接尝试解析整个响应
            try:
                data = json.loads(response_text.strip())
                if isinstance(data, list):
                    return data
            except:
                pass
            
            # 方法2：查找JSON数组
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    if isinstance(data, list):
                        return data
                except:
                    pass
            
            # 方法3：查找JSON对象数组的其他模式
            patterns = [
                r'\[\s*\{.*\}\s*\]',  # 标准数组
                r'\{.*\}.*\{.*\}',    # 多个对象
                r'question_number.*question_text',  # 包含关键字段
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response_text, re.DOTALL)
                for match in matches:
                    try:
                        # 尝试修复常见的JSON格式问题
                        fixed_json = self.fix_json_format(match)
                        data = json.loads(fixed_json)
                        if isinstance(data, list):
                            return data
                    except:
                        continue
            
            # 方法4：手动构建JSON（如果响应包含结构化信息）
            return self.build_json_from_text(response_text)
            
        except Exception as e:
            print(f"JSON提取失败: {e}")
            return None

    def fix_json_format(self, text: str) -> str:
        """修复常见的JSON格式问题"""
        # 移除可能的markdown标记
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        
        # 修复单引号
        text = text.replace("'", '"')
        
        # 修复没有引号的键
        text = re.sub(r'(\w+):', r'"\1":', text)
        
        return text

    def build_json_from_text(self, text: str) -> List[Dict]:
        """从文本中手动构建JSON（备用方案）"""
        questions = []
        
        # 查找题目编号
        question_matches = re.findall(r'(\d+)[\.、]\s*(.+)', text)
        
        for i, (number, content) in enumerate(question_matches):
            question = {
                'question_number': int(number),
                'question_text': content.strip(),
                'options': {},
                'question_type': 'single',
                'correct_answers': [],
                'explanation': ''
            }
            
            # 查找选项
            options_text = text[text.find(content):text.find(content) + 500]  # 在题目附近查找
            option_matches = re.findall(r'([A-D])[\.、]\s*(.+)', options_text)
            for opt_key, opt_text in option_matches:
                question['options'][opt_key] = opt_text.strip()
            
            # 查找答案
            answer_match = re.search(rf'{number}[^A-D]*答案[：:]\s*([A-D]+)', text)
            if answer_match:
                question['correct_answers'] = list(answer_match.group(1))
                if len(question['correct_answers']) > 1:
                    question['question_type'] = 'multiple'
            
            questions.append(question)
        
        return questions
    
    def parse_with_regex(self, text: str) -> List[Dict]:
        """使用正则表达式解析题目文本（备用方案）"""
        questions = []
        lines = text.split('\n')
        current_question = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是题目开始
            question_match = self.question_pattern.match(line)
            if question_match:
                # 保存前一个题目
                if current_question:
                    questions.append(current_question)
                
                # 开始新题目
                question_number = int(question_match.group(1))
                question_text = question_match.group(2)
                
                current_question = {
                    'question_number': question_number,
                    'question_text': question_text,
                    'options': {},
                    'question_type': 'single',
                    'correct_answers': [],
                    'explanation': ''
                }
                continue
            
            # 检查是否是选项
            option_match = self.option_pattern.match(line)
            if option_match and current_question:
                option_key = option_match.group(1)
                option_text = option_match.group(2)
                current_question['options'][option_key] = option_text
                continue
            
            # 检查是否是答案
            answer_match = self.answer_pattern.search(line)
            if answer_match and current_question:
                answers = answer_match.group(1)
                current_question['correct_answers'] = list(answers)
                if len(answers) > 1:
                    current_question['question_type'] = 'multiple'
                continue
            
            # 检查是否是解析
            explanation_match = self.explanation_pattern.search(line)
            if explanation_match and current_question:
                current_question['explanation'] = explanation_match.group(1)
                continue
            
            # 处理延续内容
            if current_question:
                if not current_question['options']:
                    current_question['question_text'] += ' ' + line
                elif current_question['explanation']:
                    current_question['explanation'] += ' ' + line
        
        # 添加最后一个题目
        if current_question:
            questions.append(current_question)
        
        return questions
    
    def parse_questions(self, text: str) -> List[Dict]:
        """解析题目文本（优先使用Gemini）"""
        return self.parse_with_gemini(text)
    
    def parse_answers(self, text: str) -> Dict[int, Dict]:
        """解析答案解析文本"""
        answers = {}
        lines = text.split('\n')
        current_answer = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是答案开始
            answer_match = self.answer_pattern.search(line)
            if answer_match:
                # 尝试从行中找到题号
                number_match = re.search(r'(\d+)[\.、]', line)
                if number_match:
                    question_number = int(number_match.group(1))
                    answers_text = answer_match.group(1)
                    
                    current_answer = {
                        'question_number': question_number,
                        'correct_answers': list(answers_text),
                        'explanation': ''
                    }
                    continue
            
            # 检查是否是解析
            explanation_match = self.explanation_pattern.search(line)
            if explanation_match and current_answer:
                current_answer['explanation'] = explanation_match.group(1)
                answers[current_answer['question_number']] = current_answer
                current_answer = None
                continue
            
            # 处理延续内容
            if current_answer and current_answer['explanation']:
                current_answer['explanation'] += ' ' + line
        
        return answers
    
    def merge_questions_and_answers(self, questions: List[Dict], answers: Dict[int, Dict]) -> List[Dict]:
        """合并题目和答案信息"""
        for question in questions:
            question_number = question['question_number']
            if question_number in answers:
                answer_info = answers[question_number]
                question['correct_answers'] = answer_info['correct_answers']
                question['explanation'] = answer_info['explanation']
                
                # 根据答案数量判断题目类型
                if len(answer_info['correct_answers']) > 1:
                    question['question_type'] = 'multiple'
                else:
                    question['question_type'] = 'single'
        
        return questions

    def test_api_response(self, text: str = "1. 测试题目\nA. 选项A\nB. 选项B\n答案：A"):
        """测试API响应格式"""
        try:
            prompt = f"解析以下题目：\n{text}\n返回JSON格式。"
            response = self.call_gemini_api(prompt)
            print(f"测试响应: {response}")
            return response
        except Exception as e:
            print(f"测试失败: {e}")
            return None