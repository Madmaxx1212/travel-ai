import React from 'react'
import { motion } from 'framer-motion'
import { PlaneTakeoff, Map, Clock, TrendingUp } from 'lucide-react'
import useStore from '../store/useStore'
import FlightCard from '../components/flight/FlightCard'
import HotelCard from '../components/trip/HotelCard'
import ItineraryTimeline from '../components/trip/ItineraryTimeline'
import RiskWarningBanner from '../components/risk/RiskWarningBanner'

export default function TripDashboard() {
    const { rankedFlights, recommendedFlight, recommendedHotels, itinerary, riskWarnings, tripPlan } = useStore()

    const stats = [
        { icon: PlaneTakeoff, label: 'Flights Analysed', value: rankedFlights.length || '—', color: 'text-primary' },
        { icon: Clock, label: 'Avg Delay Risk', value: rankedFlights.length ? `${Math.round(rankedFlights.reduce((sum, f) => sum + (f.delay_probability || 0), 0) / rankedFlights.length * 100)}%` : '—', color: 'text-warning' },
        { icon: Map, label: 'Itinerary Days', value: itinerary?.days?.length || '—', color: 'text-accent' },
        { icon: TrendingUp, label: 'Top CCS Score', value: recommendedFlight ? Math.round((recommendedFlight.ccs_score || 0) * 100) : '—', color: 'text-primary' },
    ]

    return (
        <div className="min-h-screen pt-14">
            <div className="max-w-6xl mx-auto px-4 py-8">
                <h1 className="text-2xl font-bold text-white mb-2">Trip Dashboard</h1>
                <p className="text-sm text-gray-400 mb-8">
                    {tripPlan ? `${tripPlan.source} → ${tripPlan.destination}` : 'Start a conversation to see your trip here'}
                </p>

                {/* Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    {stats.map((s, i) => (
                        <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.1 }} className="glass rounded-xl p-4">
                            <s.icon size={20} className={s.color} />
                            <div className="text-2xl font-bold text-white mt-2">{s.value}</div>
                            <div className="text-xs text-gray-400">{s.label}</div>
                        </motion.div>
                    ))}
                </div>

                <div className="grid lg:grid-cols-2 gap-6">
                    {/* Flights */}
                    <div>
                        <h2 className="text-lg font-semibold text-white mb-3">Top Flights</h2>
                        <div className="space-y-3">
                            {rankedFlights.length > 0 ? rankedFlights.map((f, i) => (
                                <FlightCard key={i} flight={f} />
                            )) : <p className="text-sm text-gray-400 glass rounded-xl p-8 text-center">No flights yet. Start planning!</p>}
                        </div>
                    </div>

                    <div className="space-y-6">
                        {/* Risk Warnings */}
                        {riskWarnings.length > 0 && (
                            <div>
                                <h2 className="text-lg font-semibold text-white mb-3">Risk Warnings</h2>
                                <div className="space-y-2">
                                    {riskWarnings.map((w, i) => <RiskWarningBanner key={i} warning={w} />)}
                                </div>
                            </div>
                        )}

                        {/* Hotels */}
                        <div>
                            <h2 className="text-lg font-semibold text-white mb-3">Hotels</h2>
                            <div className="space-y-3">
                                {recommendedHotels.length > 0 ? recommendedHotels.map((h, i) => (
                                    <HotelCard key={i} hotel={h} />
                                )) : <p className="text-sm text-gray-400 glass rounded-xl p-8 text-center">No hotel picks yet</p>}
                            </div>
                        </div>

                        {/* Itinerary */}
                        {itinerary && (
                            <div>
                                <h2 className="text-lg font-semibold text-white mb-3">Itinerary</h2>
                                <ItineraryTimeline itinerary={itinerary} />
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
