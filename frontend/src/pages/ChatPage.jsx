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
                addMessage({ role: 'assistant', content: `⚠️ ${err || 'Something went wrong. Please try again.'}` })
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

    // Send initial message from landing page
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
        <div className="flex h-[calc(100vh-56px)] mt-14">
            {/* Chat section */}
            <div className="flex-1 flex flex-col min-w-0">
                <ChatWindow />

                {/* Inline flight results */}
                {rankedFlights.length > 0 && (
                    <div className="px-4 pb-2">
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-xs font-medium text-gray-400">Top Flights</span>
                            <button onClick={() => setShowPanel(true)} className="text-xs text-primary hover:underline">View Details →</button>
                        </div>
                        <div className="flex gap-3 overflow-x-auto pb-2">
                            {rankedFlights.slice(0, 3).map((f, i) => (
                                <div key={i} className="min-w-[280px]"><FlightCard flight={f} compact /></div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Risk warnings */}
                {riskWarnings.filter(w => w.severity === 'red').length > 0 && (
                    <div className="px-4 pb-2 space-y-1">
                        {riskWarnings.filter(w => w.severity === 'red').map((w, i) => (
                            <RiskWarningBanner key={i} warning={w} />
                        ))}
                    </div>
                )}

                <ChatInput onSend={handleSend} disabled={isTyping} />
            </div>

            {/* Panel toggle */}
            <button onClick={() => setShowPanel(!showPanel)}
                className="hidden lg:flex items-center justify-center w-6 border-l border-border/30 text-gray-500 hover:text-white hover:bg-card transition-colors">
                {showPanel ? <PanelRightClose size={14} /> : <PanelRightOpen size={14} />}
            </button>

            {/* Trip Plan Panel */}
            <AnimatePresence>
                {showPanel && (
                    <motion.div initial={{ width: 0 }} animate={{ width: 400 }} exit={{ width: 0 }}
                        className="overflow-hidden flex-shrink-0">
                        <div className="w-[400px] h-full">
                            <TripPlanPanel onClose={() => setShowPanel(false)} />
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    )
}
