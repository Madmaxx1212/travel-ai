import React from 'react'
import Badge from '../ui/Badge'

export default function DelayRiskBadge({ probability, riskLevel }) {
    const pct = Math.round((probability || 0) * 100)
    const variant = riskLevel === 'low' ? 'low' : riskLevel === 'medium' ? 'medium' : riskLevel === 'high' ? 'high' : 'very_high'
    return <Badge variant={variant}>⏱ {pct}% delay risk ({riskLevel})</Badge>
}
