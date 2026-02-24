import React from 'react'
import { motion } from 'framer-motion'
import { Bot, User, Copy, Check } from 'lucide-react'

export default function MessageBubble({ message }) {
    const [copied, setCopied] = React.useState(false)
    const isUser = message.role === 'user'

    const handleCopy = () => {
        navigator.clipboard.writeText(message.content)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 12, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
            className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'} group`}
        >
            {/* Avatar */}
            <div className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 ${isUser
                    ? 'bg-gradient-to-br from-primary to-primary-dark shadow-glow-sm'
                    : 'bg-gradient-to-br from-surface-elevated to-surface-card ring-1 ring-border-subtle'
                }`}>
                {isUser
                    ? <User size={14} className="text-white" />
                    : <Bot size={14} className="text-primary-light" />
                }
            </div>

            {/* Bubble */}
            <div className={`relative max-w-[75%] px-4 py-3 rounded-2xl ${isUser
                ? 'bg-gradient-to-br from-primary to-primary-dark text-white rounded-tr-sm shadow-glow-sm'
                : 'glass-card rounded-tl-sm border-l-2 border-l-primary/30'
                }`}>
                <div className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</div>
                <div className={`flex items-center gap-2 mt-1.5 ${isUser ? 'justify-end' : 'justify-start'}`}>
                    <span className="text-[10px] opacity-40">
                        {message.timestamp ? new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
                    </span>
                </div>

                {!isUser && (
                    <button onClick={handleCopy}
                        className="absolute top-2.5 right-2.5 opacity-0 group-hover:opacity-100 transition-all duration-300 p-1.5 rounded-lg hover:bg-white/5">
                        {copied
                            ? <Check size={12} className="text-accent" />
                            : <Copy size={12} className="text-slate-500" />
                        }
                    </button>
                )}
            </div>
        </motion.div>
    )
}
