import { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { Shield, Map, Zap, PlusSquare, Clock, LogOut, Search, Filter } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState('');

  const navItems = [
    { path: '/war-room', icon: Map, label: 'War Room', title: 'Global Operations', subtitle: 'Status: High Alert. All units deployed.' },
    { path: '/my-assignments', icon: Zap, label: 'My Assignments', title: 'Personal Directive', subtitle: 'Missions under your command.' },
    { path: '/create', icon: PlusSquare, label: 'Blueprint Studio', title: 'New Mission Blueprint', subtitle: 'Design and launch a new operation.' },
    { path: '/archive', icon: Clock, label: 'Intel Archive', title: 'Historical Records', subtitle: 'Completed and aborted missions.' },
  ];

  const isActive = (path) => location.pathname === path;

  // Get current page info
  const currentPage = navItems.find(item => isActive(item.path)) || navItems[0];

  return (
    <div className="flex h-screen bg-dark-bg text-slate-200">
      {/* Sidebar */}
      <aside className="w-64 bg-dark-card border-r border-slate-800 flex flex-col">
        {/* Branding */}
        <div className="p-6 flex items-center gap-3">
          <div className="bg-gold p-2 rounded-lg">
            <Shield className="text-black size-6" />
          </div>
          <h1 className="font-bold text-xl tracking-tighter text-white">
            POCKET HEIST
          </h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all group ${
                  active
                    ? 'bg-gold text-black shadow-[0_0_15px_rgba(245,158,11,0.3)]'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon
                  size={18}
                  className={active ? 'text-black' : 'text-slate-500 group-hover:text-gold transition-colors'}
                />
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* User Profile */}
        <div className="p-4 border-t border-slate-800">
          <div className="flex items-center gap-3 p-3 mb-4 rounded-xl bg-slate-900/50">
            <div className="w-10 h-10 rounded-full bg-gold/20 flex items-center justify-center text-gold border border-gold/30">
              <span className="font-bold">{user?.username?.[0]?.toUpperCase() || 'A'}</span>
            </div>
            <div className="overflow-hidden flex-1">
              <p className="text-sm font-bold truncate text-white">
                {user?.username || 'Agent'}
              </p>
              <p className="text-[10px] text-slate-500 uppercase tracking-widest">
                Operative
              </p>
            </div>
          </div>

          {/* Logout Button */}
          <button
            onClick={logout}
            className="w-full flex items-center gap-2 text-slate-500 hover:text-rose-400 transition-colors p-2 text-sm"
          >
            <LogOut size={16} /> Logout System
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-slate-900/20 via-dark-bg to-dark-bg">
        {/* Header */}
        <header className="px-8 py-6 border-b border-slate-800 flex justify-between items-center sticky top-0 bg-dark-bg/80 backdrop-blur-md z-10">
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              {currentPage.title}
            </h2>
            <p className="text-slate-500 text-sm">
              {currentPage.subtitle}
            </p>
          </div>
          <div className="flex items-center gap-4">
            {/* Search Bar */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
              <input
                type="text"
                placeholder="Search intel..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-slate-900 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-gold/50 transition-all w-64 text-white placeholder:text-slate-600"
              />
            </div>
            {/* Filter Button */}
            <button className="p-2 bg-slate-900 border border-slate-800 rounded-lg hover:border-slate-700 transition-colors">
              <Filter size={18} />
            </button>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-8">
          <Outlet context={{ searchQuery }} />
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
