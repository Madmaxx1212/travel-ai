import React, { useRef, useEffect } from 'react'
import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'
import useStore from '../../store/useStore'

export default function ChatWindow() {
    const { messages, isTyping } = useStore()
    const bottomRef = useRef(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages, isTyping])

    return (
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
            {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-center">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center mb-4">
                        <span className="text-3xl">✈️</span>
                    </div>
                    <h3 className="text-lg font-semibold text-white mb-1">Plan your perfect trip</h3>
                    <p className="text-sm text-gray-400 max-w-sm">Tell me where you'd like to go, and I'll find the best flights, hotels, and create a personalised itinerary.</p>
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
