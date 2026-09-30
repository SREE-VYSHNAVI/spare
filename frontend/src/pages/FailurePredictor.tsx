import { useState } from 'react'
import { AlertTriangle } from 'lucide-react'
import { api } from '../services/api'

function FailurePredictor({ setApiError }: { setApiError: (error: string | null) => void }) {
  const [formData, setFormData] = useState({ vibration_mm_s: 2.0, bearing_temp_c: 65.0, motor_current_a: 150.0, pressure_bar: 100.0 })
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) })
  }

  const handlePredict = async () => {
    try {
      setLoading(true)
      const response = await api.post('/api/predict/failure', formData)
      setResult(response.data)
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Machine Failure Prediction</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Sensor Input</h2>
          <div className="space-y-4">
            {Object.entries(formData).map(([key, value]) => {
              const labels: any = { vibration_mm_s: 'Vibration (mm/s)', bearing_temp_c: 'Bearing Temp (°C)', motor_current_a: 'Motor Current (A)', pressure_bar: 'Pressure (bar)' }
              return <div key={key}><label className="block text-sm font-medium mb-1">{labels[key]}</label><input type="number" name={key} value={value} onChange={handleChange} className="w-full px-4 py-2 border rounded-lg" step="0.1" /></div>
            })}
            <button onClick={handlePredict} disabled={loading} className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Predicting...' : 'Predict'}</button>
          </div>
        </div>
        {result && (
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-bold mb-4">Result</h2>
            <div className={`p-4 rounded-lg mb-4 ${result.failure_probability > 0.7 ? 'bg-red-100' : 'bg-yellow-100'}`}>
              <div className="flex items-center space-x-2"><AlertTriangle className="h-5 w-5" /><span className="font-bold">{result.failure_probability > 0.7 ? 'CRITICAL' : 'WARNING'}</span></div>
              <p className="mt-2">Failure: {(result.failure_probability * 100).toFixed(1)}%</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default FailurePredictor