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
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'} group`}
        >
            <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${isUser ? 'bg-primary' : 'bg-gradient-to-br from-primary/50 to-accent/50'}`}>
                {isUser ? <User size={14} className="text-white" /> : <Bot size={14} className="text-white" />}
            </div>

            <div className={`relative max-w-[75%] px-4 py-3 rounded-2xl ${isUser
                ? 'bg-primary text-white rounded-br-sm'
                : 'glass rounded-bl-sm'
                }`}>
                <div className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</div>
                <div className={`flex items-center gap-2 mt-1 ${isUser ? 'justify-end' : 'justify-start'}`}>
                    <span className="text-[10px] opacity-50">
                        {message.timestamp ? new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}
                    </span>
                </div>

                {!isUser && (
                    <button onClick={handleCopy} className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded hover:bg-white/10">
                        {copied ? <Check size={12} className="text-accent" /> : <Copy size={12} className="text-gray-400" />}
                    </button>
                )}
            </div>
        </motion.div>
    )
}
