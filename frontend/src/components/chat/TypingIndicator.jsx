import React from 'react'
import { motion } from 'framer-motion'
import { Bot } from 'lucide-react'

export default function TypingIndicator() {
    return (
        <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex gap-3"
        >
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-surface-elevated to-surface-card ring-1 ring-border-subtle flex items-center justify-center flex-shrink-0">
                <Bot size={14} className="text-primary-light" />
            </div>
            <div className="glass-card rounded-2xl rounded-tl-sm px-5 py-3.5 border-l-2 border-l-primary/30">
                <div className="flex items-center gap-2">
                    <div className="flex gap-1">
                        {[0, 1, 2].map(i => (
                            <div key={i}
                                className="w-1.5 h-1.5 rounded-full bg-primary-light animate-bounce-dot"
                                style={{ animationDelay: `${i * 0.16}s` }} />
                        ))}
                    </div>
                    <span className="text-xs text-slate-500 ml-1">AI is thinking...</span>
                </div>
            </div>
        </motion.div>
    )
}
