import React, { useEffect, useState } from 'react'

export default function CCSGauge({ score = 0, size = 120, label = 'Convenience Score' }) {
    const [animatedScore, setAnimatedScore] = useState(0)
    const maxScore = 100
    const normalised = Math.min(Math.round(score * 100), maxScore)
    const radius = (size - 14) / 2
    const circumference = 2 * Math.PI * radius
    const progress = (animatedScore / maxScore) * circumference

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

    const getGradientId = () => `ccs-grad-${size}`
    const getGlowId = () => `ccs-glow-${size}`

    return (
        <div className="flex flex-col items-center relative">
            <svg width={size} height={size} className="transform -rotate-90">
                <defs>
                    <linearGradient id={getGradientId()} x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor={animatedScore < 40 ? '#f43f5e' : animatedScore < 60 ? '#f59e0b' : '#6366f1'} />
                        <stop offset="100%" stopColor={animatedScore < 40 ? '#f59e0b' : animatedScore < 60 ? '#10b981' : '#10b981'} />
                    </linearGradient>
                    <filter id={getGlowId()}>
                        <feGaussianBlur stdDeviation="3" result="blur" />
                        <feMerge>
                            <feMergeNode in="blur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>
                {/* Background track */}
                <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
                    stroke="rgba(99,102,241,0.08)" strokeWidth="8" />
                {/* Progress arc */}
                <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
                    stroke={`url(#${getGradientId()})`} strokeWidth="8"
                    strokeDasharray={circumference} strokeDashoffset={circumference - progress}
                    strokeLinecap="round" filter={`url(#${getGlowId()})`}
                    className="transition-all duration-300" />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-display text-2xl font-bold text-white">{animatedScore}</span>
                <span className="text-[9px] text-slate-500 uppercase tracking-wider">/ 100</span>
            </div>
            <span className="text-[10px] text-slate-500 mt-1.5">{label}</span>
        </div>
    )
}
