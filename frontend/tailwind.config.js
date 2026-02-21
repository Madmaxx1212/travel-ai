/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,jsx}'],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: { DEFAULT: '#3B82F6', dark: '#2563EB', light: '#60A5FA' },
                accent: { DEFAULT: '#10B981', dark: '#059669', light: '#34D399' },
                warning: { DEFAULT: '#F59E0B', dark: '#D97706' },
                danger: { DEFAULT: '#EF4444', dark: '#DC2626' },
                navy: { DEFAULT: '#0A0F1E', light: '#111827' },
                card: '#1E2535',
                border: '#2D3748',
            },
            fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
            animation: {
                'float': 'float 6s ease-in-out infinite',
                'pulse-slow': 'pulse 3s ease-in-out infinite',
                'bounce-dot': 'bounceDot 1.4s infinite ease-in-out both',
            },
            keyframes: {
                float: { '0%, 100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-20px)' } },
                bounceDot: { '0%, 80%, 100%': { transform: 'scale(0)' }, '40%': { transform: 'scale(1)' } },
            },
        },
    },
    plugins: [],
}
