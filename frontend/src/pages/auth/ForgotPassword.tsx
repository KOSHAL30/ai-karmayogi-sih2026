// ==============================================================================
// AI KARMAYOGI — FORGOT PASSWORD / CREDENTIAL RECOVERY
// Sovereign Recovery Workflow for Civil Servants
// ==============================================================================

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Compass, CheckCircle2, ArrowLeft, Shield } from 'lucide-react';

export const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Simulate secure recovery trigger
    setTimeout(() => {
      setLoading(false);
      setSubmitted(true);
    }, 800);
  };

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12 bg-slate-50 ">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-500 text-white shadow-lg shadow-emerald-600/25">
            <Compass className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-slate-100 ">
            Credential Recovery
          </h1>
          <p className="text-xs text-slate-500 ">
            Secure password reset for civil service officials
          </p>
        </div>

        <Card className="shadow-xl border-slate-200/80 ">
          <CardHeader className="space-y-1 pb-4">
            <CardTitle className="text-xl">Reset your password</CardTitle>
            <CardDescription>
              Enter your registered government email to receive reset instructions or contact your departmental Nodal Officer.
            </CardDescription>
          </CardHeader>

          <CardContent>
            {submitted ? (
              <div className="space-y-4">
                <div className="flex items-start gap-3 p-4 rounded-xl bg-emerald-50 /40 text-emerald-800  border border-emerald-200  text-xs">
                  <CheckCircle2 className="h-5 w-5 text-teal-600 shrink-0 mt-0.5" />
                  <div className="space-y-1">
                    <p className="font-bold">Reset Instructions Dispatched</p>
                    <p>
                      If <span className="font-semibold">{email}</span> matches an active civil service account, an authenticated reset dispatch has been logged.
                    </p>
                    <p className="text-[11px] text-emerald-700/80  mt-2">
                      For hackathon evaluation: All demo accounts use the standard password <span className="font-mono font-bold">Karmayogi2026!</span>
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-1.5">
                  <Label htmlFor="email" required>
                    Registered Government Email
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="rajesh.kumar@gov.in"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>

                <Button type="submit" className="w-full" isLoading={loading}>
                  Dispatch Reset Link
                </Button>
              </form>
            )}
          </CardContent>

          <CardFooter className="flex justify-center border-t border-slate-100  pt-4">
            <Link
              to="/login"
              className="flex items-center gap-1.5 text-xs font-semibold text-teal-600  hover:underline"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              Return to Login Portal
            </Link>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
};
