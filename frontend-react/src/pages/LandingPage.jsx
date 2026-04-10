import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, User, Lock, ChevronRight, AlertCircle, CheckCircle } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const LandingPage = () => {
  const navigate = useNavigate();
  const { login, register } = useAuth();

  const [isRegistering, setIsRegistering] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Form state
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear errors when user starts typing
    setError('');
    setSuccess('');
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validation
    if (!formData.username || !formData.password) {
      setError('Enter both codename and encryption key.');
      setLoading(false);
      return;
    }

    // Call login service
    const result = await login(formData.username, formData.password);

    if (result.success) {
      // Redirect to dashboard
      navigate('/war-room');
    } else {
      setError(result.error || 'Authentication failed. Invalid credentials.');
    }

    setLoading(false);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    // Validation
    if (!formData.username || !formData.password || !formData.confirmPassword) {
      setError('Fill all fields to register.');
      setLoading(false);
      return;
    }

    if (formData.password.length < 8) {
      setError('Encryption key must be at least 8 characters.');
      setLoading(false);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Encryption keys do not match.');
      setLoading(false);
      return;
    }

    // Call register service
    const result = await register(formData.username, formData.password);

    if (result.success) {
      setSuccess('Account created! You can now authenticate.');
      // Clear form
      setFormData({
        username: '',
        password: '',
        confirmPassword: '',
      });
      // Switch to login after 2 seconds
      setTimeout(() => {
        setIsRegistering(false);
        setSuccess('');
      }, 2000);
    } else {
      setError(result.error || 'Registration failed.');
    }

    setLoading(false);
  };

  const toggleMode = () => {
    setIsRegistering(!isRegistering);
    setError('');
    setSuccess('');
    setFormData({
      username: '',
      password: '',
      confirmPassword: '',
    });
  };

  return (
    <div className="min-h-screen bg-dark-bg text-slate-200 flex flex-col items-center justify-center p-6 relative overflow-hidden">
      {/* Background Decorative Elements */}
      <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-gold/5 blur-[120px] rounded-full"></div>
      <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-500/5 blur-[120px] rounded-full"></div>

      <div className="max-w-md w-full z-10">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-block bg-gold p-4 rounded-3xl mb-6 shadow-[0_0_30px_rgba(245,158,11,0.2)]">
            <Shield className="text-black size-12" />
          </div>
          <h1 className="text-4xl font-black text-white tracking-tighter mb-2 italic">
            POCKET HEIST
          </h1>
          <p className="text-slate-500 font-medium">
            Gamified Office Missions. Tiny Mischief, Big Impact.
          </p>
        </div>

        {/* Login/Register Card */}
        <div className="bg-dark-card border border-slate-800 rounded-3xl p-8 shadow-2xl">
          {/* Form */}
          <form onSubmit={isRegistering ? handleRegister : handleLogin} className="space-y-6">
            {/* Username Field */}
            <div className="space-y-2">
              <label className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">
                Operative Codename
              </label>
              <div className="relative">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600" size={18} />
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  className="w-full bg-slate-900/50 border border-slate-800 rounded-2xl pl-12 pr-4 py-4 text-white focus:outline-none focus:border-gold/50 transition-all placeholder:text-slate-700"
                  placeholder="Agent_Viper"
                />
              </div>
            </div>

            {/* Password Field */}
            <div className="space-y-2">
              <label className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">
                {isRegistering ? 'Set Encryption Key (min 8 characters)' : 'Access Credentials'}
              </label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600" size={18} />
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="w-full bg-slate-900/50 border border-slate-800 rounded-2xl pl-12 pr-4 py-4 text-white focus:outline-none focus:border-gold/50 transition-all placeholder:text-slate-700"
                  placeholder="••••••••"
                />
              </div>
            </div>

            {/* Confirm Password Field (Register Only) */}
            {isRegistering && (
              <div className="space-y-2">
                <label className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">
                  Confirm Encryption Key
                </label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600" size={18} />
                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                    className="w-full bg-slate-900/50 border border-slate-800 rounded-2xl pl-12 pr-4 py-4 text-white focus:outline-none focus:border-gold/50 transition-all placeholder:text-slate-700"
                    placeholder="••••••••"
                  />
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 flex items-center gap-2 text-rose-500 text-sm">
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}

            {/* Success Message */}
            {success && (
              <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-3 flex items-center gap-2 text-green-500 text-sm">
                <CheckCircle size={16} />
                <span>{success}</span>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-white text-black font-black py-4 rounded-2xl hover:bg-gold transition-all uppercase tracking-widest text-sm flex items-center justify-center gap-2 group disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                'Processing...'
              ) : isRegistering ? (
                'Register'
              ) : (
                <>
                  Establish Connection
                  <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </form>

          {/* Toggle Mode */}
          <div className="mt-8 pt-8 border-t border-slate-800 text-center">
            <button
              onClick={toggleMode}
              className="text-xs font-bold text-slate-500 hover:text-white transition-colors uppercase tracking-widest"
            >
              {isRegistering ? 'Back to Login' : 'Apply for New Credentials'}
            </button>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center mt-12 text-[10px] text-slate-700 uppercase tracking-[0.3em] font-bold">
          Secure Line Established • End-to-End Encrypted
        </p>
      </div>
    </div>
  );
};

export default LandingPage;
