from django.db import models
import json


class QuestionSet(models.Model):
    """题目集合模型"""
    title = models.CharField(max_length=200, verbose_name="题目集合标题")
    questions_file = models.FileField(upload_to='questions/', verbose_name="题目文件")
    answers_file = models.FileField(upload_to='answers/', verbose_name="答案解析文件")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "题目集合"
        verbose_name_plural = "题目集合"
    
    def __str__(self):
        return self.title


class Question(models.Model):
    """题目模型"""
    QUESTION_TYPES = [
        ('single', '单选题'),
        ('multiple', '多选题'),
    ]
    
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name='questions')
    question_number = models.IntegerField(verbose_name="题号")
    question_text = models.TextField(verbose_name="题干")
    options = models.JSONField(verbose_name="选项")
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, verbose_name="题目类型")
    correct_answers = models.JSONField(verbose_name="正确答案")
    explanation = models.TextField(verbose_name="答案解析", blank=True)
    
    class Meta:
        verbose_name = "题目"
        verbose_name_plural = "题目"
        ordering = ['question_number']
    
    def __str__(self):
        return f"第{self.question_number}题"


class UserAnswer(models.Model):
    """用户答案模型"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    user_answers = models.JSONField(verbose_name="用户答案")
    is_correct = models.BooleanField(verbose_name="是否正确")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")
    
    class Meta:
        verbose_name = "用户答案"
        verbose_name_plural = "用户答案"
    
    def __str__(self):
        return f"用户答案 - 第{self.question.question_number}题" 