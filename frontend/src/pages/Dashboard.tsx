import { useEffect, useState } from 'react'
import { Activity, AlertCircle, TrendingDown, Package } from 'lucide-react'
import { api } from '../services/api'

function Dashboard({ setApiError }: { setApiError: (error: string | null) => void }) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await api.get('/api/dashboard')
        setData(response.data)
        setApiError(null)
      } catch (error) {
        setApiError(error instanceof Error ? error.message : 'Failed to fetch dashboard')
      } finally {
        setLoading(false)
      }
    }
    fetchDashboard()
  }, [])

  if (loading) return <div className="text-center text-gray-600">Loading...</div>

  const stats = [
    { title: 'Total Assets', value: data?.total_assets || 5, icon: Activity, color: 'bg-blue-100 text-blue-600' },
    { title: 'Critical Alerts', value: data?.critical_alerts || 0, icon: AlertCircle, color: 'bg-red-100 text-red-600' },
    { title: 'Parts in Stock', value: data?.parts_in_stock || 0, icon: Package, color: 'bg-green-100 text-green-600' },
    { title: 'Avg Lead Time', value: `${data?.avg_lead_time || 14} days`, icon: TrendingDown, color: 'bg-yellow-100 text-yellow-600' },
  ]

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Executive Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => {
          const Icon = stat.icon
          return (
            <div key={i} className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex items-center justify-between">
                <div><p className="text-gray-600 text-sm">{stat.title}</p><p className="text-3xl font-bold mt-2">{stat.value}</p></div>
                <div className={`p-3 rounded-lg ${stat.color}`}><Icon className="h-6 w-6" /></div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Dashboard