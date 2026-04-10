import { useState } from 'react';
import { Terminal, Skull, User, Clock, ChevronRight } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import HeistDetailsModal from './HeistDetailsModal';

const HeistCard = ({ heist, onAbort, currentUsername }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Status badge colors
  const statusColors = {
    Active: 'text-green-500 border-green-500/20',
    Completed: 'text-blue-500 border-blue-500/20',
    Expired: 'text-rose-500 border-rose-500/20',
    Aborted: 'text-rose-500 border-rose-500/20',
  };

  // Difficulty highlight (Extreme/Legendary in red)
  const isDangerousDifficulty = ['Extreme', 'Legendary'].includes(heist.difficulty);

  // Check if current user is the creator
  const isCreator = currentUsername === heist.creator_username;

  // Format deadline
  const formatDeadline = (deadline) => {
    try {
      const deadlineDate = new Date(deadline);
      const now = new Date();

      if (deadlineDate < now) {
        return 'EXPIRED';
      }

      return formatDistanceToNow(deadlineDate, { addSuffix: false });
    } catch {
      return 'Invalid date';
    }
  };

  const handleAbort = () => {
    if (window.confirm(`Are you sure you want to abort "${heist.title}"?`)) {
      onAbort(heist.id);
    }
  };

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <div className="bg-dark-card border border-slate-800 rounded-2xl overflow-hidden hover:border-gold/40 transition-all group relative">
        <div className="p-6">
          {/* Status and ID */}
          <div className="flex justify-between items-start mb-4">
            <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-1 rounded bg-slate-900 border ${statusColors[heist.status]}`}>
              {heist.status}
            </span>
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">
              #{heist.id.toString().padStart(4, '0')}
            </span>
          </div>

          {/* Title */}
          <h3 className="text-xl font-bold text-white mb-2 group-hover:text-gold transition-colors">
            {heist.title}
          </h3>

          {/* Description */}
          {heist.description && (
            <p className="text-slate-400 text-sm mb-6 line-clamp-2">
              {heist.description}
            </p>
          )}

          {/* Info Rows */}
          <div className="space-y-3">
            {/* Target */}
            <InfoRow
              icon={<Terminal size={14} />}
              label="Target"
              value={heist.target}
            />

            {/* Difficulty */}
            <InfoRow
              icon={<Skull size={14} />}
              label="Difficulty"
              value={heist.difficulty}
              highlight={isDangerousDifficulty}
            />

            {/* Operative */}
            <InfoRow
              icon={<User size={14} />}
              label="Operative"
              value={heist.assignee_username}
            />

            {/* Time Remaining */}
            <InfoRow
              icon={<Clock size={14} />}
              label="Time Remaining"
              value={formatDeadline(heist.deadline)}
            />
          </div>
        </div>

        {/* Footer */}
        <div className="bg-slate-900/50 p-4 border-t border-slate-800 flex justify-between items-center">
          <button
            onClick={openModal}
            className="text-xs font-bold text-gold hover:text-gold-light flex items-center gap-1 uppercase tracking-wider transition-colors"
          >
            View Intel <ChevronRight size={14} />
          </button>

          {/* Abort Button (only show if user is creator and heist is active) */}
          {isCreator && heist.status === 'Active' && (
            <button
              onClick={handleAbort}
              className="text-[10px] font-bold text-rose-500/70 hover:text-rose-500 uppercase tracking-widest transition-colors"
            >
              Abort
            </button>
          )}
        </div>
      </div>

      {/* Details Modal */}
      <HeistDetailsModal
        heist={heist}
        isOpen={isModalOpen}
        onClose={closeModal}
        onAbort={onAbort}
        currentUsername={currentUsername}
      />
    </>
  );
};

// InfoRow sub-component
const InfoRow = ({ icon, label, value, highlight = false }) => (
  <div className="flex items-center justify-between text-xs">
    <div className="flex items-center gap-2 text-slate-500 uppercase tracking-wider font-semibold">
      {icon} {label}
    </div>
    <div className={`font-mono ${highlight ? 'text-rose-500 font-bold' : 'text-slate-300'}`}>
      {value}
    </div>
  </div>
);

export default HeistCard;
