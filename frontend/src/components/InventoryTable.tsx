import React from 'react';
import { Database } from 'lucide-react';

interface InventoryProps {
    inventory: any[];
}

export default function InventoryTable({ inventory }: InventoryProps) {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
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
    );
}