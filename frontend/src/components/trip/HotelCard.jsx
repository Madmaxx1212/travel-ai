import React from 'react'
import { Hotel, Star, MapPin, Shield } from 'lucide-react'

export default function HotelCard({ hotel }) {
    return (
        <div className="glass-card rounded-2xl p-5 group">
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-lg bg-amber-500/10 flex items-center justify-center">
                        <Hotel size={14} className="text-amber-400" />
                    </div>
                    <span className="text-sm font-semibold text-white">{hotel.name}</span>
                </div>
                {hotel.rank && (
                    <span className="px-2.5 py-0.5 rounded-full bg-surface-elevated text-xs text-slate-400 font-mono">#{hotel.rank}</span>
                )}
            </div>

            <div className="flex items-center gap-4 mb-3 text-xs">
                <span className="flex items-center gap-1 text-amber-400 font-medium">
                    <Star size={11} fill="currentColor" />{hotel.rating}/5
                </span>
                <span className="flex items-center gap-1 text-slate-400">
                    <MapPin size={11} />{hotel.distance_centre_km}km from centre
                </span>
                {hotel.safety_score && (
                    <span className="flex items-center gap-1 text-emerald-400 font-medium">
                        <Shield size={11} />{Math.round(hotel.safety_score * 100)}% safe
                    </span>
                )}
            </div>

            <div className="flex items-center justify-between">
                <div className="font-display text-base font-bold text-accent">
                    &#8377;{(hotel.price_per_night || 0).toLocaleString()}
                    <span className="text-xs text-slate-500 font-normal ml-1">/night</span>
                </div>
            </div>

            {hotel.recommendation_reason && (
                <p className="text-xs text-slate-400 mt-3 leading-relaxed">{hotel.recommendation_reason}</p>
            )}
            {hotel.highlight && (
                <div className="mt-3 inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-primary/10 text-xs text-primary-light">
                    <Star size={10} /> {hotel.highlight}
                </div>
            )}
        </div>
    )
}
