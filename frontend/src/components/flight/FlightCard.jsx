import React from 'react'
import { motion } from 'framer-motion'
import { Plane, Clock, AlertTriangle, Star, ChevronDown, ChevronUp } from 'lucide-react'
import Badge from '../ui/Badge'
import ScoreGauge from '../ui/ScoreGauge'

export default function FlightCard({ flight, compact = false }) {
    const [expanded, setExpanded] = React.useState(false)
    const ccsPercent = Math.round((flight.ccs_score || 0) * 100)
    const delayPct = Math.round((flight.delay_probability || 0) * 100)

    const riskVariant = flight.risk_level === 'low' ? 'low' : flight.risk_level === 'medium' ? 'medium'
        : flight.risk_level === 'high' ? 'high' : 'very_high'

    return (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            whileHover={{ y: -2 }} transition={{ duration: 0.3 }}
            className="glass rounded-xl p-4 hover:border-primary/30 transition-all cursor-pointer"
        >
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-white">{flight.airline}</span>
                    <span className="text-xs text-gray-400">{flight.flight_number}</span>
                </div>
                {flight.recommended && (
                    <Badge variant="success">✨ RECOMMENDED</Badge>
                )}
                {flight.rank && !flight.recommended && (
                    <Badge variant="default">#{flight.rank}</Badge>
                )}
            </div>

            <div className="flex items-center justify-between mb-3">
                <div className="text-center">
                    <div className="text-lg font-bold text-white">{flight.departure_time}</div>
                    <div className="text-xs text-gray-400">{flight.source}</div>
                </div>
                <div className="flex-1 flex items-center px-4">
                    <div className="flex-1 h-[1px] bg-border" />
                    <Plane size={14} className="mx-2 text-primary" />
                    <div className="flex-1 h-[1px] bg-border" />
                </div>
                <div className="text-center">
                    <div className="text-lg font-bold text-white">{flight.arrival_time}</div>
                    <div className="text-xs text-gray-400">{flight.destination}</div>
                </div>
                <div className="ml-4 text-center">
                    <div className="text-xs text-gray-400">{flight.duration_mins}m</div>
                    <div className="text-xs text-gray-500">{flight.stops === 0 ? 'Direct' : `${flight.stops} stop`}</div>
                </div>
            </div>

            <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <span className="text-sm font-bold text-accent">₹{(flight.price || 0).toLocaleString()}</span>
                    <Badge variant={riskVariant}>
                        <Clock size={10} className="mr-1" />{delayPct}% delay
                    </Badge>
                    <Badge variant="primary">
                        <Star size={10} className="mr-1" />CCS {ccsPercent}
                    </Badge>
                </div>

                {!compact && (
                    <button onClick={() => setExpanded(!expanded)} className="text-gray-400 hover:text-white transition-colors">
                        {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </button>
                )}
            </div>

            {expanded && !compact && flight.shap_top3 && (
                <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                    className="mt-3 pt-3 border-t border-border/50">
                    <div className="flex items-center gap-1 mb-2">
                        <span className="text-xs text-gray-400">💡 Why this flight?</span>
                    </div>
                    {flight.shap_top3.map((s, i) => (
                        <div key={i} className="text-xs text-gray-300 mb-1">
                            • <strong>{s.feature}</strong>: {s.direction}
                        </div>
                    ))}
                </motion.div>
            )}
        </motion.div>
    )
}
