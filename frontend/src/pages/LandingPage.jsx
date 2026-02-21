import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Plane, Brain, Map, Shield, Search, ChevronRight } from 'lucide-react'

const features = [
    { icon: Brain, label: 'XGBoost Delay Prediction', color: 'from-blue-500 to-cyan-400' },
    { icon: Shield, label: 'Groq LLM Powered', color: 'from-green-500 to-emerald-400' },
    { icon: Map, label: '7-Agent AI System', color: 'from-purple-500 to-pink-400' },
    { icon: Plane, label: 'Real-time Risk Warnings', color: 'from-orange-500 to-red-400' },
]

const steps = [
    { num: '01', title: 'Tell us your trip', desc: 'Share your destination, dates, and preferences in natural language.', icon: '💬' },
    { num: '02', title: 'AI analyses 50K+ data points', desc: 'Our ML models predict delays, analyse reviews, and score flights.', icon: '🧠' },
    { num: '03', title: 'Get your perfect plan', desc: 'Best flights, hotels, day-wise itinerary — all personalised for you.', icon: '✈️' },
]

export default function LandingPage() {
    const navigate = useNavigate()
    const [from, setFrom] = useState('')
    const [to, setTo] = useState('')
    const [date, setDate] = useState('')

    const handleSearch = () => {
        const query = `${from ? 'from ' + from : ''} ${to ? 'to ' + to : ''} ${date ? 'on ' + date : ''}`.trim()
        navigate('/chat', { state: { initialMessage: query || null } })
    }

    return (
        <div className="min-h-screen overflow-hidden">
            {/* Particles background */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                {[...Array(20)].map((_, i) => (
                    <div key={i} className="particle" style={{
                        left: `${Math.random() * 100}%`, top: `${Math.random() * 100}%`,
                        animationDelay: `${Math.random() * 4}s`, animationDuration: `${3 + Math.random() * 3}s`,
                        width: `${2 + Math.random() * 4}px`, height: `${2 + Math.random() * 4}px`,
                    }} />
                ))}
            </div>

            {/* Hero Section */}
            <section className="relative min-h-screen flex flex-col items-center justify-center px-4"
                style={{ background: 'linear-gradient(135deg, #0A0F1E 0%, #1E1B4B 50%, #0A0F1E 100%)' }}>
                <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}
                    className="text-center max-w-3xl mx-auto">
                    <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold mb-6">
                        <span className="gradient-text">AI-Powered</span>
                        <br />Travel Planning
                    </h1>
                    <p className="text-lg text-gray-400 mb-10 max-w-xl mx-auto">
                        Flight delay prediction · Real ML intelligence · End-to-end trip planning
                    </p>

                    {/* Search Bar */}
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
                        className="glass rounded-2xl p-2 max-w-2xl mx-auto mb-8">
                        <div className="flex flex-col sm:flex-row gap-2">
                            <input value={from} onChange={(e) => setFrom(e.target.value)} placeholder="From city"
                                className="flex-1 bg-card rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 outline-none focus:ring-1 focus:ring-primary/50" />
                            <input value={to} onChange={(e) => setTo(e.target.value)} placeholder="To city"
                                className="flex-1 bg-card rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 outline-none focus:ring-1 focus:ring-primary/50" />
                            <input value={date} onChange={(e) => setDate(e.target.value)} placeholder="Travel date" type="date"
                                className="flex-1 bg-card rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 outline-none focus:ring-1 focus:ring-primary/50" />
                            <button onClick={handleSearch}
                                className="px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-accent text-white font-semibold text-sm flex items-center gap-2 hover:shadow-lg hover:shadow-primary/25 transition-all">
                                <Search size={16} /> Plan My Trip
                            </button>
                        </div>
                    </motion.div>

                    {/* Feature Pills */}
                    <div className="flex flex-wrap justify-center gap-3">
                        {features.map((f, i) => (
                            <motion.div key={i} initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 0.5 + i * 0.1 }}
                                className="flex items-center gap-2 px-4 py-2 rounded-full glass text-xs text-gray-300">
                                <f.icon size={14} className="text-primary" /> {f.label}
                            </motion.div>
                        ))}
                    </div>
                </motion.div>

                {/* Quick Start Suggestions */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1 }}
                    className="mt-12 flex flex-wrap justify-center gap-3">
                    {['Mumbai → Delhi weekend trip', 'Cheap Goa flights', '5-day Jaipur itinerary'].map((q, i) => (
                        <button key={i} onClick={() => navigate('/chat', { state: { initialMessage: q } })}
                            className="px-4 py-2 rounded-full border border-border/50 text-xs text-gray-400 hover:text-white hover:border-primary/50 transition-all flex items-center gap-1">
                            {q} <ChevronRight size={12} />
                        </button>
                    ))}
                </motion.div>
            </section>

            {/* How It Works */}
            <section className="py-24 px-4 bg-navy-light">
                <div className="max-w-4xl mx-auto">
                    <h2 className="text-3xl font-bold text-center mb-16 gradient-text">How It Works</h2>
                    <div className="grid md:grid-cols-3 gap-8">
                        {steps.map((step, i) => (
                            <motion.div key={i} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }} transition={{ delay: i * 0.15 }}
                                className="glass rounded-2xl p-6 text-center hover:border-primary/30 transition-all">
                                <div className="text-4xl mb-4">{step.icon}</div>
                                <div className="text-xs text-primary font-mono mb-2">{step.num}</div>
                                <h3 className="text-lg font-semibold text-white mb-2">{step.title}</h3>
                                <p className="text-sm text-gray-400">{step.desc}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Tech Strip */}
            <section className="py-12 px-4 border-t border-border/30">
                <div className="max-w-4xl mx-auto">
                    <div className="flex flex-wrap justify-center gap-6 text-xs text-gray-500">
                        {['FastAPI', 'XGBoost', 'LangGraph', 'FAISS', 'Groq LLM', 'SHAP', 'React', 'SQLite', 'VADER NLP'].map((tech) => (
                            <span key={tech} className="px-3 py-1.5 rounded-full border border-border/30 hover:text-primary hover:border-primary/30 transition-colors cursor-default">
                                {tech}
                            </span>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-8 px-4 border-t border-border/30 text-center">
                <p className="text-xs text-gray-500">AI Travel Guardian+ — MSc Big Data Analytics Final Year Project</p>
                <p className="text-xs text-gray-600 mt-1">Powered by XGBoost · Groq LLM · LangGraph · FAISS</p>
            </footer>
        </div>
    )
}
