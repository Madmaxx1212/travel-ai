import React, { useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Plane, Sparkles } from 'lucide-react'
import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'
import useStore from '../../store/useStore'

const suggestions = [
    'Mumbai to Delhi this weekend',
    'Budget flights to Goa',
    '3-day Jaipur trip',
    'Best time to visit Leh',
]

export default function ChatWindow() {
    const { messages, isTyping } = useStore()
    const bottomRef = useRef(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages, isTyping])

    return (
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4 dot-grid">
            {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-center">
                    {/* Animated orb behind icon */}
                    <div className="relative mb-6">
                        <div className="absolute inset-0 w-20 h-20 rounded-3xl bg-primary/10 blur-2xl animate-pulse-glow" />
                        <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                            className="relative w-20 h-20 rounded-3xl bg-gradient-to-br from-primary/20 to-cyan/10 ring-1 ring-border-subtle flex items-center justify-center">
                            <Plane size={32} className="text-primary-light" />
                        </motion.div>
                    </div>

                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
                        <h3 className="font-display text-xl font-semibold text-white mb-2">Plan your perfect trip</h3>
                        <p className="text-sm text-slate-400 max-w-sm leading-relaxed">
                            Tell me where you'd like to go, and I'll find the best flights, hotels, and create a personalised itinerary.
                        </p>
                    </motion.div>

                    {/* Suggestion chips */}
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
                        className="flex flex-wrap justify-center gap-2 mt-8">
                        {suggestions.map((s, i) => (
                            <motion.button key={i}
                                initial={{ opacity: 0, y: 8 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.6 + i * 0.08 }}
                                className="px-4 py-2 rounded-full glass text-xs text-slate-400 hover:text-white hover:border-primary/30 transition-all flex items-center gap-1.5">
                                <Sparkles size={10} className="text-primary-light" /> {s}
                            </motion.button>
                        ))}
                    </motion.div>
                </div>
            )}

            {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
            ))}
            {isTyping && <TypingIndicator />}
            <div ref={bottomRef} />
        </div>
    )
}
