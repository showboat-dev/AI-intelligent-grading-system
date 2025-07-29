from django.urls import path
from . import views

urlpatterns = [
    # 文件上传
    path('upload/', views.FileUploadView.as_view(), name='file_upload'),
    
    # 题目集合
    path('question-sets/', views.QuestionSetListView.as_view(), name='question_set_list'),
    path('question-sets/<int:pk>/', views.QuestionSetDetailView.as_view(), name='question_set_detail'),
    
    # 题目详情
    path('questions/<int:question_id>/', views.get_question_detail, name='question_detail'),
    
    # 答案提交
    path('submit-answer/', views.SubmitAnswerView.as_view(), name='submit_answer'),
    path('submit-batch-answers/', views.submit_batch_answers, name='submit_batch_answers'),
] 