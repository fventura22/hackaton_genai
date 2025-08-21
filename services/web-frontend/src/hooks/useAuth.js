import React, { createContext, useContext, useState, useEffect } from 'react';
import CognitoService from '../services/CognitoService';
import ApiService from '../services/ApiService';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (CognitoService.isAuthenticated()) {
      const userInfo = CognitoService.getCurrentUser();
      const token = CognitoService.getAccessToken();
      ApiService.setAuthToken(token);
      setIsAuthenticated(true);
      setUser(userInfo);
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const result = await CognitoService.login(username, password);
      if (result.success) {
        ApiService.setAuthToken(result.tokens.accessToken);
        setIsAuthenticated(true);
        setUser(result.user);
        return { success: true };
      }
      return result;
    } catch (error) {
      return { success: false, error: 'Login failed' };
    }
  };

  const logout = () => {
    CognitoService.logout();
    setIsAuthenticated(false);
    setUser(null);
    ApiService.setAuthToken(null);
  };

  const isAdmin = () => CognitoService.isAdmin();
  const isAnalyst = () => CognitoService.isAnalyst();

  const value = {
    isAuthenticated,
    user,
    login,
    logout,
    loading,
    isAdmin,
    isAnalyst
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}