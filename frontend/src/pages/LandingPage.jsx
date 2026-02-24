import React, { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Search, ChevronRight, ArrowRight, Sparkles, Shield, Brain, Plane, Map, BarChart3, Zap, Globe } from 'lucide-react'

/* ── Indian cities for autocomplete ── */
const CITIES = [
    { name: 'Mumbai', code: 'BOM', state: 'Maharashtra' },
    { name: 'Delhi', code: 'DEL', state: 'Delhi' },
    { name: 'Bangalore', code: 'BLR', state: 'Karnataka' },
    { name: 'Hyderabad', code: 'HYD', state: 'Telangana' },
    { name: 'Chennai', code: 'MAA', state: 'Tamil Nadu' },
    { name: 'Kolkata', code: 'CCU', state: 'West Bengal' },
    { name: 'Ahmedabad', code: 'AMD', state: 'Gujarat' },
    { name: 'Goa', code: 'GOI', state: 'Goa' },
    { name: 'Jaipur', code: 'JAI', state: 'Rajasthan' },
    { name: 'Pune', code: 'PNQ', state: 'Maharashtra' },
    { name: 'Lucknow', code: 'LKO', state: 'Uttar Pradesh' },
    { name: 'Kochi', code: 'COK', state: 'Kerala' },
    { name: 'Varanasi', code: 'VNS', state: 'Uttar Pradesh' },
    { name: 'Amritsar', code: 'ATQ', state: 'Punjab' },
    { name: 'Chandigarh', code: 'IXC', state: 'Chandigarh' },
    { name: 'Indore', code: 'IDR', state: 'Madhya Pradesh' },
    { name: 'Bhopal', code: 'BHO', state: 'Madhya Pradesh' },
    { name: 'Patna', code: 'PAT', state: 'Bihar' },
    { name: 'Srinagar', code: 'SXR', state: 'J&K' },
    { name: 'Leh', code: 'IXL', state: 'Ladakh' },
    { name: 'Udaipur', code: 'UDR', state: 'Rajasthan' },
    { name: 'Jodhpur', code: 'JDH', state: 'Rajasthan' },
    { name: 'Coimbatore', code: 'CJB', state: 'Tamil Nadu' },
    { name: 'Thiruvananthapuram', code: 'TRV', state: 'Kerala' },
]

function CityInput({ value, onChange, placeholder, cities = CITIES }) {
    const [focused, setFocused] = useState(false)
    const [activeIdx, setActiveIdx] = useState(-1)
    const ref = useRef(null)
    const dropdownRef = useRef(null)

    const filtered = value.length > 0
        ? cities.filter(c =>
            c.name.toLowerCase().startsWith(value.toLowerCase()) ||
            c.code.toLowerCase().startsWith(value.toLowerCase()) ||
            c.state.toLowerCase().startsWith(value.toLowerCase())
        ).slice(0, 6)
        : []

    const showDropdown = focused && filtered.length > 0

    useEffect(() => { setActiveIdx(-1) }, [value])

    useEffect(() => {
        const handler = (e) => {
            if (ref.current && !ref.current.contains(e.target)) setFocused(false)
        }
        document.addEventListener('mousedown', handler)
        return () => document.removeEventListener('mousedown', handler)
    }, [])

    const handleKeyDown = (e) => {
        if (!showDropdown) return
        if (e.key === 'ArrowDown') { e.preventDefault(); setActiveIdx(i => Math.min(i + 1, filtered.length - 1)) }
        if (e.key === 'ArrowUp') { e.preventDefault(); setActiveIdx(i => Math.max(i - 1, 0)) }
        if (e.key === 'Enter' && activeIdx >= 0) { e.preventDefault(); onChange(filtered[activeIdx].name); setFocused(false) }
        if (e.key === 'Escape') setFocused(false)
    }

    return (
        <div ref={ref} className="relative flex-1">
            <input value={value} onChange={(e) => onChange(e.target.value)}
                onFocus={() => setFocused(true)}
                onKeyDown={handleKeyDown}
                placeholder={placeholder}
                className="w-full bg-surface-card/80 rounded-xl px-4 py-3.5 text-sm text-white placeholder-slate-500 outline-none ring-1 ring-border-subtle focus:ring-primary/40 transition-all duration-300" />

            {showDropdown && (
                <div ref={dropdownRef}
                    className="absolute top-full left-0 right-0 mt-2 rounded-xl autocomplete-dropdown overflow-hidden z-50 animate-slide-up">
                    {filtered.map((city, i) => (
                        <button key={city.code}
                            onMouseDown={(e) => { e.preventDefault(); onChange(city.name); setFocused(false) }}
                            className={`autocomplete-item w-full flex items-center gap-3 px-4 py-3 text-left ${i === activeIdx ? 'active' : ''}`}>
                            <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                                <Globe size={14} className="text-primary-light" />
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="text-sm text-white font-medium">{city.name}</div>
                                <div className="text-xs text-slate-500">{city.code} &middot; {city.state}</div>
                            </div>
                            <span className="text-[10px] text-slate-600 font-mono">{city.code}</span>
                        </button>
                    ))}
                </div>
            )}
        </div>
    )
}

