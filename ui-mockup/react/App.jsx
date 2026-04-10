import {
    ChevronRight,
    Clock,
    Filter,
    Lock,
    LogOut,
    Map,
    PlusSquare,
    Search,
    Shield,
    Skull,
    Terminal,
    User,
    Zap
} from 'lucide-react';
import { useState } from 'react';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [user, setUser] = useState(null);

  // Mock Heist Data
  const [heists, setHeists] = useState([
    { 
      id: 1, 
      title: "The Decoy Doughnut", 
      target: "Marketing Floor", 
      difficulty: "Low", 
      agent: "Specter", 
      deadline: "2h 15m", 
      status: "Active",
      description: "Place a box of 'free' doughnuts in the kitchen, but hide a cryptic note under the lid."
    },
    { 
      id: 2, 
      title: "Project Sticky Note", 
      target: "CEO Suite", 
      difficulty: "Extreme", 
      agent: "Viper", 
      deadline: "45m", 
      status: "Active",
      description: "Cover the bottom of the CEO's mouse with a sticky note saying 'You've been ghosted'."
    },
    { 
      id: 3, 
      title: "The Printer Loop", 
      target: "HR Dept", 
      difficulty: "Medium", 
      agent: "Ghost", 
      deadline: "EXPIRED", 
      status: "Expired",
      description: "Print 50 pages of pure black ink to deplete the tray before the quarterly review."
    },
    { 
      id: 4, 
      title: "The Chair Swap", 
      target: "IT Workspace", 
      difficulty: "Hard", 
      agent: "Phantom", 
      deadline: "COMPLETED", 
      status: "Completed",
      description: "Swap the developer chairs with the ancient ones from the storage room."
    }
  ]);

  const login = (e) => {
    e.preventDefault();
    setIsAuthenticated(true);
    setUser({ name: 'Agent Smith', rank: 'Master Architect' });
  };

  if (!isAuthenticated) {
    return <LandingPage onLogin={login} />;
  }

  return (
    <div className="flex h-screen bg-[#0a0a0c] text-slate-200 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-[#111114] border-r border-slate-800 flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <div className="bg-amber-500 p-2 rounded-lg">
            <Shield className="text-black size-6" />
          </div>
          <h1 className="font-bold text-xl tracking-tighter text-white">POCKET HEIST</h1>
        </div>

        <nav className="flex-1 px-4 py-6 space-y-2">
          <NavItem 
            icon={<Map size={18} />} 
            label="War Room" 
            active={activeTab === 'dashboard'} 
            onClick={() => setActiveTab('dashboard')} 
          />
          <NavItem 
            icon={<Zap size={18} />} 
            label="My Assignments" 
            active={activeTab === 'assigned'} 
            onClick={() => setActiveTab('assigned')} 
          />
          <NavItem 
            icon={<PlusSquare size={18} />} 
            label="Blueprint Studio" 
            active={activeTab === 'create'} 
            onClick={() => setActiveTab('create')} 
          />
          <NavItem 
            icon={<Clock size={18} />} 
            label="Intel Archive" 
            active={activeTab === 'archive'} 
            onClick={() => setActiveTab('archive')} 
          />
        </nav>

        <div className="p-4 border-t border-slate-800">
          <div className="flex items-center gap-3 p-3 mb-4 rounded-xl bg-slate-900/50">
            <div className="w-10 h-10 rounded-full bg-amber-500/20 flex items-center justify-center text-amber-500 border border-amber-500/30">
              <User size={20} />
            </div>
            <div className="overflow-hidden">
              <p className="text-sm font-bold truncate text-white">{user?.name}</p>
              <p className="text-[10px] text-slate-500 uppercase tracking-widest">{user?.rank}</p>
            </div>
          </div>
          <button 
            onClick={() => setIsAuthenticated(false)}
            className="w-full flex items-center gap-2 text-slate-500 hover:text-rose-400 transition-colors p-2 text-sm"
          >
            <LogOut size={16} /> Logout System
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-slate-900/20 via-[#0a0a0c] to-[#0a0a0c]">
        <header className="px-8 py-6 border-b border-slate-800 flex justify-between items-center sticky top-0 bg-[#0a0a0c]/80 backdrop-blur-md z-10">
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              {activeTab === 'dashboard' && 'Global Operations'}
              {activeTab === 'assigned' && 'Personal Directive'}
              {activeTab === 'create' && 'New Mission Blueprint'}
              {activeTab === 'archive' && 'Historical Records'}
            </h2>
            <p className="text-slate-500 text-sm">Status: High Alert. All units deployed.</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
              <input 
                type="text" 
                placeholder="Search intel..." 
                className="bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-amber-500/50 transition-all w-64"
              />
            </div>
            <button className="p-2 bg-slate-900 border border-slate-800 rounded-lg hover:border-slate-700">
              <Filter size={18} />
            </button>
          </div>
        </header>

        <div className="p-8">
          {activeTab === 'dashboard' && <HeistGrid heists={heists.filter(h => h.status === 'Active')} />}
          {activeTab === 'assigned' && <HeistGrid heists={heists.filter(h => h.agent === 'Specter')} />}
          {activeTab === 'create' && <CreateHeistForm onAdd={(h) => setHeists([h, ...heists])} />}
          {activeTab === 'archive' && <HeistGrid heists={heists.filter(h => h.status !== 'Active')} />}
        </div>
      </main>
    </div>
  );
};

