import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Plane, Moon, Sun, Plus } from 'lucide-react'
import useStore from '../../store/useStore'

export default function Navbar() {
    const { darkMode, toggleDarkMode, newTrip } = useStore()
    const location = useLocation()

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-border/50">
            <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
                <Link to="/" className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                        <Plane size={18} className="text-white" />
                    </div>
                    <span className="font-bold text-lg gradient-text hidden sm:inline">AI Travel Guardian+</span>
                </Link>

                <div className="flex items-center gap-3">
                    {location.pathname === '/chat' && (
                        <button onClick={newTrip} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-card hover:bg-border/50 text-sm text-gray-300 transition-colors">
                            <Plus size={14} /> New Trip
                        </button>
                    )}
                    <div className="flex items-center gap-1 text-xs text-gray-400">
                        <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
                        Active
                    </div>
                    <button onClick={toggleDarkMode} className="p-2 rounded-lg hover:bg-card transition-colors text-gray-400">
                        {darkMode ? <Sun size={16} /> : <Moon size={16} />}
                    </button>
                </div>
            </div>
        </nav>
    )
}
