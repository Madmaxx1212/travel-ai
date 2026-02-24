import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plane, Hotel, Map, Utensils, X, ArrowRight } from 'lucide-react'
import useStore from '../../store/useStore'
import FlightCard from '../flight/FlightCard'
import FlightComparison from '../flight/FlightComparison'
import HotelCard from '../trip/HotelCard'
import ItineraryTimeline from '../trip/ItineraryTimeline'
import FoodCard from '../trip/FoodCard'
import CCSGauge from '../flight/CCSGauge'

const tabs = [
    { key: 'flight', label: 'Flight', icon: Plane },
    { key: 'hotel', label: 'Hotel', icon: Hotel },
    { key: 'itinerary', label: 'Itinerary', icon: Map },
    { key: 'food', label: 'Food', icon: Utensils },
]

export default function TripPlanPanel({ onClose }) {
    const [activeTab, setActiveTab] = useState('flight')
    const { rankedFlights, recommendedFlight, recommendedHotels, itinerary, foodRecommendations, tripPlan } = useStore()
    const hasData = rankedFlights.length > 0 || recommendedHotels.length > 0 || itinerary

    if (!hasData) return null

    const activeTabIdx = tabs.findIndex(t => t.key === activeTab)

    return (
        <motion.div initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 28, stiffness: 300 }}
            className="h-full flex flex-col bg-navy-light border-l border-border-subtle">

            {/* Header */}
            <div className="p-5 border-b border-border-subtle">
                <div className="flex items-center justify-between">
                    <div>
                        <h3 className="font-display text-sm font-semibold text-white flex items-center gap-2">
                            {tripPlan?.source || recommendedFlight?.source}
                            <ArrowRight size={12} className="text-primary-light" />
                            {tripPlan?.destination || recommendedFlight?.destination}
                        </h3>
                        <p className="text-xs text-slate-500 mt-0.5">{tripPlan?.travel_date || 'Trip Plan'}</p>
                    </div>
                    <button onClick={onClose}
                        className="p-1.5 rounded-lg hover:bg-surface-elevated text-slate-500 hover:text-white transition-all lg:hidden">
                        <X size={16} />
                    </button>
                </div>
            </div>

            {/* Tab bar with sliding indicator */}
            <div className="relative flex border-b border-border-subtle">
                {tabs.map((tab) => (
                    <button key={tab.key} onClick={() => setActiveTab(tab.key)}
                        className={`flex-1 flex items-center justify-center gap-1.5 py-3 text-xs font-medium transition-colors relative z-10
                        ${activeTab === tab.key ? 'text-primary-light' : 'text-slate-500 hover:text-slate-300'}`}>
                        <tab.icon size={13} />{tab.label}
                    </button>
                ))}
                {/* Sliding indicator */}
                <motion.div
                    className="absolute bottom-0 h-0.5 bg-gradient-to-r from-primary to-cyan rounded-full"
                    animate={{ left: `${activeTabIdx * 25}%`, width: '25%' }}
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                />
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <AnimatePresence mode="wait">
                    {activeTab === 'flight' && (
                        <motion.div key="flight" initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }}>
                            {recommendedFlight && (
                                <div className="relative mb-4">
                                    <FlightCard flight={recommendedFlight} />
                                    <div className="flex justify-center mt-4">
                                        <CCSGauge score={recommendedFlight.ccs_score} />
                                    </div>
                                </div>
                            )}
                            {rankedFlights.length > 1 && (
                                <div>
                                    <h4 className="text-xs font-medium text-slate-500 mb-3 uppercase tracking-wider">Compare Top Flights</h4>
                                    <FlightComparison flights={rankedFlights} />
                                </div>
                            )}
                        </motion.div>
                    )}

                    {activeTab === 'hotel' && (
                        <motion.div key="hotel" initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }}
                            className="space-y-3">
                            {recommendedHotels.map((h, i) => <HotelCard key={i} hotel={h} />)}
                            {recommendedHotels.length === 0 && (
                                <p className="text-sm text-slate-500 text-center py-12">No hotel recommendations yet</p>
                            )}
                        </motion.div>
                    )}

                    {activeTab === 'itinerary' && (
                        <motion.div key="itinerary" initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }}>
                            {itinerary ? <ItineraryTimeline itinerary={itinerary} /> : (
                                <p className="text-sm text-slate-500 text-center py-12">No itinerary yet</p>
                            )}
                        </motion.div>
                    )}

                    {activeTab === 'food' && (
                        <motion.div key="food" initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }}
                            className="space-y-3">
                            {foodRecommendations.map((f, i) => <FoodCard key={i} food={f} />)}
                            {foodRecommendations.length === 0 && (
                                <p className="text-sm text-slate-500 text-center py-12">No food recommendations yet</p>
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </motion.div>
    )
}
