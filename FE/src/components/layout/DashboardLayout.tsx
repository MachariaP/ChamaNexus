import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard,
  Users,
  Wallet,
  TrendingUp,
  PiggyBank,
  FileText,
  Vote,
  CheckSquare,
  BarChart3,
  FileBarChart,
  Shield,
  MessageSquare,
  Calendar,
  FolderOpen,
  Settings,
  UserCircle,
  LogOut,
  Menu,
  X,
  ChevronDown,
  DollarSign,
  CreditCard,
  Receipt,
  Coins,
  Smartphone,
  LineChart,
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import type { User } from '../../types';

interface NavItem {
  name: string;
  path: string;
  icon: React.ElementType;
  adminOnly?: boolean;
}

interface NavSection {
  title: string;
  items: NavItem[];
  adminOnly?: boolean;
}

const navigationSections: NavSection[] = [
  {
    title: 'Overview',
    items: [
      { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
      { name: 'Analytics', path: '/dashboard/analytics', icon: BarChart3 },
    ],
  },
  {
    title: 'Groups',
    items: [
      { name: 'My Groups', path: '/dashboard/groups', icon: Users },
      { name: 'Create Group', path: '/dashboard/groups/create', icon: Users },
    ],
  },
  {
    title: 'Finance',
    items: [
      { name: 'Finance Hub', path: '/dashboard/finance', icon: Wallet },
      { name: 'Contributions', path: '/dashboard/contributions', icon: DollarSign },
      { name: 'Transactions', path: '/dashboard/transactions', icon: Receipt },
      { name: 'Expenses', path: '/dashboard/expenses', icon: CreditCard },
      { name: 'Statements', path: '/dashboard/statements', icon: FileText },
    ],
  },
  {
    title: 'Loans & Investments',
    items: [
      { name: 'Loans', path: '/dashboard/loans', icon: Coins },
      { name: 'Apply for Loan', path: '/dashboard/loans/apply', icon: FileText },
      { name: 'Investments', path: '/dashboard/investments', icon: TrendingUp },
      { name: 'Portfolio', path: '/dashboard/investments/portfolio', icon: PiggyBank },
      { name: 'Wealth Engine', path: '/dashboard/wealth-engine', icon: LineChart },
    ],
  },
  {
    title: 'Governance & Tools',
    items: [
      { name: 'Voting', path: '/dashboard/voting', icon: Vote },
      { name: 'Approvals', path: '/dashboard/approvals', icon: CheckSquare },
      { name: 'Reports', path: '/dashboard/reports', icon: FileBarChart },
      { name: 'M-Pesa Integration', path: '/dashboard/mpesa-integration', icon: Smartphone },
    ],
  },
  {
    title: 'Collaboration',
    items: [
      { name: 'Chat', path: '/dashboard/chat', icon: MessageSquare },
      { name: 'Meetings', path: '/dashboard/meetings', icon: Calendar },
      { name: 'Documents', path: '/dashboard/documents', icon: FolderOpen },
    ],
  },
  {
    title: 'Administration',
    items: [
      { name: 'Admin Panel', path: '/dashboard/admin', icon: Shield, adminOnly: true },
    ],
    adminOnly: true,
  },
  {
    title: 'Account',
    items: [
      { name: 'Profile', path: '/dashboard/profile', icon: UserCircle },
      { name: 'Settings', path: '/dashboard/settings', icon: Settings },
      { name: 'Two-Factor Auth', path: '/dashboard/two-factor-auth', icon: Shield },
      { name: 'Audit Log', path: '/dashboard/audit-log', icon: Shield },
    ],
  },
];

interface DashboardLayoutProps {
  children: React.ReactNode;
}

interface SidebarProps {
  isMobile?: boolean;
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  expandedSections: Set<string>;
  toggleSection: (title: string) => void;
  isActivePath: (path: string) => boolean;
  handleLogout: () => void;
  setMobileMenuOpen: (open: boolean) => void;
  isAdmin: boolean;
}

function Sidebar({
  isMobile = false,
  sidebarOpen,
  setSidebarOpen,
  expandedSections,
  toggleSection,
  isActivePath,
  handleLogout,
  setMobileMenuOpen,
  isAdmin,
}: SidebarProps) {
  const { user } = useAuth();

  return (
    <div
      className={`${
        isMobile ? 'w-full' : sidebarOpen ? 'w-64' : 'w-16'
      } bg-white border-r border-gray-200 flex flex-col h-full transition-all duration-300 shadow-lg`}
    >
      {/* Logo & Toggle - Fixed at top */}
      <div className="p-4 border-b border-gray-200 flex items-center justify-between flex-shrink-0">
        {(sidebarOpen || isMobile) && (
          <h1 className="text-lg font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            ChamaNexus
          </h1>
        )}
        {!isMobile && (
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-1.5 hover:bg-gray-100 rounded transition-all"
            title={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            {sidebarOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
          </button>
        )}
      </div>

      {/* User Profile Section */}
      {(sidebarOpen || isMobile) && user && (
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-semibold">
              {user?.first_name?.charAt(0)}{user?.last_name?.charAt(0)}
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">{user?.first_name} {user?.last_name}</p>
              <p className="text-xs text-gray-500">{user?.email}</p>
            </div>
          </div>
        </div>
      )}

      {/* Navigation - Scrollable area */}
      <div className="flex-1 flex flex-col min-h-0">
        <nav className="flex-1 overflow-y-auto p-3 space-y-1">
          {navigationSections
            .filter((section) => !section.adminOnly || isAdmin)
            .map((section) => (
            <div key={section.title} className="space-y-1">
              {(sidebarOpen || isMobile) && (
                <button
                  onClick={() => toggleSection(section.title)}
                  className="flex items-center justify-between w-full px-3 py-2 text-xs font-bold uppercase tracking-wide bg-gradient-to-r from-blue-50 to-purple-50 hover:from-blue-100 hover:to-purple-100 text-gray-700 rounded transition-all"
                >
                  <span>{section.title}</span>
                  <ChevronDown
                    className={`h-3.5 w-3.5 transition-transform duration-200 ${
                      expandedSections.has(section.title) ? 'rotate-0' : '-rotate-90'
                    }`}
                  />
                </button>
              )}
              <AnimatePresence>
                {(expandedSections.has(section.title) || !sidebarOpen) && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.2 }}
                    className="space-y-0.5 py-1"
                  >
                    {section.items
                      .filter((item) => !item.adminOnly || isAdmin)
                      .map((item) => {
                      const Icon = item.icon;
                      const isActive = isActivePath(item.path);
                      return (
                        <Link
                          key={item.path}
                          to={item.path}
                          onClick={() => isMobile && setMobileMenuOpen(false)}
                          className={`flex items-center gap-3 px-3 py-2 rounded transition-all duration-150 ${
                            isActive
                              ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white font-medium'
                              : 'hover:bg-gray-100 text-gray-700 hover:text-gray-900'
                          } ${!sidebarOpen && !isMobile ? 'justify-center' : ''}`}
                          title={!sidebarOpen && !isMobile ? item.name : undefined}
                        >
                          <Icon className={`h-4 w-4 flex-shrink-0`} />
                          {(sidebarOpen || isMobile) && (
                            <span className="text-sm">{item.name}</span>
                          )}
                        </Link>
                      );
                    })}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </nav>
      </div>

      {/* Logout Button - Fixed at bottom */}
      <div className="p-3 border-t border-gray-200 flex-shrink-0">
        <button
          onClick={handleLogout}
          className={`flex items-center gap-3 px-3 py-2 rounded w-full text-red-600 hover:bg-red-50 transition-all ${
            !sidebarOpen && !isMobile ? 'justify-center' : ''
          }`}
          title={!sidebarOpen && !isMobile ? 'Logout' : undefined}
        >
          <LogOut className="h-4 w-4 flex-shrink-0" />
          {(sidebarOpen || isMobile) && <span className="text-sm font-medium">Logout</span>}
        </button>
      </div>
    </div>
  );
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(
    new Set(navigationSections.map((section) => section.title))
  );
  const [isAdmin, setIsAdmin] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  useEffect(() => {
    // Check if user is admin (based on user data)
    if (user) {
      // You can add admin logic here based on your user model
      setIsAdmin(user.is_staff || false);
    }
  }, [user]);

  const toggleSection = (title: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(title)) {
      newExpanded.delete(title);
    } else {
      newExpanded.add(title);
    }
    setExpandedSections(newExpanded);
  };

  const handleLogout = async () => {
    await logout();
  };

  const isActivePath = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-50 to-blue-50 overflow-hidden">
      {/* Desktop Sidebar */}
      <div className="hidden lg:flex lg:flex-col h-full flex-shrink-0">
        <Sidebar
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
          expandedSections={expandedSections}
          toggleSection={toggleSection}
          isActivePath={isActivePath}
          handleLogout={handleLogout}
          setMobileMenuOpen={setMobileMenuOpen}
          isAdmin={isAdmin}
        />
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileMenuOpen(false)}
              className="fixed inset-0 bg-black/50 z-40 lg:hidden"
            />
            <motion.div
              initial={{ x: -300 }}
              animate={{ x: 0 }}
              exit={{ x: -300 }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed inset-y-0 left-0 z-50 lg:hidden"
            >
              <Sidebar
                isMobile
                sidebarOpen={sidebarOpen}
                setSidebarOpen={setSidebarOpen}
                expandedSections={expandedSections}
                toggleSection={toggleSection}
                isActivePath={isActivePath}
                handleLogout={handleLogout}
                setMobileMenuOpen={setMobileMenuOpen}
                isAdmin={isAdmin}
              />
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Mobile Header */}
        <div className="lg:hidden border-b border-gray-200 bg-white p-4 flex items-center justify-between flex-shrink-0">
          <button
            onClick={() => setMobileMenuOpen(true)}
            className="p-2 hover:bg-gray-100 rounded transition-all"
          >
            <Menu className="h-5 w-5" />
          </button>
          <h1 className="text-base font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            ChamaNexus
          </h1>
          <div className="w-9" /> {/* Spacer for centering */}
        </div>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto overflow-x-hidden p-4 lg:p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
