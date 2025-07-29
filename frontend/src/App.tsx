import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import QuestionSetList from './pages/QuestionSetList';
import QuestionSetDetail from './pages/QuestionSetDetail';
import './App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/question-sets" element={<QuestionSetList />} />
            <Route path="/question-sets/:id" element={<QuestionSetDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 