const NavItem = ({ icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all group
      ${active 
        ? 'bg-amber-500 text-black shadow-[0_0_15px_rgba(245,158,11,0.3)]' 
        : 'text-slate-400 hover:bg-slate-800 hover:text-white'}
    `}
  >
    <span className={active ? 'text-black' : 'text-slate-500 group-hover:text-amber-500 transition-colors'}>
      {icon}
    </span>
    {label}
  </button>
);

const HeistGrid = ({ heists }) => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {heists.map(heist => (
      <div key={heist.id} className="bg-[#111114] border border-slate-800 rounded-2xl overflow-hidden hover:border-amber-500/40 transition-all group relative">
        <div className="p-6">
          <div className="flex justify-between items-start mb-4">
            <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-1 rounded bg-slate-900 border ${
              heist.status === 'Active' ? 'text-green-500 border-green-500/20' : 
              heist.status === 'Completed' ? 'text-blue-500 border-blue-500/20' : 'text-rose-500 border-rose-500/20'
            }`}>
              {heist.status}
            </span>
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">#{heist.id.toString().padStart(4, '0')}</span>
          </div>
          
          <h3 className="text-xl font-bold text-white mb-2 group-hover:text-amber-500 transition-colors">{heist.title}</h3>
          <p className="text-slate-400 text-sm mb-6 line-clamp-2">{heist.description}</p>
          
          <div className="space-y-3">
            <InfoRow icon={<Terminal size={14} />} label="Target" value={heist.target} />
            <InfoRow icon={<Skull size={14} />} label="Difficulty" value={heist.difficulty} highlight={heist.difficulty === 'Extreme'} />
            <InfoRow icon={<User size={14} />} label="Operative" value={heist.agent} />
            <InfoRow icon={<Clock size={14} />} label="Time Remaining" value={heist.deadline} />
          </div>
        </div>
        
        <div className="bg-slate-900/50 p-4 border-t border-slate-800 flex justify-between items-center">
          <button className="text-xs font-bold text-amber-500 hover:text-amber-400 flex items-center gap-1 uppercase tracking-wider">
            View Intel <ChevronRight size={14} />
          </button>
          {heist.status === 'Active' && (
            <button className="text-[10px] font-bold text-rose-500/70 hover:text-rose-500 uppercase tracking-widest">
              Abort
            </button>
          )}
        </div>
      </div>
    ))}
  </div>
);

const InfoRow = ({ icon, label, value, highlight }) => (
  <div className="flex items-center justify-between text-xs">
    <div className="flex items-center gap-2 text-slate-500 uppercase tracking-wider font-semibold">
      {icon} {label}
    </div>
    <div className={`font-mono ${highlight ? 'text-rose-500 font-bold' : 'text-slate-300'}`}>{value}</div>
  </div>
);

