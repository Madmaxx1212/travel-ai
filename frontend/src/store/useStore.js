import { create } from 'zustand'

const useStore = create((set, get) => ({
    // Session
    sessionId: localStorage.getItem('sessionId') || crypto.randomUUID(),
    tripPlanId: null,
    darkMode: true,

    // Chat
    messages: [],
    isTyping: false,

    // Trip data
    tripPlan: null,
    rankedFlights: [],
    recommendedFlight: null,
    riskWarnings: [],
    recommendedHotels: [],
    itinerary: null,
    foodRecommendations: [],

    // Auth
    user: null,
    token: localStorage.getItem('token') || null,

    // Actions
    setSessionId: (id) => {
        localStorage.setItem('sessionId', id)
        set({ sessionId: id })
    },

    addMessage: (msg) => set((s) => ({ messages: [...s.messages, { id: Date.now(), timestamp: new Date(), ...msg }] })),

    setIsTyping: (v) => set({ isTyping: v }),

    clearMessages: () => set({ messages: [], tripPlanId: null, tripPlan: null, rankedFlights: [], recommendedFlight: null, riskWarnings: [], recommendedHotels: [], itinerary: null, foodRecommendations: [] }),

    setFlightResults: (data) => set({ rankedFlights: data }),
    setRecommendedFlight: (f) => set({ recommendedFlight: f }),
    setRiskWarnings: (w) => set({ riskWarnings: w }),

    setTripPlan: (plan) => set({
        tripPlan: plan,
        recommendedHotels: plan?.recommended_hotels || [],
        itinerary: plan?.itinerary || null,
        foodRecommendations: plan?.food_recommendations || [],
    }),

    setTripPlanId: (id) => set({ tripPlanId: id }),

    setUser: (user, token) => {
        localStorage.setItem('token', token)
        set({ user, token })
    },

    logout: () => {
        localStorage.removeItem('token')
        set({ user: null, token: null })
    },

    toggleDarkMode: () => set((s) => ({ darkMode: !s.darkMode })),

    newTrip: () => {
        const newId = crypto.randomUUID()
        localStorage.setItem('sessionId', newId)
        set({
            sessionId: newId,
            messages: [],
            tripPlanId: null,
            tripPlan: null,
            rankedFlights: [],
            recommendedFlight: null,
            riskWarnings: [],
            recommendedHotels: [],
            itinerary: null,
            foodRecommendations: [],
        })
    },
}))

export default useStore
