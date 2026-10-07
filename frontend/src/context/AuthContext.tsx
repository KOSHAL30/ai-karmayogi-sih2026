// ==============================================================================
// AI KARMAYOGI — AUTHENTICATION CONTEXT PROVIDER
// JWT Storage, Session Restoration, and 3-Role Demo Persona Support
// ==============================================================================

import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserProfile, AuthState, UserRole } from '@/types';
import { api } from '@/lib/api';

interface AuthContextType extends AuthState {
  login: (email: string, password?: string) => Promise<void>;
  logout: () => void;
  switchPersona: (role: UserRole) => Promise<void>;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Preset demo personas for SIH evaluation (3 Core Roles)
export const DEMO_PERSONAS: Record<string, { email: string; name: string; title: string; dept: string; role: UserRole }> = {
  learner: {
    email: 'rajesh.kumar@gov.in',
    name: 'Rajesh Kumar',
    title: 'Under Secretary (Establishment)',
    dept: 'Department of Personnel and Training',
    role: 'learner',
  },
  trainer: {
    email: 'sunita.deshmukh@nic.in',
    name: 'Dr. Sunita Deshmukh',
    title: 'Senior Training Faculty (ISTM)',
    dept: 'Institute of Secretariat Training & Management',
    role: 'trainer',
  },
  admin: {
    email: 'priya.nair@karmayogi.gov.in',
    name: 'Dr. Priya Nair',
    title: 'Director (Capacity Building & Analytics)',
    dept: 'Department of Personnel and Training',
    role: 'admin',
  },
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: localStorage.getItem('karmayogi_token'),
    isAuthenticated: false,
    isLoading: true,
  });

  const fetchProfile = async (token: string) => {
    try {
      const user = await api.get<UserProfile>('/auth/me');
      setState({
        user,
        token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (err) {
      console.warn('Session expired or invalid token. Resetting...');
      localStorage.removeItem('karmayogi_token');
      localStorage.removeItem('karmayogi_refresh_token');
      setState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('karmayogi_token');
    if (!token) {
      setState((prev) => ({ ...prev, isLoading: false, isAuthenticated: false, user: null }));
      return;
    }
    fetchProfile(token);
  }, []);

  const login = async (email: string, password: string = 'Karmayogi2026!') => {
    setState((prev) => ({ ...prev, isLoading: true }));
    try {
      const res = await api.post<{ access_token: string; refresh_token?: string; user: UserProfile }>('/auth/login', {
        email,
        password,
      });

      localStorage.setItem('karmayogi_token', res.access_token);
      if (res.refresh_token) {
        localStorage.setItem('karmayogi_refresh_token', res.refresh_token);
      }
      setState({
        user: res.user,
        token: res.access_token,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      setState((prev) => ({ ...prev, isLoading: false }));
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('karmayogi_token');
    localStorage.removeItem('karmayogi_refresh_token');
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
  };

  const refreshProfile = async () => {
    const token = localStorage.getItem('karmayogi_token');
    if (token) {
      await fetchProfile(token);
    }
  };

  const switchPersona = async (role: UserRole) => {
    const normalizedKey = (role === 'administrator' || role === 'department_head') ? 'admin' : role;
    const persona = DEMO_PERSONAS[normalizedKey] || DEMO_PERSONAS.learner;
    await login(persona.email, 'Karmayogi2026!');
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout, switchPersona, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
