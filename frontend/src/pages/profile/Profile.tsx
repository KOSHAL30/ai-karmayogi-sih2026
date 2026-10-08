// ==============================================================================
// AI KARMAYOGI — OFFICER PROFILE & SECURITY SETTINGS
// Civil Servant Profile View, Identity Verification, and Password Rotation
// ==============================================================================

import React, { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/lib/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  User as UserIcon,
  Shield,
  Building,
  Briefcase,
  KeyRound,
  CheckCircle2,
  AlertCircle,
  Award,
} from 'lucide-react';

export const Profile: React.FC = () => {
  const { user, refreshProfile } = useAuth();

  // Profile update form state
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [designation, setDesignation] = useState(user?.designation || '');
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileSuccess, setProfileSuccess] = useState<string | null>(null);
  const [profileError, setProfileError] = useState<string | null>(null);

  // Password change form state
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [pwdLoading, setPwdLoading] = useState(false);
  const [pwdSuccess, setPwdSuccess] = useState<string | null>(null);
  const [pwdError, setPwdError] = useState<string | null>(null);

  // Sync state if user loads later
  React.useEffect(() => {
    if (user) {
      setFullName(user.full_name);
      setDesignation(user.designation);
    }
  }, [user]);

  // Password validation
  const hasMinLength = newPassword.length >= 8;
  const hasUpper = /[A-Z]/.test(newPassword);
  const hasLower = /[a-z]/.test(newPassword);
  const hasDigit = /\d/.test(newPassword);
  const hasSpecial = /[@$!%*?&#^()_+=-]/.test(newPassword);
  const isPasswordValid = hasMinLength && hasUpper && hasLower && hasDigit && hasSpecial;

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileSuccess(null);
    setProfileError(null);
    setProfileLoading(true);

    try {
      await api.put('/users/me', {
        full_name: fullName,
        designation: designation,
      });
      await refreshProfile();
      setProfileSuccess('Civil servant credentials updated successfully.');
    } catch (err: any) {
      setProfileError(err.message || 'Failed to update profile.');
    } finally {
      setProfileLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPwdSuccess(null);
    setPwdError(null);

    if (!isPasswordValid) {
      setPwdError('New password does not meet required security complexity.');
      return;
    }

    if (newPassword !== confirmPassword) {
      setPwdError('New password and confirmation do not match.');
      return;
    }

    setPwdLoading(true);

    try {
      await api.put('/users/me/password', {
        old_password: oldPassword,
        new_password: newPassword,
      });
      setPwdSuccess('Official password rotated and secured successfully.');
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      setPwdError(err.message || 'Failed to rotate password.');
    } finally {
      setPwdLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200  pb-6">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-slate-100 ">
            Officer Profile & Credentials
          </h1>
          <p className="text-sm text-slate-500  mt-1">
            Civil Services Capacity Building Ecosystem • FRAC Framework
          </p>
        </div>
        <div className="flex items-center gap-2 self-start md:self-auto">
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 /40 text-emerald-700  border border-emerald-200 ">
            <Shield className="h-3.5 w-3.5" />
            Verified Karmayogi Official
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Official Identity Card */}
        <div className="lg:col-span-1 space-y-6">
          <Card className="border-slate-200  shadow-sm">
            <CardHeader className="text-center pb-2">
              <div className="mx-auto h-20 w-20 rounded-full bg-gradient-to-tr from-emerald-600 to-emerald-400 flex items-center justify-center text-slate-900 dark:text-slate-100 text-2xl font-bold shadow-md shadow-emerald-600/20 mb-3">
                {user?.full_name
                  ? user.full_name
                      .split(' ')
                      .map((n) => n[0])
                      .slice(0, 2)
                      .join('')
                      .toUpperCase()
                  : 'GOV'}
              </div>
              <CardTitle className="text-lg">{user?.full_name}</CardTitle>
              <CardDescription className="text-xs">{user?.designation}</CardDescription>
            </CardHeader>

            <CardContent className="space-y-4 pt-2 border-t border-slate-100 ">
              <div className="space-y-2.5 text-xs">
                <div className="flex items-center justify-between py-1 border-b border-slate-100 /60">
                  <span className="text-slate-500 flex items-center gap-1.5">
                    <UserIcon className="h-3.5 w-3.5" /> Official Role
                  </span>
                  <span className="font-semibold capitalize text-slate-900 dark:text-slate-100 ">
                    {user?.role}
                  </span>
                </div>

                <div className="flex items-center justify-between py-1 border-b border-slate-100 /60">
                  <span className="text-slate-500 flex items-center gap-1.5">
                    <Building className="h-3.5 w-3.5" /> Cadre / Ministry
                  </span>
                  <span className="font-semibold text-slate-900 dark:text-slate-100  max-w-[150px] truncate text-right">
                    {user?.department}
                  </span>
                </div>

                <div className="flex items-center justify-between py-1 border-b border-slate-100 /60">
                  <span className="text-slate-500 flex items-center gap-1.5">
                    <Briefcase className="h-3.5 w-3.5" /> Work Role
                  </span>
                  <span className="font-semibold text-slate-900 dark:text-slate-100  max-w-[150px] truncate text-right">
                    {user?.work_role || 'General Officer'}
                  </span>
                </div>

                <div className="flex items-center justify-between py-1">
                  <span className="text-slate-500">Account Status</span>
                  <span className="font-semibold text-teal-600 ">
                    Active & Mandated
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Columns: Edit Profile & Password Rotation */}
        <div className="lg:col-span-2 space-y-6">
          {/* Edit Information Form */}
          <Card className="border-slate-200  shadow-sm">
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <UserIcon className="h-4 w-4 text-teal-600" />
                Update Profile Details
              </CardTitle>
              <CardDescription className="text-xs">
                Modify your displayed official name and administrative designation.
              </CardDescription>
            </CardHeader>

            <CardContent>
              {profileSuccess && (
                <div className="mb-4 flex items-center gap-2 p-3 rounded-lg bg-emerald-50 /40 text-emerald-700  border border-emerald-200  text-xs font-medium">
                  <CheckCircle2 className="h-4 w-4 shrink-0" />
                  <span>{profileSuccess}</span>
                </div>
              )}

              {profileError && (
                <div className="mb-4 flex items-center gap-2 p-3 rounded-lg bg-rose-50 /40 text-rose-700  border border-rose-200  text-xs font-medium">
                  <AlertCircle className="h-4 w-4 shrink-0" />
                  <span>{profileError}</span>
                </div>
              )}

              <form onSubmit={handleUpdateProfile} className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label htmlFor="profileFullName" required>
                      Full Name
                    </Label>
                    <Input
                      id="profileFullName"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="profileDesignation" required>
                      Designation
                    </Label>
                    <Input
                      id="profileDesignation"
                      value={designation}
                      onChange={(e) => setDesignation(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="profileEmail">Official Email (Locked)</Label>
                  <Input id="profileEmail" value={user?.email || ''} disabled />
                  <p className="text-[11px] text-slate-600 dark:text-slate-300">
                    Email updates require verified departmental administrative clearance.
                  </p>
                </div>

                <div className="flex justify-end pt-2">
                  <Button type="submit" isLoading={profileLoading}>
                    Save Changes
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>

          {/* Password Security Rotation */}
          <Card className="border-slate-200  shadow-sm">
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <KeyRound className="h-4 w-4 text-teal-600" />
                Rotate Security Password
              </CardTitle>
              <CardDescription className="text-xs">
                Enforce government credential hygiene with strong password standards.
              </CardDescription>
            </CardHeader>

            <CardContent>
              {pwdSuccess && (
                <div className="mb-4 flex items-center gap-2 p-3 rounded-lg bg-emerald-50 /40 text-emerald-700  border border-emerald-200  text-xs font-medium">
                  <CheckCircle2 className="h-4 w-4 shrink-0" />
                  <span>{pwdSuccess}</span>
                </div>
              )}

              {pwdError && (
                <div className="mb-4 flex items-center gap-2 p-3 rounded-lg bg-rose-50 /40 text-rose-700  border border-rose-200  text-xs font-medium">
                  <AlertCircle className="h-4 w-4 shrink-0" />
                  <span>{pwdError}</span>
                </div>
              )}

              <form onSubmit={handleChangePassword} className="space-y-4">
                <div className="space-y-1.5">
                  <Label htmlFor="oldPassword" required>
                    Current Password
                  </Label>
                  <Input
                    id="oldPassword"
                    type="password"
                    placeholder="••••••••••••"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    required
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label htmlFor="newPassword" required>
                      New Password
                    </Label>
                    <Input
                      id="newPassword"
                      type="password"
                      placeholder="••••••••••••"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      required
                    />
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="confirmPassword" required>
                      Confirm New Password
                    </Label>
                    <Input
                      id="confirmPassword"
                      type="password"
                      placeholder="••••••••••••"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                    />
                  </div>
                </div>

                {newPassword && (
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
                )}

                <div className="flex justify-end pt-2">
                  <Button type="submit" isLoading={pwdLoading} disabled={!isPasswordValid || !oldPassword}>
                    Update Password
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};
