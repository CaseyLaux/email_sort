import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import EmailViewer from './EmailViewer';
import LoginPage from './LoginPage';
import SignupPage from './SignupPage';
import Profile from './profile';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/profile" element={<ProtectedRoute component={Profile} />} />
        <Route path="/" element={<ProtectedRoute component={EmailViewer} />} />
      </Routes>
    </Router>
  );
}

export default App;
