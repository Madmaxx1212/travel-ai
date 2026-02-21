import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import LandingPage from './pages/LandingPage'
import ChatPage from './pages/ChatPage'
import TripDashboard from './pages/TripDashboard'
import LoginPage from './pages/LoginPage'

export default function App() {
    return (
        <div className="min-h-screen bg-navy text-gray-100">
            <Navbar />
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/dashboard" element={<TripDashboard />} />
                <Route path="/login" element={<LoginPage />} />
            </Routes>
        </div>
    )
}
