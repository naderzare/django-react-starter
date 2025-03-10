import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { Toaster } from 'react-hot-toast';
import Header from './components/Header';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import MainPage from './pages/MainPage';
import TaskList from './pages/SampleList';

const App: React.FC = () => {
  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID || ''} onScriptLoadError={() => console.error('Google OAuth script failed to load')}>
      <Router>
        <Header /> {/* Display the navigation bar at the top */}
        <div className="container mt-4">
          <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="/users" element={<TaskList />} />
          </Routes>
        </div>
        <Toaster position="top-right" />
      </Router>
    </GoogleOAuthProvider>
  );
};

export default App;
