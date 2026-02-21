import React from 'react'
import { Hotel, Star, MapPin, Shield } from 'lucide-react'

export default function HotelCard({ hotel }) {
    return (
        <div className="glass rounded-xl p-4 hover:border-primary/30 transition-all">
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                    <Hotel size={14} className="text-primary" />
                    <span className="text-sm font-semibold text-white">{hotel.name}</span>
                </div>
                {hotel.rank && <span className="text-xs text-gray-400">#{hotel.rank}</span>}
            </div>
            <div className="flex items-center gap-3 mb-2 text-xs text-gray-400">
                <span className="flex items-center gap-1"><Star size={10} className="text-yellow-400" />{hotel.rating}/5</span>
                <span className="flex items-center gap-1"><MapPin size={10} />{hotel.distance_centre_km}km from centre</span>
                {hotel.safety_score && <span className="flex items-center gap-1"><Shield size={10} className="text-accent" />{Math.round(hotel.safety_score * 100)}% safe</span>}
            </div>
            <div className="text-accent font-bold text-sm">₹{(hotel.price_per_night || 0).toLocaleString()}/night</div>
            {hotel.recommendation_reason && (
                <p className="text-xs text-gray-400 mt-2">{hotel.recommendation_reason}</p>
            )}
            {hotel.highlight && (
                <div className="mt-2 text-xs text-primary">✨ {hotel.highlight}</div>
            )}
        </div>
    )
}
