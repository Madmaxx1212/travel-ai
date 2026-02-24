import React, { useState, useEffect, useRef, useCallback } from 'react'
import { useLocation } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { PanelRightOpen, PanelRightClose } from 'lucide-react'
import useStore from '../store/useStore'
import ChatWebSocket from '../lib/websocket'
import ChatWindow from '../components/chat/ChatWindow'
import ChatInput from '../components/chat/ChatInput'
import FlightCard from '../components/flight/FlightCard'
import RiskWarningBanner from '../components/risk/RiskWarningBanner'
import TripPlanPanel from '../components/trip/TripPlanPanel'

export default function ChatPage() {
    const location = useLocation()
    const [showPanel, setShowPanel] = useState(false)
    const wsRef = useRef(null)
    const assistantChunks = useRef('')
    const initialSent = useRef(false)

    const {
        sessionId, tripPlanId, messages, isTyping,
        addMessage, setIsTyping, setFlightResults,
        setRiskWarnings, setTripPlan, setTripPlanId,
        rankedFlights, riskWarnings,
    } = useStore()

    const connectWS = useCallback(() => {
        if (wsRef.current) wsRef.current.disconnect()

        const ws = new ChatWebSocket(sessionId, {
            onChunk: (content) => {
                assistantChunks.current += content
            },
            onFlightResults: (data) => {
                setFlightResults(data)
                setShowPanel(true)
            },
            onRiskWarnings: (data) => setRiskWarnings(data),
            onTripPlan: (data) => {
                setTripPlan(data)
                setShowPanel(true)
            },
            onDone: (data) => {
                setIsTyping(false)
                const fullText = data.full_response || assistantChunks.current
                addMessage({ role: 'assistant', content: fullText })
                assistantChunks.current = ''
                if (data.trip_plan_id) setTripPlanId(data.trip_plan_id)
            },
            onError: (err) => {
                setIsTyping(false)
                addMessage({ role: 'assistant', content: `Something went wrong: ${err || 'Please try again.'}` })
                assistantChunks.current = ''
            },
            onConnect: () => { },
            onDisconnect: () => { },
        })
        ws.connect()
        wsRef.current = ws
    }, [sessionId])

    useEffect(() => {
        connectWS()
        return () => wsRef.current?.disconnect()
    }, [connectWS])

    useEffect(() => {
        if (!initialSent.current && location.state?.initialMessage && wsRef.current) {
            const timer = setTimeout(() => {
                if (!initialSent.current) {
                    initialSent.current = true
                    handleSend(location.state.initialMessage)
                }
            }, 1000)
            return () => clearTimeout(timer)
        }
    }, [location.state])

    const handleSend = (text) => {
        addMessage({ role: 'user', content: text })
        setIsTyping(true)
        assistantChunks.current = ''
        wsRef.current?.send(text, tripPlanId)
    }

    return (
        <div className="flex h-[calc(100vh-64px)] mt-16">
            {/* Chat section */}
            <div className="flex-1 flex flex-col min-w-0 bg-navy">
                <ChatWindow />

                {/* Inline flight results */}
                {rankedFlights.length > 0 && (
                    <div className="px-4 pb-3 border-t border-border-subtle pt-3">
                        <div className="flex items-center gap-2 mb-3">
                            <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">Top Flights</span>
                            <button onClick={() => setShowPanel(true)}
                                className="text-xs text-primary-light hover:text-white transition-colors font-medium">
                                View Details &rarr;
                            </button>
                        </div>
                        <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
                            {rankedFlights.slice(0, 3).map((f, i) => (
                                <div key={i} className="min-w-[300px] flex-shrink-0">
                                    <FlightCard flight={f} compact />
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Risk warnings */}
                {riskWarnings.filter(w => w.severity === 'red').length > 0 && (
                    <div className="px-4 pb-3 space-y-2">
                        {riskWarnings.filter(w => w.severity === 'red').map((w, i) => (
                            <RiskWarningBanner key={i} warning={w} />
                        ))}
                    </div>
                )}

                <ChatInput onSend={handleSend} disabled={isTyping} />
            </div>

            {/* Panel toggle */}
            <button onClick={() => setShowPanel(!showPanel)}
                className="hidden lg:flex items-center justify-center w-7 border-l border-border-subtle text-slate-600 hover:text-primary-light hover:bg-surface transition-all">
                {showPanel ? <PanelRightClose size={14} /> : <PanelRightOpen size={14} />}
            </button>

            {/* Trip Plan Panel */}
            <AnimatePresence>
                {showPanel && (
                    <motion.div initial={{ width: 0 }} animate={{ width: 420 }} exit={{ width: 0 }}
                        transition={{ type: 'spring', damping: 25, stiffness: 250 }}
                        className="overflow-hidden flex-shrink-0">
                        <div className="w-[420px] h-full">
                            <TripPlanPanel onClose={() => setShowPanel(false)} />
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    )
}
