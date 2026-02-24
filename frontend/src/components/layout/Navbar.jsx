import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Plane, Plus, Sparkles } from 'lucide-react'
import useStore from '../../store/useStore'

export default function Navbar() {
    const { newTrip } = useStore()
    const location = useLocation()

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 glass-nav">
            <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                <Link to="/" className="flex items-center gap-3 group">
                    <div className="relative w-9 h-9 rounded-xl bg-gradient-to-br from-primary via-primary/80 to-cyan flex items-center justify-center shadow-glow-sm group-hover:shadow-glow transition-shadow duration-500">
                        <Plane size={18} className="text-white" />
                        <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary to-cyan opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                        <Plane size={18} className="text-white absolute" />
                    </div>
                    <div className="hidden sm:block">
                        <span className="font-display font-bold text-lg gradient-text">AI Travel Guardian</span>
                        <span className="font-display font-bold text-lg text-primary-light">+</span>
                    </div>
                </Link>

                <div className="flex items-center gap-3">
                    {location.pathname === '/chat' && (
                        <button onClick={newTrip}
                            className="flex items-center gap-2 px-4 py-2 rounded-xl glass-card text-sm text-slate-300 hover:text-white transition-all group">
                            <Plus size={14} className="group-hover:rotate-90 transition-transform duration-300" />
                            <span className="hidden sm:inline">New Trip</span>
                        </button>
                    )}

                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full glass text-xs">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                        </span>
                        <span className="text-emerald-400 font-medium">Active</span>
                    </div>

                    <Link to="/login"
                        className="hidden sm:flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-primary to-primary-dark text-white text-sm font-medium hover:shadow-glow transition-shadow duration-300">
                        <Sparkles size={14} />
                        Sign In
                    </Link>
                </div>
            </div>
        </nav>
    )
}
