import { X, Terminal, Skull, User, Clock, Calendar, FileText, Shield } from 'lucide-react';
import { format, formatDistanceToNow } from 'date-fns';
import { useToast } from '../contexts/ToastContext';

const HeistDetailsModal = ({ heist, isOpen, onClose, onAbort, currentUsername }) => {
  const toast = useToast();

  if (!isOpen || !heist) return null;

  // Check if current user is the creator
  const isCreator = currentUsername === heist.creator_username;
  const canAbort = isCreator && heist.status === 'Active';

  // Status badge colors
  const statusColors = {
    Active: 'bg-green-500/10 text-green-500 border-green-500/30',
    Completed: 'bg-blue-500/10 text-blue-500 border-blue-500/30',
    Expired: 'bg-rose-500/10 text-rose-500 border-rose-500/30',
    Aborted: 'bg-rose-500/10 text-rose-500 border-rose-500/30',
  };

  // Difficulty badge colors
  const difficultyColors = {
    Training: 'bg-slate-500/10 text-slate-500 border-slate-500/30',
    Easy: 'bg-green-500/10 text-green-500 border-green-500/30',
    Medium: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/30',
    Hard: 'bg-orange-500/10 text-orange-500 border-orange-500/30',
    Legendary: 'bg-rose-500/10 text-rose-500 border-rose-500/30',
  };

  // Format dates
  const formatDeadline = (deadline) => {
    try {
      const deadlineDate = new Date(deadline);
      const now = new Date();

      if (deadlineDate < now) {
        return {
          absolute: format(deadlineDate, 'PPpp'),
          relative: 'EXPIRED',
          isExpired: true,
        };
      }

      return {
        absolute: format(deadlineDate, 'PPpp'),
        relative: formatDistanceToNow(deadlineDate, { addSuffix: true }),
        isExpired: false,
      };
    } catch {
      return {
        absolute: 'Invalid date',
        relative: 'Invalid date',
        isExpired: false,
      };
    }
  };

  const formatCreatedAt = (createdAt) => {
    try {
      return format(new Date(createdAt), 'PPpp');
    } catch {
      return 'Invalid date';
    }
  };

  const deadline = formatDeadline(heist.deadline);

  const handleAbort = () => {
    if (window.confirm(`Are you sure you want to abort "${heist.title}"?`)) {
      onAbort(heist.id);
      toast.info('Aborting mission...');
      onClose();
    }
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/80 backdrop-blur-sm z-40 animate-fade-in"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div
          className="bg-dark-card border border-slate-800 rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto pointer-events-auto animate-scale-in"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="sticky top-0 bg-dark-card/95 backdrop-blur-md border-b border-slate-800 p-6 flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <span className={`text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full border ${statusColors[heist.status]}`}>
                  {heist.status}
                </span>
                <span className={`text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full border ${difficultyColors[heist.difficulty]}`}>
                  {heist.difficulty}
                </span>
              </div>
              <h2 className="text-2xl font-black text-white mb-1">
                {heist.title}
              </h2>
              <p className="text-xs text-slate-500 uppercase tracking-widest">
                Mission #{heist.id.toString().padStart(4, '0')}
              </p>
            </div>

            {/* Close Button */}
            <button
              onClick={onClose}
              className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
            >
              <X size={24} className="text-slate-400" />
            </button>
          </div>

          {/* Content */}
          <div className="p-6 space-y-6">
            {/* Description */}
            {heist.description && (
              <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-3">
                  <FileText size={16} className="text-gold" />
                  <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                    Intel Briefing
                  </h3>
                </div>
                <p className="text-slate-300 text-sm leading-relaxed">
                  {heist.description}
                </p>
              </div>
            )}

            {/* Mission Details Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Target */}
              <DetailItem
                icon={<Terminal size={18} />}
                label="Target Sector"
                value={heist.target}
              />

              {/* Assignee */}
              <DetailItem
                icon={<User size={18} />}
                label="Assigned Operative"
                value={heist.assignee_username}
              />

              {/* Creator */}
              <DetailItem
                icon={<Shield size={18} />}
                label="Mission Creator"
                value={heist.creator_username}
                highlight={isCreator}
              />

              {/* Created At */}
              <DetailItem
                icon={<Calendar size={18} />}
                label="Created"
                value={formatCreatedAt(heist.created_at)}
              />
            </div>

            {/* Deadline Section */}
            <div className={`border rounded-xl p-4 ${
              deadline.isExpired
                ? 'bg-rose-500/10 border-rose-500/30'
                : 'bg-gold/10 border-gold/30'
            }`}>
              <div className="flex items-center gap-2 mb-3">
                <Clock size={18} className={deadline.isExpired ? 'text-rose-500' : 'text-gold'} />
                <h3 className="text-sm font-bold uppercase tracking-wider">
                  <span className={deadline.isExpired ? 'text-rose-500' : 'text-gold'}>
                    {deadline.isExpired ? 'Mission Expired' : 'Time Remaining'}
                  </span>
                </h3>
              </div>
              <div className="space-y-1">
                <p className={`text-lg font-bold ${deadline.isExpired ? 'text-rose-500' : 'text-gold'}`}>
                  {deadline.relative}
                </p>
                <p className="text-xs text-slate-400">
                  Deadline: {deadline.absolute}
                </p>
              </div>
            </div>

            {/* Abort Button */}
            {canAbort && (
              <button
                onClick={handleAbort}
                className="w-full bg-rose-500/10 hover:bg-rose-500/20 text-rose-500 border border-rose-500/30 font-bold py-3 rounded-xl transition-all uppercase tracking-wider text-sm"
              >
                Abort Mission
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Add animation styles */}
      <style>{`
        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes scale-in {
          from {
            opacity: 0;
            transform: scale(0.95);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }
        .animate-fade-in {
          animation: fade-in 0.2s ease-out;
        }
        .animate-scale-in {
          animation: scale-in 0.2s ease-out;
        }
      `}</style>
    </>
  );
};

// DetailItem sub-component
const DetailItem = ({ icon, label, value, highlight = false }) => (
  <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
    <div className="flex items-center gap-2 mb-2">
      <span className="text-slate-500">{icon}</span>
      <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
        {label}
      </span>
    </div>
    <p className={`font-mono text-sm ${highlight ? 'text-gold font-bold' : 'text-white'}`}>
      {value}
    </p>
  </div>
);

export default HeistDetailsModal;
