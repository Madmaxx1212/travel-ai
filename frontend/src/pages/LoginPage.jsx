import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Plane, Mail, Lock, User, ArrowRight } from 'lucide-react'
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
        <div className="min-h-screen flex items-center justify-center px-4 pt-16 mesh-bg relative">
            <div className="orb orb-blue w-[400px] h-[400px] -top-20 -right-20" />
            <div className="orb orb-emerald w-[300px] h-[300px] bottom-0 -left-20" />

            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                className="w-full max-w-md relative z-10">

                <div className="text-center mb-8">
                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary to-cyan flex items-center justify-center mx-auto mb-5 shadow-glow-sm">
                        <Plane size={24} className="text-white" />
                    </div>
                    <h1 className="font-display text-2xl font-bold text-white">{isRegister ? 'Create Account' : 'Welcome Back'}</h1>
                    <p className="text-sm text-slate-400 mt-1.5">Sign in to save your trip plans</p>
                </div>

                <form onSubmit={handleSubmit} className="glass-card rounded-2xl p-7 space-y-5">
                    {isRegister && (
                        <div>
                            <label className="text-xs text-slate-500 mb-1.5 block font-medium">Username</label>
                            <div className="flex items-center gap-2.5 bg-surface rounded-xl px-4 py-3 ring-1 ring-border-subtle focus-within:ring-primary/40 transition-all">
                                <User size={14} className="text-slate-600" />
                                <input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })}
                                    className="flex-1 bg-transparent text-sm text-white outline-none" placeholder="Your username" />
                            </div>
                        </div>
                    )}
                    <div>
                        <label className="text-xs text-slate-500 mb-1.5 block font-medium">Email</label>
                        <div className="flex items-center gap-2.5 bg-surface rounded-xl px-4 py-3 ring-1 ring-border-subtle focus-within:ring-primary/40 transition-all">
                            <Mail size={14} className="text-slate-600" />
                            <input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
                                type="email" className="flex-1 bg-transparent text-sm text-white outline-none" placeholder="you@example.com" />
                        </div>
                    </div>
                    <div>
                        <label className="text-xs text-slate-500 mb-1.5 block font-medium">Password</label>
                        <div className="flex items-center gap-2.5 bg-surface rounded-xl px-4 py-3 ring-1 ring-border-subtle focus-within:ring-primary/40 transition-all">
                            <Lock size={14} className="text-slate-600" />
                            <input value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
                                type="password" className="flex-1 bg-transparent text-sm text-white outline-none" placeholder="--------" />
                        </div>
                    </div>

                    {error && <div className="text-xs text-rose-400 bg-rose-500/10 rounded-xl px-4 py-2.5 ring-1 ring-rose-500/20">{error}</div>}

                    <button type="submit" disabled={loading}
                        className="w-full py-3.5 rounded-xl bg-gradient-to-r from-primary to-primary-dark text-white font-semibold text-sm disabled:opacity-50 hover:shadow-glow transition-all duration-300 flex items-center justify-center gap-2">
                        {loading ? 'Please wait...' : isRegister ? 'Create Account' : 'Sign In'}
                        {!loading && <ArrowRight size={14} />}
                    </button>

                    <p className="text-center text-xs text-slate-400">
                        {isRegister ? 'Already have an account?' : "Don't have an account?"}
                        <button type="button" onClick={() => { setIsRegister(!isRegister); setError('') }}
                            className="ml-1 text-primary-light hover:text-white transition-colors font-medium">
                            {isRegister ? 'Sign In' : 'Register'}
                        </button>
                    </p>

                    <button type="button" onClick={() => navigate('/chat')}
                        className="w-full py-2.5 text-xs text-slate-500 hover:text-slate-300 transition-colors flex items-center justify-center gap-1">
                        Continue as Guest <ArrowRight size={10} />
                    </button>
                </form>
            </motion.div>
        </div>
    )
}
