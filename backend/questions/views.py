from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import QuestionSet, Question, UserAnswer
from .serializers import (
    QuestionSetSerializer, QuestionSerializer, UserAnswerSerializer,
    FileUploadSerializer, SubmitAnswerSerializer
)
from .gemini_parser import GeminiPDFParser as PDFParser
import json


class FileUploadView(APIView):
    """文件上传和解析视图"""
    
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # 创建题目集合
                question_set = QuestionSet.objects.create(
                    title=serializer.validated_data['title'],
                    questions_file=serializer.validated_data['questions_file'],
                    answers_file=serializer.validated_data['answers_file']
                )
                
                # 解析PDF文件
                parser = PDFParser()
                
                # 解析题目文件
                questions_text = parser.extract_text_from_pdf(
                    serializer.validated_data['questions_file']
                )
                questions = parser.parse_questions(questions_text)
                
                # 解析答案文件
                answers_text = parser.extract_text_from_pdf(
                    serializer.validated_data['answers_file']
                )
                answers = parser.parse_answers(answers_text)
                
                # 合并题目和答案
                merged_questions = parser.merge_questions_and_answers(questions, answers)
                
                # 保存题目到数据库
                for question_data in merged_questions:
                    Question.objects.create(
                        question_set=question_set,
                        question_number=question_data['question_number'],
                        question_text=question_data['question_text'],
                        options=question_data['options'],
                        question_type=question_data['question_type'],
                        correct_answers=question_data['correct_answers'],
                        explanation=question_data['explanation']
                    )
                
                return Response({
                    'message': '文件上传成功',
                    'question_set_id': question_set.id,
                    'questions_count': len(merged_questions)
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                import traceback
                print(f"错误详情: {str(e)}")
                print(f"错误堆栈: {traceback.format_exc()}")
                return Response({
                    'error': f'文件解析失败: {str(e)}',
                    'details': traceback.format_exc()
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionSetListView(APIView):
    """题目集合列表视图"""
    
    def get(self, request):
        question_sets = QuestionSet.objects.all().order_by('-created_at')
        serializer = QuestionSetSerializer(question_sets, many=True)
        return Response(serializer.data)


class QuestionSetDetailView(APIView):
    """题目集合详情视图"""
    
    def get(self, request, pk):
        question_set = get_object_or_404(QuestionSet, pk=pk)
        serializer = QuestionSetSerializer(question_set)
        return Response(serializer.data)


class SubmitAnswerView(APIView):
    """提交答案视图"""
    
    def post(self, request):
        serializer = SubmitAnswerSerializer(data=request.data)
        if serializer.is_valid():
            question_id = serializer.validated_data['question_id']
            user_answers = serializer.validated_data['user_answers']
            
            try:
                question = Question.objects.get(id=question_id)
                
                # 判断答案是否正确
                correct_answers = set(question.correct_answers)
                user_answers_set = set(user_answers)
                is_correct = correct_answers == user_answers_set
                
                # 保存用户答案
                user_answer = UserAnswer.objects.create(
                    question=question,
                    user_answers=user_answers,
                    is_correct=is_correct
                )
                
                return Response({
                    'message': '答案提交成功',
                    'is_correct': is_correct,
                    'correct_answers': question.correct_answers,
                    'explanation': question.explanation
                }, status=status.HTTP_201_CREATED)
                
            except Question.DoesNotExist:
                return Response({
                    'error': '题目不存在'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_question_detail(request, question_id):
    """获取题目详情"""
    try:
        question = Question.objects.get(id=question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    except Question.DoesNotExist:
        return Response({
            'error': '题目不存在'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def submit_batch_answers(request):
    """批量提交答案"""
    try:
        answers_data = request.data.get('answers', [])
        results = []
        
        for answer_data in answers_data:
            question_id = answer_data.get('question_id')
            user_answers = answer_data.get('user_answers', [])
            
            try:
                question = Question.objects.get(id=question_id)
                
                # 判断答案是否正确
                correct_answers = set(question.correct_answers)
                user_answers_set = set(user_answers)
                is_correct = correct_answers == user_answers_set
                
                # 保存用户答案
                UserAnswer.objects.create(
                    question=question,
                    user_answers=user_answers,
                    is_correct=is_correct
                )
                
                results.append({
                    'question_id': question_id,
                    'is_correct': is_correct,
                    'correct_answers': question.correct_answers,
                    'explanation': question.explanation
                })
                
            except Question.DoesNotExist:
                results.append({
                    'question_id': question_id,
                    'error': '题目不存在'
                })
        
        return Response({
            'message': '批量提交完成',
            'results': results
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'批量提交失败: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST) 