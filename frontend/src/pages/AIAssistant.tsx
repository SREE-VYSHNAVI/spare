import { useState, useRef, useEffect } from 'react'
import { Send, MessageCircle } from 'lucide-react'
import { api } from '../services/api'

function AIAssistant({ setApiError }: { setApiError: (error: string | null) => void }) {
  const [messages, setMessages] = useState<any[]>([{ type: 'assistant', content: 'Hello! I am SpareWise AI. How can I help?' }])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  useEffect(() => scrollToBottom(), [messages])

  const handleSend = async () => {
    if (!input.trim()) return
    setMessages(prev => [...prev, { type: 'user', content: input }])
    const userInput = input
    setInput('')

    try {
      setLoading(true)
      const response = await api.post('/api/ai/query', { query: userInput })
      setMessages(prev => [...prev, { type: 'assistant', content: response.data.response }])
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">AI Assistant</h1>
      <div className="bg-white rounded-lg shadow-md flex flex-col h-[600px]">
        <div className="flex items-center space-x-2 p-4 border-b">
          <MessageCircle className="h-5 w-5" />
          <h2 className="font-bold">Chat</h2>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, i) => <div key={i} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}><div className={`max-w-xs px-4 py-2 rounded-lg ${msg.type === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}><p className="text-sm">{msg.content}</p></div></div>)}
          {loading && <div className="flex justify-start"><div className="bg-gray-100 px-4 py-2 rounded-lg">Typing...</div></div>}
          <div ref={messagesEndRef} />
        </div>
        <div className="p-4 border-t flex space-x-2">
          <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyPress={e => e.key === 'Enter' && handleSend()} placeholder="Ask..." className="flex-1 px-4 py-2 border rounded-lg" />
          <button onClick={handleSend} disabled={loading || !input.trim()} className="bg-blue-600 text-white px-4 py-2 rounded-lg"><Send className="h-5 w-5" /></button>
        </div>
      </div>
    </div>
  )
}

export default AIAssistant