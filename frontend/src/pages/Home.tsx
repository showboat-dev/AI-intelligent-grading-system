import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface UploadResponse {
  message: string;
  question_set_id: number;
  questions_count: number;
}

const Home: React.FC = () => {
  const [title, setTitle] = useState('');
  const [questionsFile, setQuestionsFile] = useState<File | null>(null);
  const [answersFile, setAnswersFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');
  const navigate = useNavigate();

  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title || !questionsFile || !answersFile) {
      setUploadMessage('请填写所有必填项');
      return;
    }

    setIsUploading(true);
    setUploadMessage('');

    const formData = new FormData();
    formData.append('title', title);
    formData.append('questions_file', questionsFile);
    formData.append('answers_file', answersFile);

    try {
      const response = await axios.post<UploadResponse>('/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadMessage(`上传成功！解析了 ${response.data.questions_count} 道题目`);
      
      // 跳转到题目集合详情页
      setTimeout(() => {
        navigate(`/question-sets/${response.data.question_set_id}`);
      }, 2000);

    } catch (error: any) {
      setUploadMessage(`上传失败: ${error.response?.data?.error || error.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          PMP智能做题平台
        </h1>
        <p className="text-xl text-gray-600">
          上传PDF文件，开始智能做题和自动判卷
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-6">上传题目文件</h2>
        
        <form onSubmit={handleFileUpload} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              题目集合标题 *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="请输入题目集合标题"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              题目文件 (PDF) *
            </label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setQuestionsFile(e.target.files?.[0] || null)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
            <p className="text-sm text-gray-500 mt-1">
              请上传包含题目的PDF文件（文本型）
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              答案解析文件 (PDF) *
            </label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setAnswersFile(e.target.files?.[0] || null)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
            <p className="text-sm text-gray-500 mt-1">
              请上传包含答案和解析的PDF文件（文本型）
            </p>
          </div>

          <button
            type="submit"
            disabled={isUploading}
            className="w-full bg-primary-600 text-white py-3 px-4 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isUploading ? '上传中...' : '上传文件'}
          </button>
        </form>

        {uploadMessage && (
          <div className={`mt-4 p-4 rounded-md ${
            uploadMessage.includes('成功') 
              ? 'bg-success-50 text-success-700 border border-success-200' 
              : 'bg-error-50 text-error-700 border border-error-200'
          }`}>
            {uploadMessage}
          </div>
        )}
      </div>

      <div className="mt-8 bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold mb-4">功能说明</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">📂 文件上传</h3>
            <p className="text-gray-600">
              支持上传两个PDF文件：题目文件和答案解析文件。系统会自动解析文本内容。
            </p>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">📄 智能解析</h3>
            <p className="text-gray-600">
              自动识别题目结构、选项、题型（单选/多选）和正确答案。
            </p>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">🖥️ 在线答题</h3>
            <p className="text-gray-600">
              提供友好的答题界面，支持单选和多选题的交互操作。
            </p>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">🧠 自动判卷</h3>
            <p className="text-gray-600">
              提交后自动判卷，显示正确答案和详细解析。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 