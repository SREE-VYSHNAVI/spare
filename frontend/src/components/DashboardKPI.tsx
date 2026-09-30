import React from 'react';
import { AlertTriangle, ShieldAlert } from 'lucide-react';

interface KPIsProps {
    summary: any;
}

export default function DashboardKPIs({ summary }: KPIsProps) {
    return (
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
    );
}