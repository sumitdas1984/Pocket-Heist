import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PlusSquare, Zap } from 'lucide-react';
import { createHeist } from '../services/heists';
import { useToast } from '../contexts/ToastContext';

const BlueprintStudio = () => {
  const navigate = useNavigate();
  const toast = useToast();

  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    title: '',
    target: '',
    difficulty: 'Medium',
    assignee_username: '',
    description: '',
  });

  // Auto-set deadline to +3 hours from now
  const getDeadline = () => {
    const deadline = new Date();
    deadline.setHours(deadline.getHours() + 3);
    return deadline.toISOString();
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Validation
    if (!formData.title || !formData.target || !formData.assignee_username) {
      toast.error('Blueprint incomplete. Fill all required fields.');
      setLoading(false);
      return;
    }

    // Prepare heist data
    const heistData = {
      title: formData.title,
      target: formData.target,
      difficulty: formData.difficulty,
      assignee_username: formData.assignee_username,
      deadline: getDeadline(),
      description: formData.description || null,
    };

    // Call create heist service
    const result = await createHeist(heistData);

    if (result.success) {
      toast.success(`Mission launched: ${result.data.title}`);

      // Clear form
      setFormData({
        title: '',
        target: '',
        difficulty: 'Medium',
        assignee_username: '',
        description: '',
      });

      // Redirect to War Room after 2 seconds
      setTimeout(() => {
        navigate('/war-room');
      }, 2000);
    } else {
      toast.error(result.error || 'Failed to create heist');
    }

    setLoading(false);
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-dark-card border border-slate-800 rounded-2xl p-8 shadow-2xl">
        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <div className="p-3 bg-gold rounded-xl">
            <PlusSquare className="text-black" size={24} />
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">Create Mission Blueprint</h3>
            <p className="text-slate-500 text-sm">Fill in the operative details carefully.</p>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Row 1: Mission Name + Target */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Mission Name */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                Mission Name *
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="e.g. Operation Desk-Swap"
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-gold/50 placeholder:text-slate-600 transition-all"
                required
              />
            </div>

            {/* Target Sector */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                Target Sector *
              </label>
              <input
                type="text"
                name="target"
                value={formData.target}
                onChange={handleChange}
                placeholder="e.g. Kitchen Pantry"
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-gold/50 placeholder:text-slate-600 transition-all"
                required
              />
            </div>
          </div>

          {/* Row 2: Difficulty + Assign Operative */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Difficulty */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                Difficulty *
              </label>
              <select
                name="difficulty"
                value={formData.difficulty}
                onChange={handleChange}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-gold/50 transition-all"
                required
              >
                <option value="Training">Training</option>
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
                <option value="Legendary">Legendary</option>
              </select>
            </div>

            {/* Assign Operative */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                Assign Operative *
              </label>
              <input
                type="text"
                name="assignee_username"
                value={formData.assignee_username}
                onChange={handleChange}
                placeholder="Agent Codename"
                className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-gold/50 placeholder:text-slate-600 transition-all"
                required
              />
            </div>
          </div>

          {/* Intel Briefing */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">
              Intel Briefing
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Detailed mission parameters..."
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white h-32 focus:outline-none focus:border-gold/50 resize-none placeholder:text-slate-600 transition-all"
            />
          </div>

          {/* Deadline Info */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-400">
              <span className="text-gold font-semibold">Auto-Deadline:</span> Mission will expire in 3 hours from creation.
            </p>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gold hover:bg-gold-light text-black font-black py-4 rounded-xl transition-all shadow-[0_0_20px_rgba(245,158,11,0.2)] flex items-center justify-center gap-2 uppercase tracking-tighter disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              'Initializing...'
            ) : (
              <>
                <Zap size={20} /> Initialize Operation
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default BlueprintStudio;
