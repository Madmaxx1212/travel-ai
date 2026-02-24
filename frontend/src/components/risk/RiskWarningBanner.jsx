import React from 'react'
import { AlertTriangle, AlertCircle, Info } from 'lucide-react'

const severityConfig = {
    red: { icon: AlertTriangle, bg: 'bg-rose-500/10', border: 'border-rose-500/20', text: 'text-rose-400', glow: 'shadow-[0_0_20px_-4px_rgba(244,63,94,0.3)]' },
    yellow: { icon: AlertCircle, bg: 'bg-amber-500/10', border: 'border-amber-500/20', text: 'text-amber-400', glow: '' },
    green: { icon: Info, bg: 'bg-emerald-500/10', border: 'border-emerald-500/20', text: 'text-emerald-400', glow: '' },
}

export default function RiskWarningBanner({ warning }) {
    const config = severityConfig[warning.severity] || severityConfig.yellow
    const Icon = config.icon

    return (
        <div className={`flex items-start gap-3 p-3.5 rounded-xl ${config.bg} border ${config.border} ${config.glow} transition-all`}>
            <div className="flex-shrink-0 mt-0.5">
                <Icon size={16} className={config.text} />
            </div>
            <div className="flex-1 min-w-0">
                <p className={`text-xs font-medium ${config.text}`}>{warning.flight_number}</p>
                <p className="text-xs text-slate-300 mt-0.5 leading-relaxed">{warning.message}</p>
            </div>
        </div>
    )
}
