import React from 'react'
import { Star, TrendingDown } from 'lucide-react'

export default function FlightComparison({ flights }) {
    if (!flights || flights.length === 0) return null

    const bestPrice = Math.min(...flights.map(f => f.price || Infinity))
    const bestDelay = Math.min(...flights.map(f => f.delay_probability || 1))
    const bestCCS = Math.max(...flights.map(f => f.ccs_score || 0))

    return (
        <div className="glass-card rounded-2xl overflow-hidden">
            {/* Header */}
            <div className="grid grid-cols-5 gap-2 px-4 py-3 bg-gradient-to-r from-primary/5 to-transparent border-b border-border-subtle">
                <span className="text-xs font-medium text-slate-400">Flight</span>
                <span className="text-xs font-medium text-slate-400 text-right">Price</span>
                <span className="text-xs font-medium text-slate-400 text-right">Delay Risk</span>
                <span className="text-xs font-medium text-slate-400 text-right">CCS</span>
                <span className="text-xs font-medium text-slate-400 text-right">Duration</span>
            </div>

            {/* Rows */}
            {flights.map((f, i) => {
                const ccs = Math.round((f.ccs_score || 0) * 100)
                const delay = Math.round((f.delay_probability || 0) * 100)
                const isBestPrice = f.price === bestPrice
                const isBestDelay = f.delay_probability === bestDelay
                const isBestCCS = f.ccs_score === bestCCS

                return (
                    <div key={i} className={`grid grid-cols-5 gap-2 px-4 py-3 items-center transition-colors hover:bg-primary/5
                        ${i < flights.length - 1 ? 'border-b border-border-subtle' : ''}
                        ${f.recommended ? 'bg-primary/5' : ''}`}>

                        <div>
                            <div className="text-xs font-medium text-white">{f.airline}</div>
                            <div className="text-[10px] text-slate-500 font-mono">{f.flight_number}</div>
                        </div>

                        <div className={`text-right text-xs font-semibold ${isBestPrice ? 'text-accent' : 'text-slate-300'}`}>
                            &#8377;{(f.price || 0).toLocaleString()}
                        </div>

                        <div className={`text-right text-xs font-medium ${isBestDelay ? 'text-emerald-400' : delay > 20 ? 'text-rose-400' : 'text-slate-300'}`}>
                            {delay}%
                        </div>

                        <div className={`text-right text-xs font-semibold ${isBestCCS ? 'text-primary-light' : 'text-slate-300'}`}>
                            {ccs}
                        </div>

                        <div className="text-right text-xs text-slate-400">{f.duration_mins}m</div>
                    </div>
                )
            })}
        </div>
    )
}
