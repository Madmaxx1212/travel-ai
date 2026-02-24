import React from 'react'
import { Utensils, MapPin, Star } from 'lucide-react'

export default function FoodCard({ food }) {
    return (
        <div className="glass-card rounded-2xl p-4 group">
            <div className="flex items-center gap-2.5 mb-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-500/15 to-orange-500/10 flex items-center justify-center">
                    <Utensils size={13} className="text-amber-400" />
                </div>
                <div className="flex-1 min-w-0">
                    <span className="text-sm font-semibold text-white block truncate">{food.name}</span>
                    <span className="text-[10px] text-slate-500 capitalize">{food.type || 'meal'}</span>
                </div>
            </div>

            <div className="flex items-center gap-2 text-xs text-slate-400 mb-2">
                <span className="px-2 py-0.5 rounded-full bg-surface-elevated text-[10px]">{food.cuisine}</span>
                <span className="flex items-center gap-0.5">
                    <MapPin size={10} className="text-slate-600" />{food.area}
                </span>
            </div>

            <div className="flex items-center justify-between">
                <span className="text-xs text-accent font-medium">{food.price_range}</span>
                {food.must_try && (
                    <span className="flex items-center gap-1 text-[10px] text-amber-400 font-medium">
                        <Star size={9} fill="currentColor" /> {food.must_try}
                    </span>
                )}
            </div>
        </div>
    )
}
