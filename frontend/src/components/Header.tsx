import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold text-primary-600">
            PMP智能做题平台
          </Link>
          <nav className="flex space-x-6">
            <Link 
              to="/" 
              className="text-gray-600 hover:text-primary-600 transition-colors"
            >
              首页
            </Link>
            <Link 
              to="/question-sets" 
              className="text-gray-600 hover:text-primary-600 transition-colors"
            >
              题目集合
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 