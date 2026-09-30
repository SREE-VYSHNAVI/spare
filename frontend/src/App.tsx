import React, { useEffect, useState } from 'react';
import { fetchDashboardSummary, fetchInventoryStatus, sendAIChatQuery } from './services/api';
import { ShieldAlert, Cpu, Database, Send, AlertTriangle } from 'lucide-react';

export default function App() {
    const [summary, setSummary] = useState<any>(null);
    const [inventory, setInventory] = useState<any[]>([]);
    const [chatQuery, setChatQuery] = useState('');
    const [chatLog, setChatLog] = useState<{ sender: string; text: string }[]>([
        { sender: 'SpareWise AI', text: 'Hello! I am monitoring all thermal assets. Ask me about stock shortages or machine risks.' }
    ]);
    const [loadingAI, setLoadingAI] = useState(false);

    useEffect(() => {
        // Load backend data on mount
        fetchDashboardSummary().then(setSummary).catch(console.error);
        fetchInventoryStatus().then(setInventory).catch(console.error);
    }, []);

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
        <div className="min-h-screen bg-slate-950 text-slate-100 p-6 font-sans">
            {/* Header */}
            <header className="flex justify-between items-center mb-8 border-b border-slate-800 pb-4">
                <div>
                    <h1 className="text-2xl font-bold tracking-wider text-cyan-400 flex items-center gap-2">
                        <Cpu className="w-7 h-7" /> SPAREWISE AI // Thermal Plant Intelligence
                    </h1>
                    <p className="text-sm text-slate-400">Predictive Maintenance & Supply Chain Optimization Platform</p>
                </div>
                <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg">
                    <span className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></span>
                    <span className="text-xs font-medium text-emerald-400">System Live & Connected</span>
                </div>
            </header>

            {/* KPI Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
                    <p className="text-xs text-slate-400 uppercase tracking-wider">Monitored Assets</p>
                    <p className="text-3xl font-bold text-white mt-1">{summary?.assets_monitored || 5}</p>
                </div>
                <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
                    <p className="text-xs text-slate-400 uppercase tracking-wider">High Risk Machines</p>
                    <p className="text-3xl font-bold text-amber-400 mt-1 flex items-center gap-2">
                        <AlertTriangle className="w-6 h-6" /> {summary?.high_risk_assets || 2}
                    </p>
                </div>
                <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
                    <p className="text-xs text-slate-400 uppercase tracking-wider">Critical Shortages</p>
                    <p className="text-3xl font-bold text-rose-500 mt-1 flex items-center gap-2">
                        <ShieldAlert className="w-6 h-6" /> {summary?.critical_spare_shortages || 1}
                    </p>
                </div>
                <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
                    <p className="text-xs text-slate-400 uppercase tracking-wider">Downtime Risk Exposure</p>
                    <p className="text-2xl font-bold text-cyan-400 mt-1">{summary?.estimated_downtime_risk_inr || '750,000 INR'}</p>
                </div>
            </div>

            {/* Main Grid: Inventory Table & AI Assistant */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Inventory Table (Takes 2 cols) */}
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h2 className="text-lg font-semibold mb-4 text-slate-200 flex items-center gap-2">
                        <Database className="w-5 h-5 text-cyan-400" /> Spare Parts & Shortage Watchlist
                    </h2>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse text-sm">
                            <thead>
                                <tr className="border-b border-slate-800 text-slate-400">
                                    <th className="py-3 px-4">Part ID</th>
                                    <th className="py-3 px-4">Description</th>
                                    <th className="py-3 px-4">Stock</th>
                                    <th className="py-3 px-4">Demand</th>
                                    <th className="py-3 px-4">Risk Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {inventory.map((item, index) => (
                                    <tr key={index} className="border-b border-slate-800/50 hover:bg-slate-800/30">
                                        <td className="py-3 px-4 font-mono text-cyan-300">{item.part_id}</td>
                                        <td className="py-3 px-4">{item.part_name}</td>
                                        <td className="py-3 px-4 font-bold">{item.current_stock}</td>
                                        <td className="py-3 px-4">{item.expected_demand}</td>
                                        <td className="py-3 px-4">
                                            <span className={`px-2.5 py-1 rounded text-xs font-semibold ${
                                                item.shortage_risk === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-emerald-500/20 text-emerald-400'
                                            }`}>
                                                {item.shortage_risk}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* AI Assistant Chat Box (Takes 1 col) */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col h-[500px]">
                    <h2 className="text-lg font-semibold mb-4 text-slate-200 flex items-center gap-2">
                        <Cpu className="w-5 h-5 text-indigo-400" /> SpareWise AI Assistant
                    </h2>
                    
                    {/* Chat Messages */}
                    <div className="flex-1 overflow-y-auto space-y-3 pr-2 mb-4">
                        {chatLog.map((msg, idx) => (
                            <div key={idx} className={`p-3 rounded-lg text-sm ${msg.sender === 'You' ? 'bg-cyan-950/40 border border-cyan-800/50 ml-6 text-slate-200' : 'bg-slate-800/60 mr-6 text-slate-300'}`}>
                                <p className="text-xs font-bold text-slate-400 mb-1">{msg.sender}</p>
                                <p>{msg.text}</p>
                            </div>
                        ))}
                        {loadingAI && <div className="text-xs text-slate-500 italic animate-pulse">SpareWise AI is analyzing plant telemetry...</div>}
                    </div>

                    {/* Chat Input */}
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
            </div>
        </div>
    );
}