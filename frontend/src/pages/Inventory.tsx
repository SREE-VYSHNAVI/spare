import { useEffect, useState } from 'react'
import { Package, AlertTriangle, CheckCircle } from 'lucide-react'
import { api } from '../services/api'

function Inventory({ setApiError }: { setApiError: (error: string | null) => void }) {
  const [inventory, setInventory] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'critical' | 'in-stock'>('all')

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const response = await api.get('/api/inventory')
        setInventory(Array.isArray(response.data) ? response.data : response.data.inventory || [])
      } catch (error) {
        setApiError(error instanceof Error ? error.message : 'Failed to fetch inventory')
      } finally {
        setLoading(false)
      }
    }
    fetchInventory()
  }, [])

  const filteredInventory = inventory.filter((item) => {
    if (filter === 'critical') return item.current_stock === 0
    if (filter === 'in-stock') return item.current_stock > 0
    return true
  })

  if (loading) return <div className="text-center">Loading...</div>

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Inventory Management</h1>
        <div className="flex space-x-2">
          {(['all', 'critical', 'in-stock'] as const).map((f) => (
            <button key={f} onClick={() => setFilter(f)} className={`px-4 py-2 rounded-lg ${filter === f ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
              {f.replace('-', ' ')}
            </button>
          ))}
        </div>
      </div>
      <div className="grid gap-4">
        {filteredInventory.map((item, i) => (
          <div key={i} className="bg-white p-4 rounded-lg shadow-md border-l-4 border-blue-500">
            <div className="flex items-start justify-between">
              <div><h3 className="font-bold">{item.part_name}</h3><p className="text-sm text-gray-600">{item.part_no}</p>
              <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                <div><span className="text-gray-600">Stock:</span> <span className="font-medium">{item.current_stock}</span></div>
                <div><span className="text-gray-600">Lead:</span> <span className="font-medium">{item.vendor_lead_time_days}d</span></div>
              </div></div>
              {item.current_stock === 0 ? <AlertTriangle className="text-red-600" /> : <CheckCircle className="text-green-600" />}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Inventory