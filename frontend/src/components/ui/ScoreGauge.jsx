import React, { useEffect, useState } from 'react'

export default function ScoreGauge({ score = 0, size = 120, label = 'Score', maxScore = 100 }) {
    const [animatedScore, setAnimatedScore] = useState(0)
    const normalised = Math.min(score, maxScore)
    const radius = (size - 14) / 2
    const circumference = 2 * Math.PI * radius
    const progress = (animatedScore / maxScore) * circumference
    const gradId = `sg-grad-${size}-${label}`
    const glowId = `sg-glow-${size}-${label}`

    useEffect(() => {
        let frame
        const duration = 1400
        const start = performance.now()
        const animate = (now) => {
            const elapsed = now - start
            const pct = Math.min(elapsed / duration, 1)
            const eased = 1 - Math.pow(1 - pct, 4)
            setAnimatedScore(Math.round(normalised * eased))
            if (pct < 1) frame = requestAnimationFrame(animate)
        }
        frame = requestAnimationFrame(animate)
        return () => cancelAnimationFrame(frame)
    }, [normalised])

    return (
        <div className="flex flex-col items-center relative">
            <svg width={size} height={size} className="transform -rotate-90">
                <defs>
                    <linearGradient id={gradId} x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor={animatedScore < 40 ? '#f43f5e' : '#6366f1'} />
                        <stop offset="100%" stopColor={animatedScore < 40 ? '#f59e0b' : '#10b981'} />
                    </linearGradient>
                    <filter id={glowId}>
                        <feGaussianBlur stdDeviation="3" result="blur" />
                        <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                    </filter>
                </defs>
                <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="rgba(99,102,241,0.08)" strokeWidth="8" />
                <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
                    stroke={`url(#${gradId})`} strokeWidth="8"
                    strokeDasharray={circumference} strokeDashoffset={circumference - progress}
                    strokeLinecap="round" filter={`url(#${glowId})`}
                    className="transition-all duration-300" />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center" style={{ width: size, height: size }}>
                <span className="font-display text-2xl font-bold text-white">{animatedScore}</span>
            </div>
            <span className="text-[10px] text-slate-500 mt-1">{label}</span>
        </div>
    )
}
