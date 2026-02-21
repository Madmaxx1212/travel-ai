import React, { useEffect, useState } from 'react'

export default function ScoreGauge({ score = 0, size = 120, label = 'Score', maxScore = 100 }) {
    const [animatedScore, setAnimatedScore] = useState(0)
    const normalised = Math.min(score, maxScore)
    const radius = (size - 12) / 2
    const circumference = 2 * Math.PI * radius
    const progress = (animatedScore / maxScore) * circumference

    useEffect(() => {
        let frame
        const duration = 1200
        const start = performance.now()
        const animate = (now) => {
            const elapsed = now - start
            const pct = Math.min(elapsed / duration, 1)
            const eased = 1 - Math.pow(1 - pct, 3)
            setAnimatedScore(Math.round(normalised * eased))
            if (pct < 1) frame = requestAnimationFrame(animate)
        }
        frame = requestAnimationFrame(animate)
        return () => cancelAnimationFrame(frame)
    }, [normalised])

    const getColor = (s) => {
        if (s < 40) return '#EF4444'
        if (s < 60) return '#F59E0B'
        if (s < 80) return '#10B981'
        return '#10B981'
    }

    return (
        <div className="flex flex-col items-center">
            <svg width={size} height={size} className="transform -rotate-90">
                <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#2D3748" strokeWidth="8" />
                <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke={getColor(animatedScore)} strokeWidth="8"
                    strokeDasharray={circumference} strokeDashoffset={circumference - progress}
                    strokeLinecap="round" className="transition-all duration-300" />
            </svg>
            <div className="absolute flex flex-col items-center justify-center" style={{ width: size, height: size }}>
                <span className="text-2xl font-bold text-white">{animatedScore}</span>
            </div>
            <span className="text-xs text-gray-400 mt-1">{label}</span>
        </div>
    )
}
