import React from 'react'
import { motion } from 'framer-motion'
import { Plane, Clock, Star, ChevronDown, ChevronUp, TrendingDown, Sparkles } from 'lucide-react'
import Badge from '../ui/Badge'

export default function FlightCard({ flight, compact = false }) {
    const [expanded, setExpanded] = React.useState(false)
    const ccsPercent = Math.round((flight.ccs_score || 0) * 100)
    const delayPct = Math.round((flight.delay_probability || 0) * 100)

    const riskColor = delayPct <= 5 ? 'text-emerald-400' : delayPct <= 20 ? 'text-amber-400' : 'text-rose-400'
    const riskBg = delayPct <= 5 ? 'bg-emerald-500/10' : delayPct <= 20 ? 'bg-amber-500/10' : 'bg-rose-500/10'
    const riskVariant = flight.risk_level === 'low' ? 'low' : flight.risk_level === 'medium' ? 'medium'
        : flight.risk_level === 'high' ? 'high' : 'very_high'

    return (
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
            whileHover={{ y: -3 }} transition={{ duration: 0.3 }}
            className={`glass-card rounded-2xl p-5 cursor-pointer ${flight.recommended ? 'ring-1 ring-primary/30 shadow-glow-sm' : ''}`}>

            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2.5">
                    <span className="text-sm font-semibold text-white">{flight.airline}</span>
                    <span className="text-xs text-slate-500 font-mono">{flight.flight_number}</span>
                </div>
                {flight.recommended && (
                    <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-gradient-to-r from-primary/20 to-cyan/10 text-primary-light text-xs font-medium ring-1 ring-primary/20">
                        <Sparkles size={10} /> RECOMMENDED
                    </span>
                )}
                {flight.rank && !flight.recommended && (
                    <span className="px-2.5 py-0.5 rounded-full bg-surface-elevated text-xs text-slate-400 font-mono">#{flight.rank}</span>
                )}
            </div>

            {/* Route */}
            <div className="flex items-center justify-between mb-4">
                <div className="text-center">
                    <div className="text-xl font-bold text-white font-display">{flight.departure_time}</div>
                    <div className="text-xs text-slate-500 mt-0.5">{flight.source}</div>
                </div>
                <div className="flex-1 flex items-center px-4">
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-border-strong to-transparent" />
                    <div className="mx-3 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                        <Plane size={14} className="text-primary-light rotate-45" />
                    </div>
                    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-border-strong to-transparent" />
                </div>
                <div className="text-center">
                    <div className="text-xl font-bold text-white font-display">{flight.arrival_time}</div>
                    <div className="text-xs text-slate-500 mt-0.5">{flight.destination}</div>
                </div>
                <div className="ml-5 text-center">
                    <div className="text-xs text-slate-400 font-medium">{flight.duration_mins}m</div>
                    <div className="text-[10px] text-slate-600">{flight.stops === 0 ? 'Direct' : `${flight.stops} stop`}</div>
                </div>
            </div>

            {/* Bottom stats */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <span className="text-base font-bold text-accent font-display">
                        &#8377;{(flight.price || 0).toLocaleString()}
                    </span>
                    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium ${riskBg} ${riskColor}`}>
                        <TrendingDown size={10} />{delayPct}% delay
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-primary/10 text-primary-light text-[11px] font-medium">
                        <Star size={10} />CCS {ccsPercent}
                    </span>
                </div>
                {!compact && (
                    <button onClick={(e) => { e.stopPropagation(); setExpanded(!expanded) }}
                        className="p-1.5 rounded-lg hover:bg-surface-elevated text-slate-500 hover:text-white transition-all">
                        {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </button>
                )}
            </div>

            {/* Expanded SHAP explanation */}
            {expanded && !compact && flight.shap_top3 && (
                <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                    className="mt-4 pt-4 border-t border-border-subtle">
                    <div className="flex items-center gap-1.5 mb-2.5">
                        <Sparkles size={11} className="text-primary-light" />
                        <span className="text-xs text-slate-400 font-medium">Why this flight?</span>
                    </div>
                    {flight.shap_top3.map((s, i) => (
                        <div key={i} className="flex items-start gap-2 text-xs text-slate-300 mb-1.5">
                            <span className="w-1 h-1 rounded-full bg-primary-light mt-1.5 flex-shrink-0" />
                            <span><strong className="text-white">{s.feature}</strong>: {s.direction}</span>
                        </div>
                    ))}
                </motion.div>
            )}
        </motion.div>
    )
}
