from rest_framework import serializers
from .models import QuestionSet, Question, UserAnswer


class QuestionSerializer(serializers.ModelSerializer):
    """题目序列化器"""
    class Meta:
        model = Question
        fields = [
            'id', 'question_number', 'question_text', 'options', 
            'question_type', 'correct_answers', 'explanation'
        ]


class QuestionSetSerializer(serializers.ModelSerializer):
    """题目集合序列化器"""
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuestionSet
        fields = ['id', 'title', 'created_at', 'questions']


class UserAnswerSerializer(serializers.ModelSerializer):
    """用户答案序列化器"""
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'user_answers', 'is_correct', 'submitted_at']


class FileUploadSerializer(serializers.Serializer):
    """文件上传序列化器"""
    title = serializers.CharField(max_length=200)
    questions_file = serializers.FileField()
    answers_file = serializers.FileField()


class SubmitAnswerSerializer(serializers.Serializer):
    """提交答案序列化器"""
    question_id = serializers.IntegerField()
    user_answers = serializers.ListField(child=serializers.CharField()) 