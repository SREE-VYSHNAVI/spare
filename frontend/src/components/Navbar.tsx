import { Zap, BarChart3, Package, AlertTriangle, Clock, MessageCircle } from 'lucide-react'

interface NavbarProps {
  currentPage: string
  setCurrentPage: (page: string) => void
}

function Navbar({ currentPage, setCurrentPage }: NavbarProps) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'inventory', label: 'Inventory', icon: Package },
    { id: 'failure', label: 'Failure Prediction', icon: AlertTriangle },
    { id: 'leadtime', label: 'Lead Time', icon: Clock },
    { id: 'assistant', label: 'AI Assistant', icon: MessageCircle },
  ]

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <Zap className="h-6 w-6 text-blue-600" />
            <span className="text-2xl font-bold text-gray-900">SpareWise AI</span>
          </div>
          <div className="flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <button key={item.id} onClick={() => setCurrentPage(item.id)} className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors ${currentPage === item.id ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-100'}`}>
                  <Icon className="h-4 w-4" />
                  <span className="text-sm font-medium">{item.label}</span>
                </button>
              )
            })}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar