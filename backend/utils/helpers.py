"""
AI Travel Guardian+ — Utility Helpers
Date parsing, city normalization, IATA code mapping, Indian holidays.
"""

from datetime import datetime, date
from typing import Optional
import re

# City name → IATA code mapping for Indian cities
CITY_TO_IATA = {
    "mumbai": "BOM", "bombay": "BOM", "delhi": "DEL", "new delhi": "DEL",
    "bangalore": "BLR", "bengaluru": "BLR", "hyderabad": "HYD",
    "chennai": "MAA", "madras": "MAA", "kolkata": "CCU", "calcutta": "CCU",
    "ahmedabad": "AMD", "goa": "GOI", "jaipur": "JAI", "pune": "PNQ",
    "lucknow": "LKO", "kochi": "COK", "cochin": "COK",
    "thiruvananthapuram": "TRV", "trivandrum": "TRV",
    "varanasi": "VNS", "amritsar": "ATQ", "chandigarh": "IXC",
    "indore": "IDR", "bhopal": "BHO", "patna": "PAT",
    "srinagar": "SXR", "leh": "IXL", "udaipur": "UDR",
    "jodhpur": "JDH", "coimbatore": "CJB",
}

IATA_TO_CITY = {v: k.title() for k, v in CITY_TO_IATA.items() if len(k) > 3}
# Override with canonical names
IATA_TO_CITY.update({
    "BOM": "Mumbai", "DEL": "Delhi", "BLR": "Bangalore",
    "HYD": "Hyderabad", "MAA": "Chennai", "CCU": "Kolkata",
    "AMD": "Ahmedabad", "GOI": "Goa", "JAI": "Jaipur",
    "PNQ": "Pune", "LKO": "Lucknow", "COK": "Kochi",
})

# Indian public holidays (month, day) for delay prediction
INDIAN_HOLIDAYS = [
    (1, 26),   # Republic Day
    (3, 29),   # Holi (approx)
    (4, 14),   # Ambedkar Jayanti
    (5, 1),    # May Day
    (8, 15),   # Independence Day
    (10, 2),   # Gandhi Jayanti
    (10, 24),  # Dussehra (approx)
    (11, 1),   # Diwali (approx)
    (11, 12),  # Diwali (approx second day)
    (12, 25),  # Christmas
    (1, 1),    # New Year
    (4, 10),   # Eid (approx)
    (6, 17),   # Eid al-Adha (approx)
]


def normalize_city(city_input: str) -> tuple[str, str]:
    """
    Normalize a city name or IATA code to (city_name, iata_code).
    Returns (city_name, iata_code) tuple.
    """
    if not city_input:
        return ("", "")

    cleaned = city_input.strip().lower()

    # Check if it's already an IATA code (3 uppercase letters)
    if len(cleaned) == 3 and cleaned.upper() in IATA_TO_CITY:
        iata = cleaned.upper()
        return (IATA_TO_CITY[iata], iata)

    # Look up city name
    if cleaned in CITY_TO_IATA:
        iata = CITY_TO_IATA[cleaned]
        return (IATA_TO_CITY.get(iata, city_input.title()), iata)

    # Partial match
    for city_name, iata in CITY_TO_IATA.items():
        if cleaned in city_name or city_name in cleaned:
            return (IATA_TO_CITY.get(iata, city_name.title()), iata)

    # Return as-is if no match found
    return (city_input.title(), city_input.upper()[:3])


def parse_date(date_str: str) -> Optional[str]:
    """
    Parse various date formats to YYYY-MM-DD string.
    Handles: "March 15", "15/03/2025", "2025-03-15", "this weekend", etc.
    """
    if not date_str:
        return None

    date_str = date_str.strip().lower()

    # Handle relative dates
    today = date.today()
    if "today" in date_str:
        return today.isoformat()
    if "tomorrow" in date_str:
        from datetime import timedelta
        return (today + timedelta(days=1)).isoformat()
    if "this weekend" in date_str:
        from datetime import timedelta
        days_until_saturday = (5 - today.weekday()) % 7
        if days_until_saturday == 0:
            days_until_saturday = 7
        return (today + timedelta(days=days_until_saturday)).isoformat()
    if "next week" in date_str:
        from datetime import timedelta
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        return (today + timedelta(days=days_until_monday)).isoformat()

    # Try standard formats
    formats = [
        "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y",
        "%B %d", "%B %d, %Y", "%b %d", "%b %d, %Y",
        "%d %B", "%d %B %Y", "%d %b", "%d %b %Y",
    ]
    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str, fmt)
            # If year is 1900 (no year in format), use current/next year
            if parsed.year == 1900:
                parsed = parsed.replace(year=today.year)
                if parsed.date() < today:
                    parsed = parsed.replace(year=today.year + 1)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def is_indian_holiday(month: int, day: int) -> bool:
    """Check if a date falls on an Indian public holiday."""
    return (month, day) in INDIAN_HOLIDAYS


def format_price_inr(price: float) -> str:
    """Format a price in Indian Rupees with comma separation."""
    if price >= 100000:
        return f"₹{price / 100000:.1f}L"
    elif price >= 1000:
        return f"₹{price:,.0f}"
    return f"₹{price:.0f}"


def calculate_duration_mins(dep_time: str, arr_time: str) -> int:
    """Calculate flight duration in minutes from departure and arrival times."""
    try:
        dep = datetime.strptime(dep_time, "%H:%M")
        arr = datetime.strptime(arr_time, "%H:%M")
        diff = (arr - dep).total_seconds() / 60
        if diff <= 0:
            diff += 1440  # Add 24 hours for overnight flights
        return int(diff)
    except (ValueError, TypeError):
        return 0


def generate_session_id() -> str:
    """Generate a unique session ID."""
    import uuid
    return str(uuid.uuid4())
