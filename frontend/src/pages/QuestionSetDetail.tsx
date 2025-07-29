import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

interface Question {
  id: number;
  question_number: number;
  question_text: string;
  options: Record<string, string>;
  question_type: 'single' | 'multiple';
  correct_answers: string[];
  explanation: string;
}

interface QuestionSet {
  id: number;
  title: string;
  created_at: string;
  questions: Question[];
}

interface AnswerResult {
  question_id: number;
  is_correct: boolean;
  correct_answers: string[];
  explanation: string;
}

const QuestionSetDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [questionSet, setQuestionSet] = useState<QuestionSet | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState<Record<number, string[]>>({});
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState<Record<number, AnswerResult>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      fetchQuestionSet();
    }
  }, [id]);

  const fetchQuestionSet = async () => {
    try {
      const response = await axios.get<QuestionSet>(`/api/question-sets/${id}/`);
      setQuestionSet(response.data);
    } catch (error: any) {
      setError('获取题目集合失败: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId: number, option: string, checked: boolean) => {
    const currentAnswers = userAnswers[questionId] || [];
    let newAnswers: string[];

    if (checked) {
      newAnswers = [...currentAnswers, option];
    } else {
      newAnswers = currentAnswers.filter(answer => answer !== option);
    }

    setUserAnswers({
      ...userAnswers,
      [questionId]: newAnswers
    });
  };

  const handleSubmit = async () => {
    if (!questionSet) return;

    const answers = Object.entries(userAnswers).map(([questionId, answers]) => ({
      question_id: parseInt(questionId),
      user_answers: answers
    }));

    try {
      const response = await axios.post('/api/submit-batch-answers/', {
        answers
      });

      const resultsMap: Record<number, AnswerResult> = {};
      response.data.results.forEach((result: any) => {
        resultsMap[result.question_id] = result;
      });

      setResults(resultsMap);
      setSubmitted(true);
    } catch (error: any) {
      setError('提交答案失败: ' + (error.response?.data?.error || error.message));
    }
  };

  const getQuestionStatus = (questionIndex: number) => {
    if (!submitted) return 'pending';
    const question = questionSet?.questions[questionIndex];
    if (!question) return 'pending';
    
    const result = results[question.id];
    if (!result) return 'pending';
    
    return result.is_correct ? 'correct' : 'incorrect';
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

  if (!questionSet) {
    return (
      <div className="text-center">
        <p className="text-gray-600">题目集合不存在</p>
      </div>
    );
  }

  const currentQuestion = questionSet.questions[currentQuestionIndex];
  const totalQuestions = questionSet.questions.length;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{questionSet.title}</h1>
          <p className="text-gray-600">共 {totalQuestions} 道题目</p>
        </div>
        <Link
          to="/question-sets"
          className="text-primary-600 hover:text-primary-700"
        >
          返回列表
        </Link>
      </div>

      {/* 题目导航 */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="flex flex-wrap gap-2">
          {questionSet.questions.map((question, index) => (
            <button
              key={question.id}
              onClick={() => setCurrentQuestionIndex(index)}
              className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                index === currentQuestionIndex
                  ? 'bg-primary-600 text-white'
                  : getQuestionStatus(index) === 'correct'
                  ? 'bg-success-100 text-success-700'
                  : getQuestionStatus(index) === 'incorrect'
                  ? 'bg-error-100 text-error-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {question.question_number}
            </button>
          ))}
        </div>
      </div>

      {/* 当前题目 */}
      {currentQuestion && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">
              第 {currentQuestion.question_number} 题
            </h2>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              currentQuestion.question_type === 'single'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-warning-100 text-warning-800'
            }`}>
              {currentQuestion.question_type === 'single' ? '单选题' : '多选题'}
            </span>
          </div>

          <div className="mb-6">
            <p className="text-gray-900 leading-relaxed">{currentQuestion.question_text}</p>
          </div>

          <div className="space-y-3 mb-6">
            {Object.entries(currentQuestion.options).map(([key, value]) => (
              <label
                key={key}
                className={`flex items-start p-3 border rounded-md cursor-pointer transition-colors ${
                  userAnswers[currentQuestion.id]?.includes(key)
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                <input
                  type={currentQuestion.question_type === 'single' ? 'radio' : 'checkbox'}
                  name={`question-${currentQuestion.id}`}
                  value={key}
                  checked={userAnswers[currentQuestion.id]?.includes(key) || false}
                  onChange={(e) => handleAnswerChange(
                    currentQuestion.id,
                    key,
                    e.target.checked
                  )}
                  className="mt-1 mr-3"
                />
                <span className="font-medium text-gray-700 mr-2">{key}.</span>
                <span className="text-gray-900">{value}</span>
              </label>
            ))}
          </div>

          {/* 提交按钮 */}
          {!submitted && (
            <div className="flex justify-between">
              <button
                onClick={() => setCurrentQuestionIndex(Math.max(0, currentQuestionIndex - 1))}
                disabled={currentQuestionIndex === 0}
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                上一题
              </button>
              
              {currentQuestionIndex === totalQuestions - 1 ? (
                <button
                  onClick={handleSubmit}
                  className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition-colors"
                >
                  提交答案
                </button>
              ) : (
                <button
                  onClick={() => setCurrentQuestionIndex(Math.min(totalQuestions - 1, currentQuestionIndex + 1))}
                  className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition-colors"
                >
                  下一题
                </button>
              )}
            </div>
          )}

          {/* 答案解析 */}
          {submitted && results[currentQuestion.id] && (
            <div className={`mt-6 p-4 rounded-md ${
              results[currentQuestion.id].is_correct
                ? 'bg-success-50 border border-success-200'
                : 'bg-error-50 border border-error-200'
            }`}>
              <div className="flex items-center mb-3">
                <span className={`text-lg font-medium ${
                  results[currentQuestion.id].is_correct ? 'text-success-700' : 'text-error-700'
                }`}>
                  {results[currentQuestion.id].is_correct ? '✓ 正确' : '✗ 错误'}
                </span>
              </div>
              
              <div className="mb-3">
                <p className="text-sm text-gray-600 mb-1">正确答案:</p>
                <p className="font-medium text-gray-900">
                  {results[currentQuestion.id].correct_answers.join(', ')}
                </p>
              </div>
              
              {results[currentQuestion.id].explanation && (
                <div>
                  <p className="text-sm text-gray-600 mb-1">解析:</p>
                  <p className="text-gray-900 whitespace-pre-line">
                    {results[currentQuestion.id].explanation}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* 统计信息 */}
      {submitted && (
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h3 className="text-lg font-semibold mb-4">答题统计</h3>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-primary-600">
                {Object.values(results).filter(r => r.is_correct).length}
              </p>
              <p className="text-sm text-gray-600">正确</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-error-600">
                {Object.values(results).filter(r => !r.is_correct).length}
              </p>
              <p className="text-sm text-gray-600">错误</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-600">
                {Math.round((Object.values(results).filter(r => r.is_correct).length / totalQuestions) * 100)}%
              </p>
              <p className="text-sm text-gray-600">正确率</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuestionSetDetail; 