import { useState } from 'react'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Inventory from './pages/Inventory'
import FailurePredictor from './pages/FailurePredictor'
import LeadTimePredictor from './pages/LeadTimePredictor'
import AIAssistant from './pages/AIAssistant'
import { AlertCircle } from 'lucide-react'

function App() {
  const [currentPage, setCurrentPage] = useState<string>('dashboard')
  const [apiError, setApiError] = useState<string | null>(null)

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard setApiError={setApiError} />
      case 'inventory':
        return <Inventory setApiError={setApiError} />
      case 'failure':
        return <FailurePredictor setApiError={setApiError} />
      case 'leadtime':
        return <LeadTimePredictor setApiError={setApiError} />
      case 'assistant':
        return <AIAssistant setApiError={setApiError} />
      default:
        return <Dashboard setApiError={setApiError} />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      
      {apiError && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 m-4 rounded">
          <div className="flex items-center">
            <AlertCircle className="h-5 w-5 text-red-400 mr-2" />
            <p className="text-red-700 text-sm">{apiError}</p>
            <button onClick={() => setApiError(null)} className="ml-auto text-red-700 hover:text-red-900">✕</button>
          </div>
        </div>
      )}
      
      <main className="container mx-auto py-8">
        {renderPage()}
      </main>
    </div>
  )
}

export default App