import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Clock, MapPin, Camera, Utensils, ChevronDown, ChevronUp } from 'lucide-react'

const typeIcons = { sightseeing: Camera, food: Utensils, default: MapPin }

export default function ItineraryTimeline({ itinerary }) {
    const [expandedDay, setExpandedDay] = React.useState(1)
    if (!itinerary?.days) return null

    return (
        <div className="space-y-3">
            {itinerary.days.map((day) => (
                <div key={day.day} className="relative">
                    {/* Day header */}
                    <button onClick={() => setExpandedDay(expandedDay === day.day ? null : day.day)}
                        className="w-full flex items-center gap-3 p-3 glass rounded-lg hover:border-primary/30 transition-all">
                        <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-xs font-bold text-primary">
                            {day.day}
                        </div>
                        <div className="flex-1 text-left">
                            <div className="text-sm font-medium text-white">Day {day.day}</div>
                            <div className="text-xs text-gray-400">{day.theme}</div>
                        </div>
                        {expandedDay === day.day ? <ChevronUp size={14} className="text-gray-400" /> : <ChevronDown size={14} className="text-gray-400" />}
                    </button>

                    <AnimatePresence>
                        {expandedDay === day.day && (
                            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
                                <div className="ml-4 border-l-2 border-primary/30 pl-4 py-2 space-y-3">
                                    {/* Activities */}
                                    {day.activities?.map((act, i) => (
                                        <div key={i} className="flex items-start gap-2">
                                            <div className="w-5 h-5 rounded-full bg-card flex items-center justify-center flex-shrink-0 mt-0.5">
                                                <Clock size={10} className="text-primary" />
                                            </div>
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <span className="text-xs text-primary font-medium">{act.time}</span>
                                                    <span className="text-xs text-white font-medium">{act.name}</span>
                                                </div>
                                                <p className="text-xs text-gray-400 mt-0.5">{act.description}</p>
                                                <div className="flex gap-2 mt-1">
                                                    <span className="text-[10px] text-gray-500">{act.duration_mins}min</span>
                                                    <span className="text-[10px] text-accent">{act.cost_estimate}</span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                    {/* Meals */}
                                    {day.meals?.map((meal, i) => (
                                        <div key={`meal-${i}`} className="flex items-start gap-2">
                                            <div className="w-5 h-5 rounded-full bg-orange-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                                                <Utensils size={10} className="text-orange-400" />
                                            </div>
                                            <div>
                                                <div className="text-xs text-white font-medium">{meal.type}: {meal.name}</div>
                                                <div className="text-xs text-gray-400">{meal.cuisine} • {meal.area} • {meal.price_range}</div>
                                                {meal.must_try && <div className="text-[10px] text-yellow-400">⭐ Must try: {meal.must_try}</div>}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            ))}
        </div>
    )
}
