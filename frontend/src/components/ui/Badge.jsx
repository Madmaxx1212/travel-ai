import React from 'react'
import { clsx } from 'clsx'

const variants = {
    default: 'bg-surface-elevated text-slate-400 ring-1 ring-border-subtle',
    primary: 'bg-primary/10 text-primary-light ring-1 ring-primary/20',
    success: 'bg-emerald-500/10 text-emerald-400 ring-1 ring-emerald-500/20',
    warning: 'bg-amber-500/10 text-amber-400 ring-1 ring-amber-500/20',
    danger: 'bg-rose-500/10 text-rose-400 ring-1 ring-rose-500/20',
    low: 'bg-emerald-500/10 text-emerald-400 ring-1 ring-emerald-500/20',
    medium: 'bg-amber-500/10 text-amber-400 ring-1 ring-amber-500/20',
    high: 'bg-orange-500/10 text-orange-400 ring-1 ring-orange-500/20',
    very_high: 'bg-rose-500/10 text-rose-400 ring-1 ring-rose-500/20',
}

export default function Badge({ children, variant = 'default', className = '' }) {
    return (
        <span className={clsx(
            'inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-medium',
            variants[variant] || variants.default,
            className
        )}>
            {children}
        </span>
    )
}
