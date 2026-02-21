import React from 'react'
import { Utensils, MapPin } from 'lucide-react'

export default function FoodCard({ food }) {
    return (
        <div className="glass rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
                <Utensils size={12} className="text-orange-400" />
                <span className="text-sm font-medium text-white">{food.name}</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-gray-400 mb-1">
                <span>{food.cuisine}</span>
                <span>•</span>
                <span className="flex items-center gap-0.5"><MapPin size={10} />{food.area}</span>
            </div>
            <div className="flex items-center justify-between text-xs">
                <span className="text-accent">{food.price_range}</span>
                {food.must_try && <span className="text-yellow-400">⭐ {food.must_try}</span>}
            </div>
        </div>
    )
}
