import React from 'react'
export default function FlightComparison({ flights }) {
    if (!flights || flights.length === 0) return null
    return (
        <div className="overflow-x-auto">
            <table className="w-full text-xs">
                <thead>
                    <tr className="text-gray-400 border-b border-border/50">
                        <th className="py-2 text-left">Flight</th><th className="py-2">Price</th>
                        <th className="py-2">Delay Risk</th><th className="py-2">CCS</th><th className="py-2">Duration</th>
                    </tr>
                </thead>
                <tbody>
                    {flights.slice(0, 3).map((f, i) => (
                        <tr key={i} className={`border-b border-border/30 ${i === 0 ? 'text-accent' : 'text-gray-300'}`}>
                            <td className="py-2 font-medium">{f.airline} {f.flight_number}</td>
                            <td className="py-2 text-center">₹{(f.price || 0).toLocaleString()}</td>
                            <td className="py-2 text-center">{Math.round((f.delay_probability || 0) * 100)}%</td>
                            <td className="py-2 text-center">{Math.round((f.ccs_score || 0) * 100)}</td>
                            <td className="py-2 text-center">{f.duration_mins}m</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}
