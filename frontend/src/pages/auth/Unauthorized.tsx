// ==============================================================================
// AI KARMAYOGI — 403 UNAUTHORIZED / RBAC RESTRICTION
// Sovereign Government Access Boundary Notification
// ==============================================================================

import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ShieldAlert, ArrowLeft, Home } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

export const Unauthorized: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12 bg-slate-50 ">
      <div className="w-full max-w-md space-y-6 text-center">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-amber-100 /40 text-amber-600 ">
          <ShieldAlert className="h-8 w-8" />
        </div>

        <Card className="shadow-xl border-slate-200/80  text-left">
          <CardHeader className="text-center pb-3">
            <CardTitle className="text-xl text-slate-900 ">
              Access Restricted (403)
            </CardTitle>
            <CardDescription>
              Your civil service profile does not possess the requisite role clearance for this module.
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-3 text-xs text-slate-600 ">
            <div className="p-3 rounded-lg bg-slate-50 /60 border border-slate-200  space-y-1">
              <p>
                <span className="font-semibold text-slate-900 ">Current Officer:</span>{' '}
                {user?.full_name || 'Authenticated Official'}
              </p>
              <p>
                <span className="font-semibold text-slate-900 ">Designated Role:</span>{' '}
                <span className="capitalize font-medium text-teal-600 ">{user?.role}</span>
              </p>
              <p>
                <span className="font-semibold text-slate-900 ">Cadre/Ministry:</span>{' '}
                {user?.department}
              </p>
            </div>
            <p>
              Under Mission Karmayogi role-based governance, administrative and faculty modules require explicit authorization.
            </p>
          </CardContent>

          <CardFooter className="flex gap-2 border-t border-slate-100  pt-4">
            <Link to="/" className="flex-1">
              <Button variant="primary" className="w-full">
                <Home className="h-4 w-4 mr-1.5" />
                Return to Overview
              </Button>
            </Link>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};
