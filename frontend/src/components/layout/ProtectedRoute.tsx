// ==============================================================================
// AI KARMAYOGI — PROTECTED ROUTE COMPONENT
// Enforces Authentication and Role-Based Access Control (RBAC)
// ==============================================================================

import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { UserRole } from '@/types';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: UserRole[];
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles }) => {
  const { isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="flex flex-col items-center space-y-3">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-emerald-600 border-t-transparent" />
          <p className="text-sm font-medium text-slate-500">Verifying security credentials...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If specific roles required, check normalized role
  if (allowedRoles && allowedRoles.length > 0) {
    const userRole = user.role;
    const isAllowed =
      allowedRoles.includes(userRole) ||
      (userRole === 'administrator' && allowedRoles.includes('admin')) ||
      (userRole === 'admin' && allowedRoles.includes('administrator')) ||
      (userRole === 'department_head' && allowedRoles.includes('admin'));

    if (!isAllowed) {
      return <Navigate to="/unauthorized" replace />;
    }
  }

  return <>{children}</>;
};
