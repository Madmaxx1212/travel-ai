import React from 'react'
import { motion } from 'framer-motion'
import { AlertTriangle, AlertCircle, Info, X } from 'lucide-react'

const icons = { red: AlertTriangle, amber: AlertCircle, blue: Info }
const styles = {
    red: 'border-l-red-500 bg-red-500/10',
    amber: 'border-l-yellow-500 bg-yellow-500/10',
    blue: 'border-l-blue-400 bg-blue-400/10',
}

export default function RiskWarningBanner({ warning, onDismiss }) {
    const Icon = icons[warning.severity] || Info
    return (
        <motion.div initial={{ x: -20, opacity: 0 }} animate={{ x: 0, opacity: 1 }}
            className={`border-l-4 rounded-r-lg p-3 flex items-start gap-3 ${styles[warning.severity] || styles.blue}`}>
            <Icon size={16} className={`flex-shrink-0 mt-0.5 ${warning.severity === 'red' ? 'text-red-400' : warning.severity === 'amber' ? 'text-yellow-400' : 'text-blue-400'}`} />
            <div className="flex-1">
                <div className="text-xs font-semibold text-white capitalize">{warning.warning_type} Warning</div>
                <div className="text-xs text-gray-300 mt-0.5">{warning.message}</div>
            </div>
            {onDismiss && (
                <button onClick={onDismiss} className="text-gray-500 hover:text-white"><X size={14} /></button>
            )}
        </motion.div>
    )
}