/* ── Data ── */
const features = [
    { icon: BarChart3, label: 'XGBoost Delay Prediction', desc: 'ML-powered flight analysis' },
    { icon: Zap, label: 'Groq LLM Intelligence', desc: 'Ultra-fast AI responses' },
    { icon: Brain, label: '7-Agent AI System', desc: 'Multi-agent orchestration' },
    { icon: Shield, label: 'Real-time Risk Alerts', desc: 'Smart safety warnings' },
]

const steps = [
    { num: '01', title: 'Describe your trip', desc: 'Share your destination, dates, budget, and preferences in natural language.', icon: Search, color: 'from-primary to-cyan' },
    { num: '02', title: 'AI analyses everything', desc: 'Our 7-agent system predicts delays, scores flights, and finds the best options.', icon: Brain, color: 'from-cyan to-accent' },
    { num: '03', title: 'Get your perfect plan', desc: 'Ranked flights, hotels, full itinerary, and food recommendations -- personalised.', icon: Map, color: 'from-accent to-primary' },
]

const stats = [
    { value: '50K+', label: 'Data Points Analysed' },
    { value: '7', label: 'AI Agents Working' },
    { value: '<2s', label: 'Prediction Speed' },
    { value: '95%', label: 'Accuracy Rate' },
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
            {/* ── Hero Section ── */}
            <section className="relative min-h-screen flex flex-col items-center justify-center px-4 mesh-bg">
                {/* Floating orbs */}
                <div className="orb orb-blue w-[500px] h-[500px] -top-40 -left-40 animate-float-slow" />
                <div className="orb orb-emerald w-[400px] h-[400px] -bottom-20 -right-20 animate-float-slower" />
                <div className="orb orb-cyan w-[300px] h-[300px] top-1/3 right-1/4 animate-float" />

                <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
                    className="relative text-center max-w-4xl mx-auto z-10">

                    {/* Tagline pill */}
                    <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2 }}
                        className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass text-xs text-slate-400 mb-8">
                        <Sparkles size={12} className="text-primary-light" />
                        Powered by XGBoost + Groq LLM + 7 AI Agents
                    </motion.div>

                    <h1 className="font-display text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-extrabold leading-[0.95] tracking-tight mb-6">
                        <span className="gradient-text">Intelligent</span>
                        <br />
                        <span className="text-white">Travel Planning</span>
                    </h1>

                    <p className="text-base sm:text-lg text-slate-400 mb-12 max-w-xl mx-auto leading-relaxed">
                        Flight delay prediction &middot; Real-time risk analysis &middot; Personalised trip plans &mdash; all powered by machine learning.
                    </p>

                    {/* ── Search Bar ── */}
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4, duration: 0.8 }}
                        className="glass-card rounded-2xl p-2 max-w-2xl mx-auto mb-10 gradient-border">
                        <div className="flex flex-col sm:flex-row gap-2">
                            <CityInput value={from} onChange={setFrom} placeholder="From city" />
                            <CityInput value={to} onChange={setTo} placeholder="To city" />
                            <input value={date} onChange={(e) => setDate(e.target.value)} placeholder="Travel date" type="date"
                                className="flex-1 bg-surface-card/80 rounded-xl px-4 py-3.5 text-sm text-white placeholder-slate-500 outline-none ring-1 ring-border-subtle focus:ring-primary/40 transition-all duration-300" />
                            <button onClick={handleSearch}
                                className="px-8 py-3.5 rounded-xl bg-gradient-to-r from-primary to-primary-dark text-white font-semibold text-sm flex items-center justify-center gap-2 hover:shadow-glow transition-all duration-300 active:scale-[0.98]">
                                <Search size={16} /> Plan My Trip
                            </button>
                        </div>
                    </motion.div>

                    {/* ── Feature Pills ── */}
                    <div className="flex flex-wrap justify-center gap-3">
                        {features.map((f, i) => (
                            <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.6 + i * 0.1 }}
                                className="group flex items-center gap-2.5 px-4 py-2.5 rounded-full glass-card text-xs cursor-default">
                                <div className="w-6 h-6 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                                    <f.icon size={12} className="text-primary-light" />
                                </div>
                                <span className="text-slate-300 group-hover:text-white transition-colors">{f.label}</span>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>

                {/* Quick Start */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 }}
                    className="relative mt-16 flex flex-wrap justify-center gap-3 z-10">
                    {['Mumbai to Delhi weekend', 'Budget Goa flights', '5-day Jaipur trip'].map((q, i) => (
                        <button key={i} onClick={() => navigate('/chat', { state: { initialMessage: q } })}
                            className="px-5 py-2.5 rounded-full glass text-xs text-slate-400 hover:text-white hover:border-primary/30 transition-all flex items-center gap-1.5 group">
                            {q} <ArrowRight size={12} className="group-hover:translate-x-0.5 transition-transform" />
                        </button>
                    ))}
                </motion.div>

                {/* Scroll indicator */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.5 }}
                    className="absolute bottom-8 left-1/2 -translate-x-1/2">
                    <div className="w-5 h-8 rounded-full border border-slate-700 flex justify-center pt-1.5">
                        <motion.div animate={{ y: [0, 8, 0] }} transition={{ duration: 1.5, repeat: Infinity }}
                            className="w-1 h-1 rounded-full bg-primary-light" />
                    </div>
                </motion.div>
            </section>

            {/* ── Stats Strip ── */}
            <section className="py-8 border-y border-border-subtle bg-surface/50">
                <div className="max-w-5xl mx-auto flex justify-around">
                    {stats.map((s, i) => (
                        <motion.div key={i} initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }} transition={{ delay: i * 0.1 }}
                            className="text-center">
                            <div className="font-display text-2xl sm:text-3xl font-bold gradient-text">{s.value}</div>
                            <div className="text-xs text-slate-500 mt-1">{s.label}</div>
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* ── How It Works ── */}
            <section className="py-24 px-4 dot-grid relative">
                <div className="orb orb-blue w-[300px] h-[300px] top-20 -left-20" />
                <div className="max-w-5xl mx-auto relative z-10">
                    <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }} className="text-center mb-16">
                        <h2 className="font-display text-3xl sm:text-4xl font-bold text-white mb-4">How It Works</h2>
                        <p className="text-slate-400 text-sm max-w-md mx-auto">Three simple steps to your perfect trip, powered by cutting-edge AI.</p>
                    </motion.div>

                    <div className="grid md:grid-cols-3 gap-6">
                        {steps.map((step, i) => (
                            <motion.div key={i} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }} transition={{ delay: i * 0.15 }}
                                className="glass-card rounded-2xl p-8 text-center group">
                                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center mx-auto mb-5 shadow-glow-sm group-hover:shadow-glow transition-shadow duration-500`}>
                                    <step.icon size={24} className="text-white" />
                                </div>
                                <div className="text-xs text-primary font-mono font-medium mb-3 tracking-widest">{step.num}</div>
                                <h3 className="font-display text-lg font-semibold text-white mb-2">{step.title}</h3>
                                <p className="text-sm text-slate-400 leading-relaxed">{step.desc}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── Tech Strip ── */}
            <section className="py-14 px-4 border-t border-border-subtle">
                <div className="max-w-5xl mx-auto">
                    <p className="text-center text-xs text-slate-600 mb-6 uppercase tracking-widest">Built With</p>
                    <div className="flex flex-wrap justify-center gap-3">
                        {['FastAPI', 'XGBoost', 'LangGraph', 'FAISS', 'Groq LLM', 'SHAP', 'React', 'Sentence-BERT', 'VADER NLP'].map((tech) => (
                            <span key={tech}
                                className="px-4 py-2 rounded-full glass text-xs text-slate-500 hover:text-primary-light hover:border-primary/20 transition-all duration-300 cursor-default">
                                {tech}
                            </span>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── Footer ── */}
            <footer className="py-10 px-4 border-t border-border-subtle text-center">
                <p className="text-xs text-slate-600">AI Travel Guardian+ -- MSc Big Data Analytics Final Year Project</p>
                <p className="text-[10px] text-slate-700 mt-1">Powered by XGBoost &middot; Groq LLM &middot; LangGraph &middot; FAISS</p>
            </footer>
        </div>
    )
}