const CreateHeistForm = ({ onAdd }) => {
  const [formData, setFormData] = useState({
    title: '',
    target: '',
    difficulty: 'Medium',
    agent: '',
    description: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd({
      ...formData,
      id: Math.floor(Math.random() * 10000),
      status: 'Active',
      deadline: '24h 00m'
    });
    alert('Mission Dispatched to Agent!');
  };

  return (
    <div className="max-w-2xl bg-[#111114] border border-slate-800 rounded-2xl p-8 shadow-2xl">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-amber-500 rounded-xl">
          <PlusSquare className="text-black" size={24} />
        </div>
        <div>
          <h3 className="text-xl font-bold text-white">Create Mission Blueprint</h3>
          <p className="text-slate-500 text-sm">Fill in the operative details carefully.</p>
        </div>
      </div>

      <form className="space-y-6" onSubmit={handleSubmit}>
        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Mission Name</label>
            <input 
              type="text" 
              value={formData.title}
              onChange={e => setFormData({...formData, title: e.target.value})}
              placeholder="e.g. Operation Desk-Swap"
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-amber-500/50"
            />
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Target Sector</label>
            <input 
              type="text" 
              value={formData.target}
              onChange={e => setFormData({...formData, target: e.target.value})}
              placeholder="e.g. Kitchen Pantry"
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-amber-500/50"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Difficulty</label>
            <select 
              value={formData.difficulty}
              onChange={e => setFormData({...formData, difficulty: e.target.value})}
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-amber-500/50"
            >
              <option>Low</option>
              <option>Medium</option>
              <option>Hard</option>
              <option>Extreme</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Assign Operative</label>
            <input 
              type="text" 
              value={formData.agent}
              onChange={e => setFormData({...formData, agent: e.target.value})}
              placeholder="Agent Codename"
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-amber-500/50"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Intel Briefing</label>
          <textarea 
            value={formData.description}
            onChange={e => setFormData({...formData, description: e.target.value})}
            placeholder="Detailed mission parameters..."
            className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 text-white h-32 focus:outline-none focus:border-amber-500/50 resize-none"
          />
        </div>

        <button className="w-full bg-amber-500 hover:bg-amber-400 text-black font-black py-4 rounded-xl transition-all shadow-[0_0_20px_rgba(245,158,11,0.2)] flex items-center justify-center gap-2 uppercase tracking-tighter">
          <Zap size={20} /> Initialize Operation
        </button>
      </form>
    </div>
  );
};

const LandingPage = ({ onLogin }) => (
  <div className="min-h-screen bg-[#0a0a0c] text-slate-200 flex flex-col items-center justify-center p-6 relative overflow-hidden">
    {/* Background Decorative Elements */}
    <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-amber-500/5 blur-[120px] rounded-full"></div>
    <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-500/5 blur-[120px] rounded-full"></div>
    
    <div className="max-w-md w-full z-10">
      <div className="text-center mb-12">
        <div className="inline-block bg-amber-500 p-4 rounded-3xl mb-6 shadow-[0_0_30px_rgba(245,158,11,0.2)]">
          <Shield className="text-black size-12" />
        </div>
        <h1 className="text-4xl font-black text-white tracking-tighter mb-2 italic">POCKET HEIST</h1>
        <p className="text-slate-500 font-medium">Gamified Office Missions. Tiny Mischief, Big Impact.</p>
      </div>

      <div className="bg-[#111114] border border-slate-800 rounded-3xl p-8 shadow-2xl">
        <form className="space-y-6" onSubmit={onLogin}>
          <div className="space-y-2">
            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">Operative Codename</label>
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600" size={18} />
              <input 
                type="text" 
                required
                className="w-full bg-slate-900/50 border border-slate-800 rounded-2xl pl-12 pr-4 py-4 text-white focus:outline-none focus:border-amber-500/50 transition-all placeholder:text-slate-700"
                placeholder="Agent_Viper"
              />
            </div>
          </div>
          
          <div className="space-y-2">
            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">Access Credentials</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600" size={18} />
              <input 
                type="password" 
                required
                className="w-full bg-slate-900/50 border border-slate-800 rounded-2xl pl-12 pr-4 py-4 text-white focus:outline-none focus:border-amber-500/50 transition-all placeholder:text-slate-700"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button className="w-full bg-white text-black font-black py-4 rounded-2xl hover:bg-amber-500 transition-all uppercase tracking-widest text-sm flex items-center justify-center gap-2 group">
            Establish Connection <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
          </button>
        </form>
        
        <div className="mt-8 pt-8 border-t border-slate-800 text-center">
          <button className="text-xs font-bold text-slate-500 hover:text-white transition-colors uppercase tracking-widest">
            Apply for New Credentials
          </button>
        </div>
      </div>

      <p className="text-center mt-12 text-[10px] text-slate-700 uppercase tracking-[0.3em] font-bold">
        Secure Line Established • End-to-End Encrypted
      </p>
    </div>
  </div>
);

export default App;