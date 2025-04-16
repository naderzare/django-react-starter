import React, { useState } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import toast from 'react-hot-toast';
import { authService } from '../services/authService';
import { LoginCredentials, RegisterCredentials, User } from '../types/auth';

const MainPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState('');
  const [user, setUser] = useState<User | null>(() => {
    const savedUser = localStorage.getItem('user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const credentials: LoginCredentials = {
      username: formData.get('username') as string,
      password: formData.get('password') as string,
    };

    try {
      const response = await authService.login(credentials);
      localStorage.setItem('token', response.access);
      localStorage.setItem('user', JSON.stringify(response.user));
      setUser(response.user);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed');
    }
  };

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const credentials: RegisterCredentials = {
      username: formData.get('username') as string,
      email: formData.get('email') as string,
      password1: formData.get('password1') as string,
      password2: formData.get('password2') as string,
    };

    try {
      const response = await authService.register(credentials);
      localStorage.setItem('token', response.access);
      localStorage.setItem('user', JSON.stringify(response.user));
      setUser(response.user);
      setError('');
    } catch (err: any) {
      console.error('Registration error:', err);
      
      // Handle different error formats
      if (err.response?.data) {
        const errorData = err.response.data;
        // If error is an object with field-specific errors
        if (typeof errorData === 'object' && !Array.isArray(errorData)) {
          const errorMessages = Object.entries(errorData)
            .map(([field, errors]) => {
              if (Array.isArray(errors)) {
                return `${field}: ${errors.join(', ')}`;
              } else {
                return `${field}: ${errors}`;
              }
            })
            .join('\n');
          setError(errorMessages);
        } else if (typeof errorData === 'string') {
          setError(errorData);
        } else {
          setError('Registration failed. Please check your information and try again.');
        }
      } else {
        setError('Registration failed. Please try again later.');
      }
    }
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      setUser(null);
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  const handleGoogleLogin = useGoogleLogin({
    flow: 'implicit',
    onSuccess: async (response) => {
      try {
        const result = await authService.googleLogin(response.access_token);
        localStorage.setItem('token', result.access);
        localStorage.setItem('user', JSON.stringify(result.user));
        setUser(result.user);
        setError('');
        toast.success('Successfully logged in with Google!');
      } catch (err: any) {
        console.error('Google login error:', err);
        setError(err.response?.data?.error || 'Google login failed');
        toast.error(err.response?.data?.error || 'Google login failed');
      }
    },
    onError: (error) => {
      console.error('Google OAuth error:', error);
      setError('Google login failed');
      toast.error('Google login failed');
    }
  });

  if (user) {
    return (
      <div className="container mt-5">
        <div className="card p-4">
          <h2>Welcome, {user.username}!</h2>
          <p>Email: {user.email}</p>
          <button className="btn btn-danger" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <div className="mb-3">
                <button
                  className={`btn ${isLogin ? 'btn-primary' : 'btn-outline-primary'} me-2`}
                  onClick={() => setIsLogin(true)}
                >
                  Login
                </button>
                <button
                  className={`btn ${!isLogin ? 'btn-primary' : 'btn-outline-primary'}`}
                  onClick={() => setIsLogin(false)}
                >
                  Register
                </button>
              </div>

              {error && (
                <div className="alert alert-danger">
                  {error.split('\n').map((line, index) => (
                    <React.Fragment key={index}>
                      {line}
                      {index < error.split('\n').length - 1 && <br />}
                    </React.Fragment>
                  ))}
                </div>
              )}

              {/* Google Login Button */}
              <div className="mb-4 d-grid">
                <button
                  className="btn btn-danger"
                  onClick={() => handleGoogleLogin()}
                >
                  Sign in with Google
                </button>
              </div>

              <div className="text-center mb-4">
                <div className="divider d-flex align-items-center">
                  <span className="mx-3">Or</span>
                </div>
              </div>

              {isLogin ? (
                <form onSubmit={handleLogin}>
                  <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                      type="text"
                      className="form-control"
                      id="username"
                      name="username"
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                      type="password"
                      className="form-control"
                      id="password"
                      name="password"
                      required
                    />
                  </div>
                  <button type="submit" className="btn btn-primary">Login</button>
                </form>
              ) : (
                <form onSubmit={handleRegister}>
                  <div className="mb-3">
                    <label htmlFor="reg-username" className="form-label">Username</label>
                    <input
                      type="text"
                      className="form-control"
                      id="reg-username"
                      name="username"
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      name="email"
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="password1" className="form-label">Password</label>
                    <input
                      type="password"
                      className="form-control"
                      id="password1"
                      name="password1"
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="password2" className="form-label">Confirm Password</label>
                    <input
                      type="password"
                      className="form-control"
                      id="password2"
                      name="password2"
                      required
                    />
                  </div>
                  <button type="submit" className="btn btn-primary">Register</button>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
