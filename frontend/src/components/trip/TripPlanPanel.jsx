import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plane, Hotel, Map, Utensils, X } from 'lucide-react'
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

    return (
        <motion.div initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25 }}
            className="h-full flex flex-col bg-navy-light border-l border-border/50">
            {/* Header */}
            <div className="p-4 border-b border-border/50 flex items-center justify-between">
                <div>
                    <h3 className="text-sm font-semibold text-white">
                        {tripPlan?.source || recommendedFlight?.source} → {tripPlan?.destination || recommendedFlight?.destination}
                    </h3>
                    <p className="text-xs text-gray-400">{tripPlan?.travel_date || 'Trip Plan'}</p>
                </div>
                <button onClick={onClose} className="p-1 hover:bg-card rounded-lg transition-colors lg:hidden">
                    <X size={16} className="text-gray-400" />
                </button>
            </div>

            {/* Tabs */}
            <div className="flex border-b border-border/30">
                {tabs.map((tab) => (
                    <button key={tab.key} onClick={() => setActiveTab(tab.key)}
                        className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 text-xs font-medium transition-colors
              ${activeTab === tab.key ? 'text-primary border-b-2 border-primary' : 'text-gray-400 hover:text-gray-200'}`}>
                        <tab.icon size={12} />{tab.label}
                    </button>
                ))}
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {activeTab === 'flight' && (
                    <>
                        {recommendedFlight && (
                            <div className="relative">
                                <FlightCard flight={recommendedFlight} />
                                <div className="flex justify-center mt-3">
                                    <CCSGauge score={recommendedFlight.ccs_score} />
                                </div>
                            </div>
                        )}
                        {rankedFlights.length > 1 && (
                            <div>
                                <h4 className="text-xs font-medium text-gray-400 mb-2">Compare Top Flights</h4>
                                <FlightComparison flights={rankedFlights} />
                            </div>
                        )}
                    </>
                )}

                {activeTab === 'hotel' && (
                    <div className="space-y-3">
                        {recommendedHotels.map((h, i) => <HotelCard key={i} hotel={h} />)}
                        {recommendedHotels.length === 0 && <p className="text-sm text-gray-400 text-center py-8">No hotel recommendations yet</p>}
                    </div>
                )}

                {activeTab === 'itinerary' && (
                    <>
                        {itinerary ? <ItineraryTimeline itinerary={itinerary} /> : <p className="text-sm text-gray-400 text-center py-8">No itinerary generated yet</p>}
                    </>
                )}

                {activeTab === 'food' && (
                    <div className="space-y-3">
                        {foodRecommendations.map((f, i) => <FoodCard key={i} food={f} />)}
                        {foodRecommendations.length === 0 && <p className="text-sm text-gray-400 text-center py-8">No food recommendations yet</p>}
                    </div>
                )}
            </div>
        </motion.div>
    )
}
