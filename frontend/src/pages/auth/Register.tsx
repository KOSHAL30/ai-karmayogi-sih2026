// ==============================================================================
// AI KARMAYOGI — OFFICIAL REGISTRATION INTERFACE
// Civil Servant Self-Onboarding & Role Assignment
// ==============================================================================

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { api } from '@/lib/api';
import { Compass, ShieldCheck, AlertCircle, CheckCircle2 } from 'lucide-react';

export const Register: React.FC = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    designation: '',
    roleCode: 'learner',
    departmentCode: 'DEPT-DOPT',
    password: '',
    confirmPassword: '',
  });

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Password requirements calculation
  const pwd = formData.password;
  const hasMinLength = pwd.length >= 8;
  const hasUpper = /[A-Z]/.test(pwd);
  const hasLower = /[a-z]/.test(pwd);
  const hasDigit = /\d/.test(pwd);
  const hasSpecial = /[@$!%*?&#^()_+=-]/.test(pwd);
  const isPasswordValid = hasMinLength && hasUpper && hasLower && hasDigit && hasSpecial;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!isPasswordValid) {
      setError('Password does not satisfy government security complexity policy.');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Password and confirmation password do not match.');
      return;
    }

    setLoading(true);

    try {
      await api.post('/auth/register', {
        full_name: formData.fullName,
        email: formData.email,
        designation: formData.designation,
        role_code: formData.roleCode,
        department_code: formData.departmentCode,
        password: formData.password,
      });

      setSuccess('Account provisioned successfully! Redirecting to login portal...');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err: any) {
      setError(err.message || 'Registration failed. Please check inputs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12 bg-slate-50 ">
      <div className="w-full max-w-lg space-y-6">
        {/* Emblem & Portal Title */}
        <div className="text-center space-y-2">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-500 text-white shadow-lg shadow-emerald-600/25">
            <Compass className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-slate-100 ">
            Official Registration
          </h1>
          <p className="text-xs text-slate-500 ">
            Provision access to the AI Karmayogi Competency Diagnostic Framework
          </p>
        </div>

        <Card className="shadow-xl border-slate-200/80 ">
          <CardHeader className="space-y-1 pb-4">
            <CardTitle className="text-xl">Create your account</CardTitle>
            <CardDescription>
              Enter your verified civil service details and credentials.
            </CardDescription>
          </CardHeader>

          <CardContent>
            {error && (
              <div className="mb-4 flex items-center gap-2 p-3 rounded-lg bg-rose-50 /40 text-rose-700  border border-rose-200  text-xs font-medium">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {success && (
              <div className="mb-4 flex items-center gap-2 p-3 rounded-lg bg-emerald-50 /40 text-emerald-700  border border-emerald-200  text-xs font-medium">
                <CheckCircle2 className="h-4 w-4 shrink-0" />
                <span>{success}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label htmlFor="fullName" required>
                    Full Name
                  </Label>
                  <Input
                    id="fullName"
                    placeholder="Rajesh Kumar"
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                    required
                  />
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="designation" required>
                    Designation
                  </Label>
                  <Input
                    id="designation"
                    placeholder="Under Secretary"
                    value={formData.designation}
                    onChange={(e) => setFormData({ ...formData, designation: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="email" required>
                  Government Email Address
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="rajesh.kumar@gov.in"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label htmlFor="roleCode" required>
                    Assigned Role
                  </Label>
                  <select
                    id="roleCode"
                    value={formData.roleCode}
                    onChange={(e) => setFormData({ ...formData, roleCode: e.target.value })}
                    className="flex h-10 w-full rounded-lg border border-slate-300  bg-white  px-3 py-2 text-sm text-slate-900 dark:text-slate-100  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
                  >
                    <option value="learner">Learner (Civil Services Official)</option>
                    <option value="trainer">Trainer (Capacity Building Faculty)</option>
                    <option value="admin">Admin (Department Governance Lead)</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="departmentCode" required>
                    Cadre / Department
                  </Label>
                  <select
                    id="departmentCode"
                    value={formData.departmentCode}
                    onChange={(e) => setFormData({ ...formData, departmentCode: e.target.value })}
                    className="flex h-10 w-full rounded-lg border border-slate-300  bg-white  px-3 py-2 text-sm text-slate-900 dark:text-slate-100  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500"
                  >
                    <option value="DEPT-DOPT">Personnel & Training (DoPT)</option>
                    <option value="DEPT-MEITY">Electronics & IT (MeitY)</option>
                    <option value="DEPT-FIN">Economic Affairs (Finance)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label htmlFor="password" required>
                    Password
                  </Label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••••••"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                  />
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="confirmPassword" required>
                    Confirm Password
                  </Label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    placeholder="••••••••••••"
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                    required
                  />
                </div>
              </div>

              {/* Password complexity hints */}
              <div className="rounded-lg bg-slate-50 /50 p-3 text-[11px] space-y-1 border border-slate-200 ">
                <p className="font-semibold text-slate-600 dark:text-slate-300 ">Security Requirement Checklist:</p>
                <div className="grid grid-cols-2 gap-1 text-slate-500 ">
                  <span className={hasMinLength ? 'text-teal-600 font-medium' : ''}>
                    {hasMinLength ? '✓' : '•'} 8+ characters
                  </span>
                  <span className={hasUpper ? 'text-teal-600 font-medium' : ''}>
                    {hasUpper ? '✓' : '•'} 1 Uppercase letter
                  </span>
                  <span className={hasLower ? 'text-teal-600 font-medium' : ''}>
                    {hasLower ? '✓' : '•'} 1 Lowercase letter
                  </span>
                  <span className={hasDigit && hasSpecial ? 'text-teal-600 font-medium' : ''}>
                    {hasDigit && hasSpecial ? '✓' : '•'} Number & Special symbol
                  </span>
                </div>
              </div>

              <Button type="submit" className="w-full" isLoading={loading} disabled={!isPasswordValid}>
                Register Account
              </Button>
            </form>
          </CardContent>

          <CardFooter className="flex justify-center border-t border-slate-100  pt-4">
            <p className="text-xs text-slate-500 ">
              Already have an official account?{' '}
              <Link to="/login" className="font-semibold text-teal-600  hover:underline">
                Sign In
              </Link>
            </p>
          </CardFooter>
        </Card>

        <div className="flex items-center justify-center gap-1.5 text-[11px] text-slate-600 dark:text-slate-300">
          <ShieldCheck className="h-3.5 w-3.5 text-teal-600" />
          <span>Sovereign Local Self-Hosted Infrastructure (Zero External Telemetry)</span>
        </div>
      </div>
    </div>
  );
};
