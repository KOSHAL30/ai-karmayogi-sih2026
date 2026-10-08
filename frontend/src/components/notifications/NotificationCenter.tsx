// ==============================================================================
// AI KARMAYOGI — IN-APP NOTIFICATION CENTER
// Real-Time Administrative Circulars, Assessment Deadlines & Priority Filtering
// ==============================================================================

import React, { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { NotificationItem, NotificationListData } from '@/types';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import {
  Bell,
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  Award,
  Sparkles,
  Info,
  Clock,
  Check,
  X,
  ExternalLink,
  ChevronRight,
  ShieldAlert,
} from 'lucide-react';

interface NotificationCenterProps {
  onClose?: () => void;
  onCountChange?: (unreadCount: number) => void;
}

export const NotificationCenter: React.FC<NotificationCenterProps> = ({
  onClose,
  onCountChange,
}) => {
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [unreadCount, setUnreadCount] = useState<number>(0);
  const [filter, setFilter] = useState<'all' | 'unread' | 'urgent'>('all');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    setIsLoading(true);
    try {
      const data = await api.get<NotificationListData>('/notifications');
      setNotifications(data.notifications || []);
      setUnreadCount(data.unread_count || 0);
      if (onCountChange) onCountChange(data.unread_count || 0);
    } catch (err) {
      console.error('Failed to load notifications:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMarkAsRead = async (id: string, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    try {
      await api.post('/notifications/read', { notification_id: id });
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
      const newCount = Math.max(0, unreadCount - 1);
      setUnreadCount(newCount);
      if (onCountChange) onCountChange(newCount);
    } catch (err) {
      console.error('Failed to mark read:', err);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await api.post('/notifications/read-all', {});
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
      setUnreadCount(0);
      if (onCountChange) onCountChange(0);
    } catch (err) {
      console.error('Failed to mark all read:', err);
    }
  };

  const handleActionClick = (note: NotificationItem) => {
    if (!note.is_read) {
      handleMarkAsRead(note.id);
    }
    if (note.action_url) {
      if (onClose) onClose();
      navigate(note.action_url);
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'URGENT':
        return 'bg-rose-100 text-rose-800   border-rose-300 ';
      case 'HIGH':
        return 'bg-amber-100 text-amber-800   border-amber-300 ';
      case 'NORMAL':
        return 'bg-teal-100 text-teal-800   border-teal-300 ';
      case 'LOW':
      default:
        return 'bg-slate-100 text-slate-700   border-slate-200 ';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'COURSE_ASSIGNED':
        return <BookOpen className="h-4 w-4 text-teal-600" />;
      case 'ASSESSMENT_REMINDER':
        return <AlertTriangle className="h-4 w-4 text-amber-500" />;
      case 'CERTIFICATE_AVAILABLE':
        return <Award className="h-4 w-4 text-teal-600" />;
      case 'MILESTONE':
        return <Sparkles className="h-4 w-4 text-purple-500" />;
      case 'ANNOUNCEMENT':
      default:
        return <Info className="h-4 w-4 text-teal-500" />;
    }
  };

  const filteredNotes = notifications.filter((n) => {
    if (filter === 'unread') return !n.is_read;
    if (filter === 'urgent') return n.priority === 'URGENT' || n.priority === 'HIGH';
    return true;
  });

  return (
    <div className="flex flex-col h-full max-h-[580px] w-full sm:w-[420px] bg-white  rounded-2xl border border-slate-200  shadow-2xl overflow-hidden animate-in fade-in slide-in-from-top-2 duration-150">
      {/* Header */}
      <div className="p-4 border-b border-slate-100  bg-slate-50/60 /60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="relative">
            <Bell className="h-4 w-4 text-slate-700 " />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-rose-500 animate-pulse" />
            )}
          </div>
          <h3 className="text-xs font-bold text-slate-900 dark:text-slate-100 ">
            Administrative Notification Center
          </h3>
          {unreadCount > 0 && (
            <span className="text-[10px] font-bold px-1.5 py-0.2 rounded-full bg-emerald-100  text-emerald-700 ">
              {unreadCount} unread
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {unreadCount > 0 && (
            <button
              onClick={handleMarkAllRead}
              className="text-[11px] text-teal-600  font-semibold hover:underline"
            >
              Mark all read
            </button>
          )}
          {onClose && (
            <button
              onClick={onClose}
              className="p-1 rounded-lg text-slate-600 dark:text-slate-300 hover:text-slate-600 dark:text-slate-300"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-1 px-4 py-2 border-b border-slate-100  text-xs bg-slate-50/30 /20">
        <button
          onClick={() => setFilter('all')}
          className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
            filter === 'all'
              ? 'bg-slate-200  text-slate-900 dark:text-slate-100  font-bold'
              : 'text-slate-500 hover:text-slate-900 dark:text-slate-100'
          }`}
        >
          All ({notifications.length})
        </button>
        <button
          onClick={() => setFilter('unread')}
          className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
            filter === 'unread'
              ? 'bg-slate-200  text-slate-900 dark:text-slate-100  font-bold'
              : 'text-slate-500 hover:text-slate-900 dark:text-slate-100'
          }`}
        >
          Unread ({unreadCount})
        </button>
        <button
          onClick={() => setFilter('urgent')}
          className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
            filter === 'urgent'
              ? 'bg-slate-200  text-slate-900 dark:text-slate-100  font-bold'
              : 'text-slate-500 hover:text-slate-900 dark:text-slate-100'
          }`}
        >
          Urgent / High
        </button>
      </div>

      {/* Notifications List */}
      <div className="flex-1 overflow-y-auto divide-y divide-slate-100 ">
        {isLoading ? (
          <div className="py-12 text-center text-xs text-slate-600 dark:text-slate-300">Loading alerts...</div>
        ) : filteredNotes.length === 0 ? (
          <div className="py-12 text-center text-xs text-slate-600 dark:text-slate-300 space-y-1">
            <CheckCircle2 className="h-6 w-6 text-slate-600 dark:text-slate-300  mx-auto mb-1" />
            <p>You're all caught up!</p>
            <p className="text-[10px]">No notifications matching your filter.</p>
          </div>
        ) : (
          filteredNotes.map((note) => (
            <div
              key={note.id}
              onClick={() => handleActionClick(note)}
              className={`p-3.5 hover:bg-slate-50  cursor-pointer transition-colors space-y-1.5 ${
                !note.is_read ? 'bg-emerald-50/20 /10' : ''
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <div className="p-1 rounded-md bg-slate-100 ">
                    {getTypeIcon(note.notification_type)}
                  </div>
                  <span className={`text-[9px] font-bold px-1.5 py-0.2 rounded border ${getPriorityBadge(note.priority)}`}>
                    {note.priority}
                  </span>
                </div>

                <div className="flex items-center gap-1.5">
                  <span className="text-[10px] text-slate-600 dark:text-slate-300 flex items-center gap-1">
                    <Clock className="h-2.5 w-2.5" />
                    {new Date(note.created_at).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}
                  </span>
                  {!note.is_read && (
                    <button
                      onClick={(e) => handleMarkAsRead(note.id, e)}
                      title="Mark as read"
                      className="p-1 text-slate-600 dark:text-slate-300 hover:text-teal-600"
                    >
                      <Check className="h-3 w-3" />
                    </button>
                  )}
                </div>
              </div>

              <h4 className={`text-xs ${!note.is_read ? 'font-bold text-slate-900 dark:text-slate-100 ' : 'font-medium text-slate-700 '}`}>
                {note.title}
              </h4>

              <p className="text-[11px] text-slate-500  leading-relaxed">
                {note.message}
              </p>

              {note.action_url && (
                <div className="pt-1 flex items-center gap-1 text-[10px] font-bold text-teal-600 ">
                  <span>Take Action</span>
                  <ChevronRight className="h-3 w-3" />
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
