import React, { useState } from 'react';
import { Cpu, Send } from 'lucide-react';
import { sendAIChatQuery } from '../services/api';

export default function AIChatBox() {
    const [chatQuery, setChatQuery] = useState('');
    const [chatLog, setChatLog] = useState<{ sender: string; text: string }[]>([
        { sender: 'SpareWise AI', text: 'Hello! I am monitoring all thermal assets. Ask me about stock shortages or machine risks.' }
    ]);
    const [loadingAI, setLoadingAI] = useState(false);

    const handleSendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!chatQuery.trim()) return;

        const userMsg = chatQuery;
        setChatLog(prev => [...prev, { sender: 'You', text: userMsg }]);
        setChatQuery('');
        setLoadingAI(true);

        try {
            const aiResponse = await sendAIChatQuery(userMsg);
            setChatLog(prev => [...prev, { sender: 'SpareWise AI', text: aiResponse }]);
        } catch (err) {
            setChatLog(prev => [...prev, { sender: 'SpareWise AI', text: 'Error connecting to backend services.' }]);
        } finally {
            setLoadingAI(false);
        }
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col h-[500px]">
            <h2 className="text-lg font-semibold mb-4 text-slate-200 flex items-center gap-2">
                <Cpu className="w-5 h-5 text-indigo-400" /> SpareWise AI Assistant
            </h2>
            
            <div className="flex-1 overflow-y-auto space-y-3 pr-2 mb-4">
                {chatLog.map((msg, idx) => (
                    <div key={idx} className={`p-3 rounded-lg text-sm ${msg.sender === 'You' ? 'bg-cyan-950/40 border border-cyan-800/50 ml-6 text-slate-200' : 'bg-slate-800/60 mr-6 text-slate-300'}`}>
                        <p className="text-xs font-bold text-slate-400 mb-1">{msg.sender}</p>
                        <p>{msg.text}</p>
                    </div>
                ))}
                {loadingAI && <div className="text-xs text-slate-500 italic animate-pulse">SpareWise AI is analyzing plant telemetry...</div>}
            </div>

            <form onSubmit={handleSendMessage} className="flex gap-2">
                <input
                    type="text"
                    value={chatQuery}
                    onChange={(e) => setChatQuery(e.target.value)}
                    placeholder="Ask about BFP-01 or parts..."
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-cyan-500"
                />
                <button type="submit" className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-lg transition-colors flex items-center justify-center">
                    <Send className="w-4 h-4" />
                </button>
            </form>
        </div>
    );
}