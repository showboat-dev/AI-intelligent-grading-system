import re
import PyPDF2
import pdfplumber
from typing import List, Dict, Tuple


class PDFParser:
    """PDF解析工具类"""
    
    def __init__(self):
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
    
    def parse_questions(self, text: str) -> List[Dict]:
        """解析题目文本"""
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
                    'question_type': 'single',  # 默认为单选
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
                # 如果答案超过1个，则为多选题
                if len(answers) > 1:
                    current_question['question_type'] = 'multiple'
                continue
            
            # 检查是否是解析
            explanation_match = self.explanation_pattern.search(line)
            if explanation_match and current_question:
                current_question['explanation'] = explanation_match.group(1)
                continue
            
            # 如果当前行不是特殊格式，可能是题干或解析的延续
            if current_question:
                if not current_question['options']:
                    # 如果还没有选项，可能是题干的延续
                    current_question['question_text'] += ' ' + line
                elif current_question['explanation']:
                    # 如果已有解析，可能是解析的延续
                    current_question['explanation'] += ' ' + line
        
        # 添加最后一个题目
        if current_question:
            questions.append(current_question)
        
        return questions
    
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
            
            # 如果当前行不是特殊格式，可能是解析的延续
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