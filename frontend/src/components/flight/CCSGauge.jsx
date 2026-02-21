import React from 'react'
import ScoreGauge from '../ui/ScoreGauge'
export default function CCSGauge({ score }) {
    return <ScoreGauge score={Math.round((score || 0) * 100)} size={100} label="Convenience Score" />
}
