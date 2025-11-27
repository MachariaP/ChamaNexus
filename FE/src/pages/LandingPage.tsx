import { motion } from 'framer-motion';
import { 
  Users, 
  TrendingUp, 
  Shield, 
  Zap, 
  PiggyBank, 
  BarChart3, 
  Vote, 
  ArrowRight,
  Star,
  Calendar,
  Crown,
  Rocket,
  HeartHandshake,
  Coins,
  Building,
  Clock,
  Sparkles,
  PlayCircle,
  LogIn,
  FileText,
  Target,
  PieChart,
  Menu,
  X
} from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import { useEffect, useState } from 'react';

export function LandingPage() {
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Close mobile menu when route changes
    return () => setIsMobileMenuOpen(false);
  }, []);

  const features = [
    {
      icon: Users,
      title: 'Smart Member Management',
      description: 'Easily track members, roles, attendance, and communication within your chama with intuitive tools.',
      gradient: 'from-blue-500 to-cyan-500',
      delay: 0.1
    },
    {
      icon: PiggyBank,
      title: 'Contribution Tracking',
      description: 'Record all savings contributions, track individual balances, and generate detailed contribution reports.',
      gradient: 'from-green-500 to-emerald-500',
      delay: 0.2
    },
    {
      icon: TrendingUp,
      title: 'Investment Insights',
      description: 'Monitor investment performance and get smart analytics on your chama portfolio growth.',
      gradient: 'from-purple-500 to-pink-500',
      delay: 0.3
    },
    {
      icon: BarChart3,
      title: 'Financial Analytics',
      description: 'Make data-driven decisions with comprehensive financial reports and visual dashboards.',
      gradient: 'from-orange-500 to-amber-500',
      delay: 0.4
    },
    {
      icon: Vote,
      title: 'Meeting Management',
      description: 'Schedule meetings, track attendance, and record collective decisions with our secure system.',
      gradient: 'from-indigo-500 to-blue-500',
      delay: 0.5
    },
    {
      icon: Shield,
      title: 'Secure Record-Keeping',
      description: 'Your chama data is protected with enterprise-level security and regular automated backups.',
      gradient: 'from-teal-500 to-cyan-500',
      delay: 0.6
    }
  ];

  const benefits = [
    { icon: Coins, text: 'Automated contribution tracking', color: 'text-green-500' },
    { icon: Building, text: 'Investment performance monitoring', color: 'text-blue-500' },
    { icon: Calendar, text: 'Meeting scheduling & reminders', color: 'text-purple-500' },
    { icon: BarChart3, text: 'Financial health dashboards', color: 'text-orange-500' },
    { icon: Clock, text: 'Mobile-first design', color: 'text-pink-500' },
    { icon: FileText, text: 'Customizable reports', color: 'text-indigo-500' },
    { icon: Users, text: 'Member activity tracking', color: 'text-teal-500' },
    { icon: Shield, text: 'Data security & privacy', color: 'text-amber-500' }
  ];

  const stats = [
    { value: '500+', label: 'Active Chamas', icon: Users, color: 'text-blue-500' },
    { value: 'KSh 50M+', label: 'Assets Tracked', icon: Coins, color: 'text-green-500' },
    { value: '98%', label: 'Satisfaction Rate', icon: Star, color: 'text-yellow-500' },
    { value: '24/7', label: 'Support Available', icon: Clock, color: 'text-purple-500' }
  ];

  const testimonials = [
    {
      name: 'Sarah Mwangi',
      role: 'Treasurer, Umoja Women Group',
      content: 'ChamaNexus transformed our record-keeping. We have complete transparency and our members trust the system completely!',
      avatar: 'SM'
    },
    {
      name: 'David Ochieng',
      role: 'Chairman, Victory Investors',
      content: 'The analytics and insights helped us make better investment decisions. Our portfolio growth is now data-driven.',
      avatar: 'DO'
    },
    {
      name: 'Grace Wanjiku',
      role: 'Secretary, Smart Savers Chama',
      content: 'From contribution tracking to meeting management, everything is seamless. Our chama has never been more organized.',
      avatar: 'GW'
    }
  ];

  const FloatingElement = ({ children, delay = 0 }: { children: React.ReactNode; delay?: number }) => (
    <motion.div
      initial={{ y: 0 }}
      animate={{ 
        y: [0, -20, 0],
      }}
      transition={{
        duration: 4,
        delay,
        repeat: Infinity,
        ease: "easeInOut"
      }}
      className="absolute"
    >
      {children}
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 font-sans overflow-hidden">
      {/* Animated Background Elements - Hidden on mobile for performance */}
      <div className="hidden sm:block fixed inset-0 overflow-hidden pointer-events-none">
        <FloatingElement delay={0}>
          <div className="absolute top-20 left-10 w-48 h-48 sm:w-72 sm:h-72 bg-gradient-to-r from-blue-200 to-cyan-200 rounded-full blur-3xl opacity-20" />
        </FloatingElement>
        <FloatingElement delay={2}>
          <div className="absolute top-40 right-4 sm:right-20 w-64 h-64 sm:w-96 sm:h-96 bg-gradient-to-r from-purple-200 to-pink-200 rounded-full blur-3xl opacity-20" />
        </FloatingElement>
        <FloatingElement delay={1}>
          <div className="absolute bottom-20 left-4 sm:left-1/4 w-48 h-48 sm:w-64 sm:h-64 bg-gradient-to-r from-green-200 to-emerald-200 rounded-full blur-3xl opacity-20" />
        </FloatingElement>
      </div>

      {/* Navigation */}
      <motion.nav 
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="relative z-50 sticky top-0 bg-white/90 backdrop-blur-xl shadow-lg border-b border-gray-200/50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
          <div className="flex justify-between items-center">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-center gap-2 sm:gap-3 cursor-pointer"
              onClick={() => navigate('/')}
            >
              <motion.div
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity, repeatDelay: 5 }}
                className="w-10 h-10 sm:w-12 sm:h-12 rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg"
              >
                <Crown className="h-5 w-5 sm:h-6 sm:w-6 text-white" />
              </motion.div>
              <div>
                <span className="text-xl sm:text-2xl font-black bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  ChamaNexus
                </span>
                <div className="text-xs text-gray-500 font-medium hidden sm:block">Smart Chama Management</div>
              </div>
            </motion.div>
            
            {/* Desktop Navigation */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="hidden md:flex gap-4 items-center"
            >
              <Link
                to="/login"
                className="px-6 py-2.5 text-gray-700 font-semibold hover:text-blue-600 transition-colors flex items-center gap-2"
              >
                <LogIn className="h-4 w-4" />
                Sign In
              </Link>
              <motion.button
                whileHover={{ 
                  scale: 1.05,
                  boxShadow: "0 20px 40px rgba(99, 102, 241, 0.3)"
                }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/register')}
                className="px-6 sm:px-8 py-2.5 sm:py-3 rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold shadow-xl hover:shadow-2xl transition-all flex items-center gap-2 group text-sm sm:text-base"
              >
                <Rocket className="h-4 w-4 group-hover:scale-110 transition-transform" />
                Start Free Trial
              </motion.button>
            </motion.div>

            {/* Mobile Menu Button */}
            <div className="flex md:hidden items-center gap-2">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/register')}
                className="px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold shadow-lg flex items-center gap-2 group text-sm"
              >
                <Rocket className="h-3 w-3" />
                Start
              </motion.button>
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors"
              >
                {isMobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </button>
            </div>
          </div>

          {/* Mobile Menu */}
          {isMobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden bg-white/95 backdrop-blur-xl border-t border-gray-200 mt-3 py-4"
            >
              <div className="flex flex-col space-y-4 px-2">
                <Link
                  to="/login"
                  className="px-4 py-3 text-gray-700 font-semibold hover:text-blue-600 transition-colors flex items-center gap-3 rounded-lg hover:bg-gray-50"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <LogIn className="h-5 w-5" />
                  Sign In
                </Link>
                <Link
                  to="/demo"
                  className="px-4 py-3 text-gray-700 font-semibold hover:text-blue-600 transition-colors flex items-center gap-3 rounded-lg hover:bg-gray-50"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <PlayCircle className="h-5 w-5" />
                  Watch Demo
                </Link>
              </div>
            </motion.div>
          )}
        </div>
      </motion.nav>

      {/* Hero Section */}
      <div className="relative overflow-hidden pt-10 sm:pt-16 lg:pt-20 pb-16 sm:pb-24 lg:pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center relative z-10"
          >
            {/* Trust Badge */}
            <motion.div
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
              className="inline-flex items-center gap-2 sm:gap-3 px-4 sm:px-6 py-2 sm:py-3 rounded-2xl bg-white/80 backdrop-blur-sm border border-gray-200 shadow-lg mb-8 sm:mb-12 max-w-xs sm:max-w-none mx-auto"
            >
              <div className="flex items-center gap-1 sm:gap-2">
                {[1, 2, 3, 4, 5].map((i) => (
                  <Star key={i} className="h-4 w-4 sm:h-5 sm:w-5 fill-yellow-400 text-yellow-400" />
                ))}
              </div>
              <span className="text-gray-700 font-bold text-sm sm:text-base">Trusted by 500+ Chamas</span>
            </motion.div>

            {/* Main Heading */}
            <motion.h1
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-black mb-6 sm:mb-8 leading-tight"
            >
              <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                Smart Chama
              </span>
              <br />
              <span className="bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl">
                Analytics
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="text-lg sm:text-xl md:text-2xl text-gray-600 mb-8 sm:mb-12 max-w-4xl mx-auto leading-relaxed font-medium px-4 sm:px-0"
            >
              Transform your savings group with intelligent record-keeping,{' '}
              <span className="text-blue-600 font-semibold">data-driven insights</span>, and{' '}
              <span className="text-purple-600 font-semibold">transparent financial tracking</span>.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 sm:gap-6 justify-center items-center mb-12 sm:mb-20 px-4 sm:px-0"
            >
              <motion.button
                whileHover={{ 
                  scale: 1.05,
                  boxShadow: "0 25px 50px -12px rgba(99, 102, 241, 0.4)"
                }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/register')}
                className="group px-8 sm:px-12 py-4 sm:py-5 rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold text-lg sm:text-xl shadow-2xl hover:shadow-3xl transition-all flex items-center justify-center gap-3 w-full sm:w-auto"
              >
                <Sparkles className="h-5 w-5 sm:h-6 sm:w-6 group-hover:scale-110 transition-transform" />
                Start Free Trial
                <ArrowRight className="h-4 w-4 sm:h-5 sm:w-5 group-hover:translate-x-1 transition-transform" />
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/demo')}
                className="group px-8 sm:px-12 py-4 sm:py-5 rounded-2xl border-2 border-gray-300 text-gray-700 font-bold text-lg sm:text-xl hover:border-blue-600 hover:text-blue-600 transition-all flex items-center justify-center gap-3 bg-white/80 backdrop-blur-sm w-full sm:w-auto"
              >
                <PlayCircle className="h-5 w-5 sm:h-6 sm:w-6 group-hover:scale-110 transition-transform" />
                Watch Demo
              </motion.button>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              className="grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-6 lg:gap-8 max-w-5xl mx-auto px-4 sm:px-0"
            >
              {stats.map((stat, index) => {
                const Icon = stat.icon;
                return (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.9 + index * 0.1 }}
                    whileHover={{ y: -5, scale: 1.05 }}
                    className="bg-white/80 backdrop-blur-xl rounded-2xl sm:rounded-3xl p-4 sm:p-6 lg:p-8 shadow-xl sm:shadow-2xl border border-gray-200/50 text-center group"
                  >
                    <div className={`w-12 h-12 sm:w-14 sm:h-14 lg:w-16 lg:h-16 rounded-xl sm:rounded-2xl bg-gradient-to-br ${stat.color.replace('text', 'from')} to-${stat.color.split('-')[1]}-300 flex items-center justify-center mx-auto mb-3 sm:mb-4 group-hover:scale-110 transition-transform shadow-lg`}>
                      <Icon className="h-6 w-6 sm:h-7 sm:w-7 lg:h-8 lg:w-8 text-white" />
                    </div>
                    <div className={`text-2xl sm:text-3xl lg:text-4xl font-black mb-1 sm:mb-2 ${stat.color}`}>
                      {stat.value}
                    </div>
                    <div className="text-gray-600 font-semibold text-xs sm:text-sm">{stat.label}</div>
                  </motion.div>
                );
              })}
            </motion.div>
          </motion.div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="relative py-16 sm:py-24 lg:py-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12 sm:mb-16 lg:mb-20"
          >
            <motion.div
              initial={{ scale: 0 }}
              whileInView={{ scale: 1 }}
              viewport={{ once: true }}
              className="w-16 h-16 sm:w-20 sm:h-20 rounded-3xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center mx-auto mb-4 sm:mb-6 shadow-2xl"
            >
              <PieChart className="h-8 w-8 sm:h-10 sm:w-10 text-white" />
            </motion.div>
            <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black mb-4 sm:mb-6 text-gray-900">
              Everything You Need for <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent block sm:inline">Smart Management</span>
            </h2>
            <p className="text-lg sm:text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto font-medium px-4 sm:px-0">
              Comprehensive record-keeping and analytics tools designed specifically for Kenyan savings groups
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 30, scale: 0.9 }}
                  whileInView={{ opacity: 1, y: 0, scale: 1 }}
                  viewport={{ once: true, amount: 0.3 }}
                  transition={{ delay: feature.delay, duration: 0.6 }}
                  whileHover={{ 
                    y: -5, 
                    scale: 1.02,
                    boxShadow: "0 20px 40px -10px rgba(0, 0, 0, 0.15)"
                  }}
                  className="bg-white/80 backdrop-blur-xl rounded-2xl sm:rounded-3xl p-6 sm:p-8 shadow-lg sm:shadow-xl border border-gray-200/50 group cursor-pointer transform-gpu"
                >
                  <div className={`w-14 h-14 sm:w-16 sm:h-16 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform shadow-lg`}>
                    <Icon className="h-6 w-6 sm:h-8 sm:w-8 text-white" />
                  </div>
                  <h3 className="text-xl sm:text-2xl font-black mb-3 sm:mb-4 text-gray-900 group-hover:bg-gradient-to-r group-hover:from-blue-600 group-hover:to-purple-600 group-hover:bg-clip-text group-hover:text-transparent transition-all">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed text-base sm:text-lg">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="bg-gradient-to-br from-gray-900 to-gray-800 py-16 sm:py-24 lg:py-32 relative overflow-hidden">
        <div className="absolute inset-0 bg-black/50" />
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12 sm:mb-16"
          >
            <HeartHandshake className="h-12 w-12 sm:h-16 sm:w-16 text-yellow-400 mx-auto mb-4 sm:mb-6" />
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-black text-white mb-4">
              Trusted by <span className="text-yellow-400">Chamas</span> Across Kenya
            </h2>
            <p className="text-lg sm:text-xl text-gray-300 max-w-2xl mx-auto px-4 sm:px-0">
              See how ChamaNexus is transforming record-keeping and financial transparency
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                whileHover={{ y: -5 }}
                className="bg-white/10 backdrop-blur-lg rounded-2xl sm:rounded-3xl p-6 sm:p-8 border border-white/20 text-white group"
              >
                <div className="flex items-center gap-3 sm:gap-4 mb-4 sm:mb-6">
                  <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl bg-gradient-to-br from-yellow-400 to-amber-500 flex items-center justify-center font-bold text-gray-900 text-sm sm:text-base">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <h4 className="font-bold text-base sm:text-lg">{testimonial.name}</h4>
                    <p className="text-yellow-200 text-xs sm:text-sm">{testimonial.role}</p>
                  </div>
                </div>
                <p className="text-gray-200 leading-relaxed text-sm sm:text-lg">{testimonial.content}</p>
                <div className="flex gap-1 mt-3 sm:mt-4">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <Star key={star} className="h-4 w-4 sm:h-5 sm:w-5 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="py-16 sm:py-24 lg:py-32 bg-gradient-to-br from-blue-600 to-purple-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-white/5" />
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12 sm:mb-16"
          >
            <Target className="h-12 w-12 sm:h-16 sm:w-16 text-white mx-auto mb-4 sm:mb-6" />
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-black text-white mb-4">
              Built for <span className="text-yellow-300">Modern Chamas</span>
            </h2>
            <p className="text-lg sm:text-xl text-blue-200 max-w-3xl mx-auto font-medium px-4 sm:px-0">
              Features that make record-keeping effortless and insights actionable, right out of the box.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            {benefits.map((benefit, index) => {
              const Icon = benefit.icon;
              return (
                <motion.div
                  key={benefit.text}
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.05, y: -5 }}
                  className="flex items-center gap-3 sm:gap-4 bg-white/10 backdrop-blur-lg rounded-xl sm:rounded-2xl p-4 sm:p-6 text-white hover:bg-white/20 transition-all border border-white/20 group"
                >
                  <Icon className={`h-6 w-6 sm:h-8 sm:w-8 flex-shrink-0 ${benefit.color} group-hover:scale-110 transition-transform`} />
                  <span className="text-sm sm:text-lg font-semibold">{benefit.text}</span>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Final CTA */}
      <div className="pb-16 sm:pb-24 lg:pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-3xl sm:rounded-4xl p-8 sm:p-12 md:p-16 lg:p-20 text-center text-white shadow-2xl relative overflow-hidden ring-4 ring-blue-400/30"
          >
            <div className="absolute inset-0 bg-black/20" />
            <div className="relative z-10">
              <motion.div
                animate={{ 
                  rotate: [0, 5, -5, 0],
                  scale: [1, 1.1, 1]
                }}
                transition={{ 
                  duration: 3,
                  repeat: Infinity,
                  repeatDelay: 2
                }}
                className="w-16 h-16 sm:w-20 sm:h-20 lg:w-24 lg:h-24 rounded-3xl bg-gradient-to-br from-yellow-400 to-amber-500 flex items-center justify-center mx-auto mb-6 sm:mb-8 shadow-2xl"
              >
                <Zap className="h-8 w-8 sm:h-10 sm:w-10 lg:h-12 lg:w-12 text-white" />
              </motion.div>
              
              <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-black mb-4 sm:mb-6 leading-tight">
                Start Your Chama's <span className="text-yellow-300 block sm:inline">Digital Transformation</span> Today
              </h2>
              
              <p className="text-base sm:text-lg md:text-xl lg:text-2xl mb-6 sm:mb-8 lg:mb-10 text-blue-100 max-w-3xl mx-auto font-medium leading-relaxed px-4 sm:px-0">
                Join hundreds of chamas that have transformed their record-keeping 
                and gained valuable insights with unmatched transparency.
              </p>
              
              <motion.button
                whileHover={{ 
                  scale: 1.05,
                  boxShadow: "0 20px 40px rgba(255, 255, 255, 0.2)"
                }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/register')}
                className="px-8 sm:px-12 lg:px-16 py-3 sm:py-4 lg:py-5 rounded-2xl bg-white text-blue-600 font-black text-lg sm:text-xl lg:text-2xl shadow-2xl hover:shadow-3xl transition-all inline-flex items-center gap-3 sm:gap-4 mb-4 sm:mb-6 w-full sm:w-auto justify-center"
              >
                <Crown className="h-5 w-5 sm:h-6 sm:w-6" />
                Create Your Chama Hub
                <ArrowRight className="h-5 w-5 sm:h-6 sm:w-6" />
              </motion.button>
              
              <p className="text-blue-200 text-sm sm:text-base lg:text-lg font-medium">
                No credit card required • 14-day free trial • Setup in minutes
              </p>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Enhanced Footer */}
      <footer className="border-t border-gray-200 bg-white/80 backdrop-blur-xl py-8 sm:py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row justify-between items-center gap-6 sm:gap-8">
            <div className="flex flex-col items-center lg:items-start gap-3 sm:gap-4 text-center lg:text-left">
              <div className="flex items-center gap-2 sm:gap-3">
                <motion.div
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.6 }}
                  className="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center"
                >
                  <Crown className="h-4 w-4 sm:h-5 sm:w-5 text-white" />
                </motion.div>
                <div>
                  <span className="text-lg sm:text-xl font-black text-gray-900">ChamaNexus</span>
                  <div className="text-xs text-gray-500 font-medium">Smart Chama Management</div>
                </div>
              </div>
              <p className="text-gray-600 max-w-md text-sm sm:text-base">
                Empowering African communities through transparent record-keeping and data-driven insights.
              </p>
            </div>
            
            <div className="flex flex-wrap justify-center gap-4 sm:gap-6">
              {['Privacy', 'Terms', 'Support', 'Contact'].map((item) => (
                <motion.a
                  key={item}
                  whileHover={{ y: -2, color: '#4f46e5' }}
                  className="text-gray-600 hover:text-blue-600 font-medium cursor-pointer transition-colors text-sm sm:text-base"
                >
                  {item}
                </motion.a>
              ))}
            </div>
          </div>
          
          <div className="border-t border-gray-200 mt-6 sm:mt-8 pt-6 sm:pt-8 text-center">
            <p className="text-gray-500 text-xs sm:text-sm">
              &copy; 2024 ChamaNexus. Empowering communities across Africa. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;
