import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Clock, MapPin, Camera, Utensils, ChevronDown, ChevronUp, Star } from 'lucide-react'

export default function ItineraryTimeline({ itinerary }) {
    const [expandedDay, setExpandedDay] = React.useState(1)
    if (!itinerary?.days) return null

    return (
        <div className="space-y-3">
            {itinerary.days.map((day) => (
                <div key={day.day} className="relative">
                    {/* Day header */}
                    <button onClick={() => setExpandedDay(expandedDay === day.day ? null : day.day)}
                        className="w-full flex items-center gap-3 p-4 glass-card rounded-2xl group">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-cyan flex items-center justify-center text-sm font-bold text-white font-display shadow-glow-sm">
                            {day.day}
                        </div>
                        <div className="flex-1 text-left">
                            <div className="text-sm font-semibold text-white">Day {day.day}</div>
                            <div className="text-xs text-slate-500">{day.theme}</div>
                        </div>
                        <div className="text-slate-500 group-hover:text-white transition-colors">
                            {expandedDay === day.day ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                        </div>
                    </button>

                    <AnimatePresence>
                        {expandedDay === day.day && (
                            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
                                <div className="ml-5 border-l-2 border-primary/20 pl-5 py-3 space-y-4">
                                    {/* Activities */}
                                    {day.activities?.map((act, i) => (
                                        <div key={i} className="relative flex items-start gap-3">
                                            {/* Timeline dot */}
                                            <div className="absolute -left-[29px] top-1 w-3 h-3 rounded-full bg-navy-light ring-2 ring-primary/30 flex items-center justify-center">
                                                <div className="w-1.5 h-1.5 rounded-full bg-primary-light" />
                                            </div>
                                            <div className="w-7 h-7 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                                                <Camera size={12} className="text-primary-light" />
                                            </div>
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <span className="text-[10px] text-primary-light font-mono font-medium px-1.5 py-0.5 rounded bg-primary/10">{act.time}</span>
                                                    <span className="text-xs text-white font-medium">{act.name}</span>
                                                </div>
                                                <p className="text-xs text-slate-400 mt-1 leading-relaxed">{act.description}</p>
                                                <div className="flex gap-3 mt-1.5">
                                                    <span className="text-[10px] text-slate-600">{act.duration_mins}min</span>
                                                    <span className="text-[10px] text-accent font-medium">{act.cost_estimate}</span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}

                                    {/* Meals */}
                                    {day.meals?.map((meal, i) => (
                                        <div key={`meal-${i}`} className="relative flex items-start gap-3">
                                            <div className="absolute -left-[29px] top-1 w-3 h-3 rounded-full bg-navy-light ring-2 ring-amber-500/30 flex items-center justify-center">
                                                <div className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                                            </div>
                                            <div className="w-7 h-7 rounded-lg bg-amber-500/10 flex items-center justify-center flex-shrink-0">
                                                <Utensils size={12} className="text-amber-400" />
                                            </div>
                                            <div>
                                                <div className="text-xs text-white font-medium capitalize">{meal.type}: {meal.name}</div>
                                                <div className="text-xs text-slate-400 mt-0.5">{meal.cuisine} &middot; {meal.area} &middot; {meal.price_range}</div>
                                                {meal.must_try && (
                                                    <div className="flex items-center gap-1 mt-1 text-[10px] text-amber-400">
                                                        <Star size={9} fill="currentColor" /> Must try: {meal.must_try}
                                                    </div>
                                                )}
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
