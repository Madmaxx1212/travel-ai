import React from 'react'
import { clsx } from 'clsx'

const variants = {
    default: 'bg-gray-700 text-gray-300',
    primary: 'bg-primary/20 text-primary',
    success: 'bg-accent/20 text-accent',
    warning: 'bg-warning/20 text-warning',
    danger: 'bg-danger/20 text-danger',
    low: 'bg-green-500/20 text-green-400',
    medium: 'bg-yellow-500/20 text-yellow-400',
    high: 'bg-orange-500/20 text-orange-400',
    very_high: 'bg-red-500/20 text-red-400',
}

export default function Badge({ children, variant = 'default', className = '' }) {
    return (
        <span className={clsx('inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', variants[variant] || variants.default, className)}>
            {children}
        </span>
    )
}
