import { create } from 'zustand';
import type { ToastProps, ToastType } from '../components/common/Toast';

interface NotificationState {
  toasts: ToastProps[];
  addToast: (type: ToastType, title: string, message?: string, duration?: number) => void;
  removeToast: (id: string) => void;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  toasts: [],

  addToast: (type, title, message, duration = 5000) => {
    const id = Math.random().toString(36).substring(7);
    const toast: ToastProps = {
      id,
      type,
      title,
      message,
      duration,
      isVisible: true,
      onClose: () => {
        set((state) => ({
          toasts: state.toasts.map((t) =>
            t.id === id ? { ...t, isVisible: false } : t
          ),
        }));
        // Remove from array after animation completes
        setTimeout(() => {
          set((state) => ({
            toasts: state.toasts.filter((t) => t.id !== id),
          }));
        }, 300);
      },
    };

    set((state) => ({
      toasts: [...state.toasts, toast],
    }));

    // Auto-dismiss after duration
    if (duration > 0) {
      setTimeout(() => {
        toast.onClose();
      }, duration);
    }
  },

  removeToast: (id) => {
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    }));
  },
}));
