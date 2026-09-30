import { useState } from 'react'
import { Clock } from 'lucide-react'
import { api } from '../services/api'

function LeadTimePredictor({ setApiError }: { setApiError: (error: string | null) => void }) {
  const [formData, setFormData] = useState({ part_no: 'BFP-PRT-BRG-01', season: 'Summer', market_condition: 'Normal' })
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const parts = ['BFP-PRT-BRG-01', 'ST-PRT-BLD-02', 'CWP-PRT-IMP-03', 'CC-PRT-BLT-01']
  const seasons = ['Summer', 'Monsoon', 'Winter']
  const conditions = ['Normal', 'High Demand (Shortage)']

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handlePredict = async () => {
    try {
      setLoading(true)
      const response = await api.post('/api/predict/lead-time', formData)
      setResult(response.data)
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Lead Time Predictor</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Parameters</h2>
          <div className="space-y-4">
            <div><label className="block text-sm font-medium mb-1">Part</label><select name="part_no" value={formData.part_no} onChange={handleChange} className="w-full px-4 py-2 border rounded-lg">{parts.map(p => <option key={p} value={p}>{p}</option>)}</select></div>
            <div><label className="block text-sm font-medium mb-1">Season</label><select name="season" value={formData.season} onChange={handleChange} className="w-full px-4 py-2 border rounded-lg">{seasons.map(s => <option key={s} value={s}>{s}</option>)}</select></div>
            <div><label className="block text-sm font-medium mb-1">Market</label><select name="market_condition" value={formData.market_condition} onChange={handleChange} className="w-full px-4 py-2 border rounded-lg">{conditions.map(c => <option key={c} value={c}>{c}</option>)}</select></div>
            <button onClick={handlePredict} disabled={loading} className="w-full bg-blue-600 text-white py-2 rounded-lg">{loading ? 'Calculating...' : 'Predict'}</button>
          </div>
        </div>
        {result && <div className="bg-white p-6 rounded-lg shadow-md"><h2 className="text-xl font-bold mb-4">Result</h2><div className="p-4 bg-blue-50 border rounded-lg"><div className="flex items-center space-x-2 mb-2"><Clock className="h-5 w-5" /><span className="text-sm text-gray-600">Estimated Delivery</span></div><p className="text-3xl font-bold">{result.predicted_lead_time || result.lead_time_days || 'N/A'} <span className="text-lg text-gray-600 ml-2">days</span></p></div></div>}
      </div>
    </div>
  )
}

export default LeadTimePredictor