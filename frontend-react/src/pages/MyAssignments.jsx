import { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { listMyHeists, abortHeist } from '../services/heists';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../contexts/ToastContext';
import HeistGrid from '../components/HeistGrid';
import HeistCardSkeleton from '../components/HeistCardSkeleton';

const MyAssignments = () => {
  const { searchQuery } = useOutletContext();
  const { user } = useAuth();
  const toast = useToast();

  const [heists, setHeists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filterStatus, setFilterStatus] = useState('All');

  // Fetch user's heists on mount
  useEffect(() => {
    fetchHeists();
  }, []);

  const fetchHeists = async () => {
    setLoading(true);
    setError('');

    const result = await listMyHeists();

    if (result.success) {
      setHeists(result.data);
    } else {
      setError(result.error || 'Failed to fetch your heists');
    }

    setLoading(false);
  };

  // Handle abort heist
  const handleAbort = async (heistId) => {
    const result = await abortHeist(heistId);

    if (result.success) {
      toast.success('Mission aborted successfully');
      fetchHeists();
    } else {
      toast.error(result.error || 'Failed to abort heist');
    }
  };

  // Filter heists based on search query and status filter
  const filteredHeists = heists.filter((heist) => {
    // Status filter
    if (filterStatus !== 'All' && heist.status !== filterStatus) {
      return false;
    }

    // Search filter
    if (!searchQuery) return true;

    const query = searchQuery.toLowerCase();
    return (
      heist.title.toLowerCase().includes(query) ||
      heist.target.toLowerCase().includes(query) ||
      heist.assignee_username.toLowerCase().includes(query) ||
      heist.difficulty.toLowerCase().includes(query) ||
      (heist.description && heist.description.toLowerCase().includes(query))
    );
  });

  // Count heists by status
  const statusCounts = {
    All: heists.length,
    Active: heists.filter(h => h.status === 'Active').length,
    Expired: heists.filter(h => h.status === 'Expired').length,
    Aborted: heists.filter(h => h.status === 'Aborted').length,
  };

  // Loading state
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <HeistCardSkeleton key={i} />
        ))}
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-4">⚠️</div>
        <p className="text-rose-500 text-lg mb-4">{error}</p>
        <button
          onClick={fetchHeists}
          className="bg-gold hover:bg-gold-light text-black font-bold py-2 px-6 rounded-xl transition-all"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Status Filter Tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto">
        {['All', 'Active', 'Expired', 'Aborted'].map((status) => (
          <button
            key={status}
            onClick={() => setFilterStatus(status)}
            className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all whitespace-nowrap ${
              filterStatus === status
                ? 'bg-gold text-black shadow-[0_0_15px_rgba(245,158,11,0.3)]'
                : 'bg-slate-900 text-slate-400 border border-slate-800 hover:border-slate-700'
            }`}
          >
            {status}
            <span className={`ml-2 text-xs ${filterStatus === status ? 'text-black/70' : 'text-slate-600'}`}>
              ({statusCounts[status]})
            </span>
          </button>
        ))}
      </div>

      {/* Search indicator */}
      {searchQuery && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-3 mb-6 text-sm text-slate-400">
          <span className="text-gold font-semibold">Searching:</span> "{searchQuery}"
          <span className="ml-2 text-slate-500">
            ({filteredHeists.length} {filteredHeists.length === 1 ? 'result' : 'results'})
          </span>
        </div>
      )}

      {/* Heists Grid */}
      <HeistGrid
        heists={filteredHeists}
        onAbort={handleAbort}
        currentUsername={user?.username}
        emptyMessage={
          searchQuery
            ? `No heists found matching "${searchQuery}".`
            : filterStatus === 'All'
            ? "📭 You haven't created any heists yet. Head to Blueprint Studio!"
            : `📭 No ${filterStatus.toLowerCase()} heists.`
        }
      />
    </div>
  );
};

export default MyAssignments;
