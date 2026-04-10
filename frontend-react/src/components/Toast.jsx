import { useEffect } from 'react';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';

const Toast = ({ message, type = 'info', onClose, duration = 3000 }) => {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const config = {
    success: {
      icon: CheckCircle,
      bg: 'bg-green-500/10',
      border: 'border-green-500/30',
      text: 'text-green-500',
    },
    error: {
      icon: AlertCircle,
      bg: 'bg-rose-500/10',
      border: 'border-rose-500/30',
      text: 'text-rose-500',
    },
    info: {
      icon: Info,
      bg: 'bg-gold/10',
      border: 'border-gold/30',
      text: 'text-gold',
    },
  };

  const { icon: Icon, bg, border, text } = config[type];

  return (
    <div
      className={`${bg} ${border} ${text} border rounded-xl p-4 shadow-lg backdrop-blur-sm animate-slide-in-right flex items-center gap-3 min-w-[300px] max-w-md`}
    >
      <Icon size={20} className="flex-shrink-0" />
      <p className="flex-1 text-sm font-semibold">{message}</p>
      <button
        onClick={onClose}
        className="flex-shrink-0 hover:opacity-70 transition-opacity"
      >
        <X size={16} />
      </button>
    </div>
  );
};

export default Toast;
