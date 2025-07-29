import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

interface QuestionSet {
  id: number;
  title: string;
  created_at: string;
  questions: Question[];
}

interface Question {
  id: number;
  question_number: number;
  question_text: string;
  question_type: 'single' | 'multiple';
}

const QuestionSetList: React.FC = () => {
  const [questionSets, setQuestionSets] = useState<QuestionSet[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchQuestionSets();
  }, []);

  const fetchQuestionSets = async () => {
    try {
      const response = await axios.get<QuestionSet[]>('/api/question-sets/');
      setQuestionSets(response.data);
    } catch (error: any) {
      setError('获取题目集合失败: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-600">加载中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-error-50 border border-error-200 rounded-md p-4">
        <p className="text-error-700">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">题目集合</h1>
        <Link
          to="/"
          className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors"
        >
          上传新题目
        </Link>
      </div>

      {questionSets.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <p className="text-gray-600 mb-4">暂无题目集合</p>
          <Link
            to="/"
            className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors"
          >
            上传第一个题目集合
          </Link>
        </div>
      ) : (
        <div className="grid gap-6">
          {questionSets.map((questionSet) => (
            <div
              key={questionSet.id}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 mb-2">
                    {questionSet.title}
                  </h2>
                  <p className="text-sm text-gray-500">
                    创建时间: {new Date(questionSet.created_at).toLocaleString('zh-CN')}
                  </p>
                </div>
                <span className="bg-primary-100 text-primary-800 text-sm px-3 py-1 rounded-full">
                  {questionSet.questions.length} 道题
                </span>
              </div>

              <div className="flex justify-between items-center">
                <div className="text-sm text-gray-600">
                  <span className="mr-4">
                    单选题: {questionSet.questions.filter(q => q.question_type === 'single').length}
                  </span>
                  <span>
                    多选题: {questionSet.questions.filter(q => q.question_type === 'multiple').length}
                  </span>
                </div>
                <Link
                  to={`/question-sets/${questionSet.id}`}
                  className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors"
                >
                  开始答题
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default QuestionSetList; 