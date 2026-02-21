import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Plane, Mail, Lock, User } from 'lucide-react'
import { login, register } from '../lib/api'
import useStore from '../store/useStore'

export default function LoginPage() {
    const navigate = useNavigate()
    const { setUser } = useStore()
    const [isRegister, setIsRegister] = useState(false)
    const [form, setForm] = useState({ username: '', email: '', password: '' })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            const res = isRegister
                ? await register(form)
                : await login({ email: form.email, password: form.password })
            setUser(res.data, res.data.access_token)
            navigate('/chat')
        } catch (err) {
            setError(err.response?.data?.detail || 'Something went wrong')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center px-4 pt-14"
            style={{ background: 'linear-gradient(135deg, #0A0F1E 0%, #1E1B4B 50%, #0A0F1E 100%)' }}>
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
                <div className="text-center mb-8">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center mx-auto mb-4">
                        <Plane size={24} className="text-white" />
                    </div>
                    <h1 className="text-2xl font-bold text-white">{isRegister ? 'Create Account' : 'Welcome Back'}</h1>
                    <p className="text-sm text-gray-400 mt-1">Sign in to save your trip plans</p>
                </div>

                <form onSubmit={handleSubmit} className="glass rounded-2xl p-6 space-y-4">
                    {isRegister && (
                        <div>
                            <label className="text-xs text-gray-400 mb-1 block">Username</label>
                            <div className="flex items-center gap-2 bg-card rounded-lg px-3 py-2 border border-border/50 focus-within:border-primary/50">
                                <User size={14} className="text-gray-500" />
                                <input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })}
                                    className="flex-1 bg-transparent text-sm text-white outline-none" placeholder="Your username" />
                            </div>
                        </div>
                    )}
                    <div>
                        <label className="text-xs text-gray-400 mb-1 block">Email</label>
                        <div className="flex items-center gap-2 bg-card rounded-lg px-3 py-2 border border-border/50 focus-within:border-primary/50">
                            <Mail size={14} className="text-gray-500" />
                            <input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
                                type="email" className="flex-1 bg-transparent text-sm text-white outline-none" placeholder="you@example.com" />
                        </div>
                    </div>
                    <div>
                        <label className="text-xs text-gray-400 mb-1 block">Password</label>
                        <div className="flex items-center gap-2 bg-card rounded-lg px-3 py-2 border border-border/50 focus-within:border-primary/50">
                            <Lock size={14} className="text-gray-500" />
                            <input value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
                                type="password" className="flex-1 bg-transparent text-sm text-white outline-none" placeholder="••••••••" />
                        </div>
                    </div>

                    {error && <div className="text-xs text-red-400 bg-red-500/10 rounded-lg px-3 py-2">{error}</div>}

                    <button type="submit" disabled={loading}
                        className="w-full py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold text-sm disabled:opacity-50 hover:shadow-lg hover:shadow-primary/25 transition-all">
                        {loading ? 'Please wait...' : isRegister ? 'Create Account' : 'Sign In'}
                    </button>

                    <p className="text-center text-xs text-gray-400">
                        {isRegister ? 'Already have an account?' : "Don't have an account?"}
                        <button type="button" onClick={() => { setIsRegister(!isRegister); setError('') }}
                            className="ml-1 text-primary hover:underline">{isRegister ? 'Sign In' : 'Register'}</button>
                    </p>

                    <button type="button" onClick={() => navigate('/chat')}
                        className="w-full py-2 text-xs text-gray-500 hover:text-gray-300 transition-colors">
                        Continue as Guest →
                    </button>
                </form>
            </motion.div>
        </div>
    )
}
