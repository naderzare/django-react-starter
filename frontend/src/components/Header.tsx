import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { User } from '../types/auth';
import { authService } from '../services/authService';

const Header: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }

    // Listen for storage events to update user state
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'user') {
        setUser(e.newValue ? JSON.parse(e.newValue) : null);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const handleLogout = async () => {
    try {
      await authService.logout();
      setUser(null);
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          MyApp
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                Main
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/users">
                Sample List
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/payments">
                Payment & Credits
              </Link>
            </li>
          </ul>

          {user ? (
            <div className="d-flex align-items-center text-light">
              <span className="me-3">
                {user.username} ({user.email})
                {user.account_value !== undefined && (
                  <span className="ms-2 badge bg-success">
                    Credits: ${typeof user.account_value === 'number' 
                      ? user.account_value.toFixed(2) 
                      : parseFloat(String(user.account_value)).toFixed(2)}
                  </span>
                )}
              </span>
              <button 
                className="btn btn-outline-light btn-sm"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          ) : (
            <Link to="/" className="btn btn-outline-light">
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Header;
