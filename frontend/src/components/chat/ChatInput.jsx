import React, { useState } from 'react'
import { Send } from 'lucide-react'

export default function ChatInput({ onSend, disabled }) {
    const [message, setMessage] = useState('')

    const handleSend = () => {
        if (!message.trim() || disabled) return
        onSend(message.trim())
        setMessage('')
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() }
    }

    return (
        <div className="p-4 border-t border-border/50">
            <div className="flex items-center gap-2 bg-card rounded-full px-4 py-2 border border-border/50 focus-within:border-primary/50 transition-colors">
                <input
                    type="text" value={message} onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown} disabled={disabled}
                    placeholder="Plan your trip... (e.g. Mumbai to Delhi this weekend)"
                    className="flex-1 bg-transparent text-sm text-white placeholder-gray-500 outline-none"
                />
                {message.length > 200 && <span className="text-[10px] text-gray-500">{message.length}</span>}
                <button onClick={handleSend} disabled={!message.trim() || disabled}
                    className="w-8 h-8 rounded-full bg-gradient-to-r from-primary to-accent flex items-center justify-center disabled:opacity-30 transition-opacity hover:shadow-lg hover:shadow-primary/25">
                    <Send size={14} className="text-white" />
                </button>
            </div>
            <p className="text-[10px] text-gray-600 mt-1 text-center">Press Enter to send</p>
        </div>
    )
}
