import React, { useState } from 'react'
import { Send, Sparkles } from 'lucide-react'

export default function ChatInput({ onSend, disabled }) {
    const [message, setMessage] = useState('')
    const [focused, setFocused] = useState(false)

    const handleSend = () => {
        if (!message.trim() || disabled) return
        onSend(message.trim())
        setMessage('')
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() }
    }

    return (
        <div className="p-4 border-t border-border-subtle bg-navy/50 backdrop-blur-xl">
            <div className={`flex items-center gap-3 rounded-2xl px-5 py-3 transition-all duration-500
                ${focused
                    ? 'bg-surface-card ring-1 ring-primary/30 shadow-glow-sm'
                    : 'bg-surface-card/70 ring-1 ring-border-subtle'
                }`}>
                <Sparkles size={16} className={`flex-shrink-0 transition-colors duration-300 ${focused ? 'text-primary-light' : 'text-slate-600'}`} />
                <input
                    type="text" value={message} onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown} disabled={disabled}
                    onFocus={() => setFocused(true)} onBlur={() => setFocused(false)}
                    placeholder="Plan your trip... (e.g. Mumbai to Delhi this weekend)"
                    className="flex-1 bg-transparent text-sm text-white placeholder-slate-500 outline-none"
                />
                <button onClick={handleSend} disabled={!message.trim() || disabled}
                    className={`w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-300 flex-shrink-0
                        ${message.trim() && !disabled
                            ? 'bg-gradient-to-r from-primary to-primary-dark text-white shadow-glow-sm hover:shadow-glow active:scale-95'
                            : 'bg-surface text-slate-600'
                        }`}>
                    <Send size={15} />
                </button>
            </div>
            <p className="text-[10px] text-slate-700 mt-1.5 text-center">Press Enter to send</p>
        </div>
    )
}
