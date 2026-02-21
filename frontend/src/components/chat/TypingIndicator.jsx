import React from 'react'

export default function TypingIndicator() {
    return (
        <div className="flex items-center gap-1.5 px-4 py-2">
            <div className="w-2 h-2 rounded-full bg-primary animate-bounce-dot" style={{ animationDelay: '0s' }} />
            <div className="w-2 h-2 rounded-full bg-primary animate-bounce-dot" style={{ animationDelay: '0.16s' }} />
            <div className="w-2 h-2 rounded-full bg-primary animate-bounce-dot" style={{ animationDelay: '0.32s' }} />
        </div>
    )
}
