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
    token: null,
    isAuthenticated: false,
    isLoading: true,
  });

  const fetchProfile = async () => {
    try {
      const user = await api.get<UserProfile>('/auth/me');
      setState({
        user,
        token: 'cookie-based',
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (err) {
      setState({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const login = async (email: string, password: string = 'Karmayogi2026!') => {
    setState((prev) => ({ ...prev, isLoading: true }));
    try {
      const res = await api.post<{ access_token: string; refresh_token?: string; user: UserProfile }>('/auth/login', {
        email,
        password,
      });

      
      if (res.refresh_token) {
        
      }
      setState({
        user: res.user,
        token: 'cookie-based',
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error) {
      setState((prev) => ({ ...prev, isLoading: false }));
      throw error;
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout', {});
    } catch (e) {}
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
  };

  const refreshProfile = async () => {
    await fetchProfile();
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
