'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface AuthContextType {
  token: string | null;
  role: string | null;
  userId: string | null;
  login: (token: string, role: string, userId: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [role, setRole] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Check local storage for existing session on mount
    const storedToken = localStorage.getItem('token');
    const storedRole = localStorage.getItem('role');
    const storedUserId = localStorage.getItem('userId');

    if (storedToken && storedRole && storedUserId) {
      setToken(storedToken);
      setRole(storedRole);
      setUserId(storedUserId);
    }
  }, []);

  const login = (newToken: string, newRole: string, newUserId: string) => {
    localStorage.setItem('token', newToken);
    localStorage.setItem('role', newRole);
    localStorage.setItem('userId', newUserId);
    
    setToken(newToken);
    setRole(newRole);
    setUserId(newUserId);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('userId');
    
    setToken(null);
    setRole(null);
    setUserId(null);

    router.push('/Login');
  };

  return (
    <AuthContext.Provider value={{ token, role, userId, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};