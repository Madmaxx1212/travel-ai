"""
AI Travel Guardian+ — Seed Data Generator
Populates SQLite database with realistic Indian domestic flight, hotel, and review data.
Also generates CSV/JSON files in the data/ directory.
"""

import os
import sys
import csv
import json
import random
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.database import engine, SessionLocal, Base
from database.models import Flight, Hotel, AirlineReview

random.seed(42)

# ── Flight Route Definitions ─────────────────────────────────

AIRLINES = {
    "Vistara": {"code": "UK", "sentiment": 0.87, "aircraft": ["A320neo", "B737-800", "A321neo"]},
    "IndiGo": {"code": "6E", "sentiment": 0.74, "aircraft": ["A320neo", "A321neo", "ATR72"]},
    "Air India": {"code": "AI", "sentiment": 0.65, "aircraft": ["A320neo", "B787-8", "B777-300ER"]},
    "SpiceJet": {"code": "SG", "sentiment": 0.61, "aircraft": ["B737-800", "B737 MAX 8", "Q400"]},
    "GoFirst": {"code": "G8", "sentiment": 0.58, "aircraft": ["A320neo", "A320"]},
    "AirAsia India": {"code": "I5", "sentiment": 0.69, "aircraft": ["A320neo", "A320"]},
}

ROUTES = [
    {"source": "BOM", "destination": "DEL", "base_price": 4500, "duration_range": (125, 155), "source_city": "Mumbai", "dest_city": "Delhi"},
    {"source": "DEL", "destination": "BOM", "base_price": 4500, "duration_range": (130, 160), "source_city": "Delhi", "dest_city": "Mumbai"},
    {"source": "BOM", "destination": "BLR", "base_price": 3800, "duration_range": (100, 125), "source_city": "Mumbai", "dest_city": "Bangalore"},
    {"source": "BLR", "destination": "BOM", "base_price": 3800, "duration_range": (105, 130), "source_city": "Bangalore", "dest_city": "Mumbai"},
    {"source": "DEL", "destination": "BLR", "base_price": 4200, "duration_range": (150, 175), "source_city": "Delhi", "dest_city": "Bangalore"},
    {"source": "BLR", "destination": "DEL", "base_price": 4200, "duration_range": (155, 180), "source_city": "Bangalore", "dest_city": "Delhi"},
    {"source": "BOM", "destination": "AMD", "base_price": 2800, "duration_range": (70, 90), "source_city": "Mumbai", "dest_city": "Ahmedabad"},
    {"source": "AMD", "destination": "BOM", "base_price": 2800, "duration_range": (70, 90), "source_city": "Ahmedabad", "dest_city": "Mumbai"},
    {"source": "DEL", "destination": "CCU", "base_price": 4000, "duration_range": (135, 160), "source_city": "Delhi", "dest_city": "Kolkata"},
    {"source": "CCU", "destination": "DEL", "base_price": 4000, "duration_range": (140, 165), "source_city": "Kolkata", "dest_city": "Delhi"},
    {"source": "BOM", "destination": "HYD", "base_price": 3200, "duration_range": (85, 105), "source_city": "Mumbai", "dest_city": "Hyderabad"},
    {"source": "HYD", "destination": "BOM", "base_price": 3200, "duration_range": (90, 110), "source_city": "Hyderabad", "dest_city": "Mumbai"},
    {"source": "DEL", "destination": "MAA", "base_price": 4800, "duration_range": (165, 190), "source_city": "Delhi", "dest_city": "Chennai"},
    {"source": "MAA", "destination": "DEL", "base_price": 4800, "duration_range": (170, 195), "source_city": "Chennai", "dest_city": "Delhi"},
    {"source": "BLR", "destination": "HYD", "base_price": 2500, "duration_range": (65, 85), "source_city": "Bangalore", "dest_city": "Hyderabad"},
    {"source": "HYD", "destination": "BLR", "base_price": 2500, "duration_range": (65, 85), "source_city": "Hyderabad", "dest_city": "Bangalore"},
    {"source": "BOM", "destination": "GOI", "base_price": 2600, "duration_range": (60, 80), "source_city": "Mumbai", "dest_city": "Goa"},
    {"source": "GOI", "destination": "BOM", "base_price": 2600, "duration_range": (60, 80), "source_city": "Goa", "dest_city": "Mumbai"},
    {"source": "DEL", "destination": "JAI", "base_price": 2200, "duration_range": (55, 75), "source_city": "Delhi", "dest_city": "Jaipur"},
    {"source": "JAI", "destination": "DEL", "base_price": 2200, "duration_range": (55, 75), "source_city": "Jaipur", "dest_city": "Delhi"},
]

TIME_SLOTS = [
    {"dep": "06:00", "congestion": 0.35, "delay_base": 0.08},
    {"dep": "06:45", "congestion": 0.40, "delay_base": 0.09},
    {"dep": "08:30", "congestion": 0.55, "delay_base": 0.12},
    {"dep": "09:15", "congestion": 0.50, "delay_base": 0.10},
    {"dep": "11:45", "congestion": 0.60, "delay_base": 0.15},
    {"dep": "14:00", "congestion": 0.55, "delay_base": 0.18},
    {"dep": "16:30", "congestion": 0.70, "delay_base": 0.22},
    {"dep": "17:15", "congestion": 0.72, "delay_base": 0.25},
    {"dep": "19:00", "congestion": 0.65, "delay_base": 0.28},
    {"dep": "21:30", "congestion": 0.45, "delay_base": 0.32},
    {"dep": "22:45", "congestion": 0.30, "delay_base": 0.35},
]


def calculate_arrival(dep_time_str: str, duration_mins: int) -> str:
    dep_h, dep_m = map(int, dep_time_str.split(":"))
    total_mins = dep_h * 60 + dep_m + duration_mins
    arr_h = (total_mins // 60) % 24
    arr_m = total_mins % 60
    return f"{arr_h:02d}:{arr_m:02d}"


def generate_flights():
    """Generate 500+ realistic flight records."""
    flights = []
    flight_id = 0

    for route in ROUTES:
        airlines_for_route = random.sample(list(AIRLINES.keys()), k=random.randint(4, 6))
        for airline_name in airlines_for_route:
            airline_info = AIRLINES[airline_name]
            num_slots = random.randint(2, 4)
            chosen_slots = random.sample(TIME_SLOTS, k=num_slots)

            for slot in chosen_slots:
                flight_id += 1
                flight_num = f"{airline_info['code']}-{random.randint(100, 999)}"
                duration = random.randint(*route["duration_range"])
                arr_time = calculate_arrival(slot["dep"], duration)

                # Price variation: ±30% from base, airline premium
                airline_premium = {"Vistara": 1.25, "IndiGo": 0.95, "Air India": 1.10,
                                   "SpiceJet": 0.82, "GoFirst": 0.78, "AirAsia India": 0.85}
                price = route["base_price"] * airline_premium.get(airline_name, 1.0)
                price *= random.uniform(0.80, 1.35)
                price = round(price, -1)  # Round to nearest 10

                # Delay and congestion with airline-specific modifiers
                delay_modifier = {"Vistara": 0.7, "IndiGo": 0.85, "Air India": 1.15,
                                  "SpiceJet": 1.35, "GoFirst": 1.45, "AirAsia India": 1.10}
                delay_rate = slot["delay_base"] * delay_modifier.get(airline_name, 1.0)
                delay_rate = min(max(delay_rate + random.uniform(-0.05, 0.05), 0.03), 0.55)
                delay_rate = round(delay_rate, 3)
                congestion = slot["congestion"] + random.uniform(-0.08, 0.08)
                congestion = round(min(max(congestion, 0.15), 0.90), 3)

                stops = 0
                if duration > 160 and random.random() < 0.25:
                    stops = 1
                    duration += random.randint(40, 70)

                for dow in range(7):
                    if random.random() < 0.6:  # Not every flight runs every day
                        for month in random.sample(range(1, 13), k=random.randint(6, 12)):
                            flights.append({
                                "flight_number": flight_num,
                                "airline": airline_name,
                                "source": route["source"],
                                "destination": route["destination"],
                                "departure_time": slot["dep"],
                                "arrival_time": arr_time,
                                "duration_mins": duration,
                                "price": price,
                                "aircraft_type": random.choice(airline_info["aircraft"]),
                                "stops": stops,
                                "day_of_week": dow,
                                "month": month,
                                "historical_delay_rate": delay_rate,
                                "historical_ontime_rate": round(1 - delay_rate, 3),
                                "airline_sentiment_score": airline_info["sentiment"],
                                "congestion_index": congestion,
                            })

    # Take a random sample if too many, or keep all if under threshold
    if len(flights) > 600:
        flights = random.sample(flights, 600)
    return flights


# ── Hotel Data ────────────────────────────────────────────────

HOTEL_DATA = {
    "Delhi": [
        ("The Imperial", "luxury", 12500, 4.8, "Janpath, Connaught Place", 28.6258, 77.2195, 0.5),
        ("The Oberoi", "luxury", 15000, 4.9, "Dr Zakir Hussain Marg", 28.5987, 77.2405, 1.2),
        ("ITC Maurya", "luxury", 11000, 4.7, "Diplomatic Enclave, Sardar Patel Marg", 28.5948, 77.1736, 3.5),
        ("Taj Palace", "luxury", 13000, 4.8, "2 Sardar Patel Marg, Chanakyapuri", 28.5910, 77.1780, 3.8),
        ("The Lalit", "luxury", 9500, 4.5, "Barakhamba Road, Connaught Place", 28.6316, 77.2308, 0.8),
        ("Radisson Blu", "medium", 5500, 4.2, "National Highway 8, Mahipalpur", 28.5524, 77.1002, 8.5),
        ("Lemon Tree Premier", "medium", 4800, 4.0, "Aerocity, New Delhi", 28.5567, 77.0965, 9.0),
        ("The Park", "medium", 6200, 4.3, "15 Parliament Street", 28.6211, 77.2136, 0.3),
        ("Holiday Inn", "medium", 4200, 3.9, "Plot 1 Asset Area 6, Aerocity", 28.5547, 77.0951, 9.2),
        ("Ibis New Delhi", "budget", 3200, 3.6, "Asset Area 6, Aerocity, New Delhi", 28.5540, 77.0940, 9.5),
        ("Hotel Godwin", "budget", 2200, 3.3, "8502 Arakashan Road, Ram Nagar", 28.6521, 77.2136, 2.5),
        ("Zostel Delhi", "budget", 800, 3.8, "5/81 Aram Nagar, Paharganj", 28.6448, 77.2092, 1.8),
        ("Bloom Rooms", "budget", 2800, 3.5, "7/26 Janakpuri District Centre", 28.6216, 77.0894, 7.0),
        ("FabHotel Prime", "budget", 1800, 3.4, "2494 Rajguru Road, Karol Bagh", 28.6503, 77.1906, 3.0),
    ],
    "Mumbai": [
        ("Taj Mahal Palace", "luxury", 18000, 4.9, "Apollo Bunder, Colaba", 18.9220, 72.8333, 2.0),
        ("The Oberoi Mumbai", "luxury", 16000, 4.8, "Nariman Point", 18.9253, 72.8230, 1.5),
        ("ITC Maratha", "luxury", 10500, 4.6, "Sahar, Andheri East", 19.0950, 72.8632, 12.0),
        ("Four Seasons", "luxury", 14000, 4.7, "114 Dr E Moses Road, Worli", 19.0117, 72.8168, 5.0),
        ("Trident Nariman Point", "medium", 7500, 4.4, "Nariman Point", 18.9257, 72.8230, 1.5),
        ("Hotel Marine Plaza", "medium", 5800, 4.1, "29 Marine Drive", 18.9377, 72.8257, 1.0),
        ("Fariyas Hotel", "medium", 4500, 3.9, "25 Arthur Bunder Road, Colaba", 18.9165, 72.8325, 2.5),
        ("Residency Hotel", "medium", 4000, 3.8, "26 Rustom Sidhwa Marg, Fort", 18.9335, 72.8367, 1.8),
        ("Hotel Suba Palace", "budget", 2800, 3.5, "211 A.K. Nayak Marg, Near Gateway", 18.9231, 72.8340, 2.0),
        ("Treebo Trend", "budget", 2200, 3.4, "Andheri East, Mumbai", 19.1075, 72.8710, 11.5),
        ("FabHotel Jubilee", "budget", 2000, 3.3, "Girgaon, Mumbai", 18.9527, 72.8156, 1.5),
        ("Backpacker Panda", "budget", 700, 3.7, "Colaba Causeway", 18.9193, 72.8325, 2.3),
    ],
    "Bangalore": [
        ("The Leela Palace", "luxury", 14000, 4.8, "23 HAL Airport Road", 12.9603, 77.6482, 6.0),
        ("ITC Gardenia", "luxury", 11500, 4.7, "1 Residency Road", 12.9716, 77.5963, 0.5),
        ("Taj West End", "luxury", 12000, 4.8, "25 Race Course Road", 12.9844, 77.5720, 2.0),
        ("JW Marriott", "luxury", 10000, 4.6, "24/1 Vittal Mallya Road", 12.9715, 77.5952, 0.6),
        ("Lemon Tree Premier", "medium", 4500, 4.0, "68 Cunningham Road", 12.9874, 77.5840, 1.5),
        ("Royal Orchid", "medium", 5200, 4.1, "1 Golf Avenue, Bellary Road", 13.0070, 77.5777, 3.0),
        ("The Paul", "medium", 6800, 4.3, "139 Residency Road", 12.9698, 77.5992, 0.3),
        ("Ibis Bangalore", "budget", 3000, 3.6, "26/1 Hosur Road, Bommanahalli", 12.9001, 77.6187, 7.0),
        ("Treebo Trend", "budget", 2400, 3.5, "Koramangala 5th Block", 12.9352, 77.6245, 4.5),
        ("Zostel Bangalore", "budget", 750, 3.8, "8 Church Street", 12.9742, 77.6040, 0.2),
        ("FabHotel Zuri", "budget", 2000, 3.4, "Indiranagar, Bangalore", 12.9784, 77.6408, 3.5),
    ],
    "Hyderabad": [
        ("Taj Falaknuma Palace", "luxury", 25000, 4.9, "Engine Bowli, Falaknuma", 17.3316, 78.4670, 7.0),
        ("ITC Kohenur", "luxury", 11000, 4.7, "HITEC City, Madhapur", 17.4401, 78.3760, 8.0),
        ("Park Hyatt", "luxury", 12000, 4.7, "Road No 2, Banjara Hills", 17.4263, 78.4388, 3.0),
        ("Novotel HICC", "medium", 5500, 4.2, "HITEC City, Madhapur", 17.4375, 78.3800, 8.5),
        ("Lemon Tree", "medium", 3800, 3.9, "Gachibowli, Hyderabad", 17.4361, 78.3413, 10.0),
        ("Hotel Minerva Grand", "medium", 4200, 4.0, "Secunderabad", 17.4399, 78.4983, 6.0),
        ("Treebo Royal", "budget", 2200, 3.5, "Abids, Hyderabad", 17.3908, 78.4753, 2.5),
        ("FabHotel Hallmark", "budget", 1800, 3.3, "Banjara Hills Road 12", 17.4215, 78.4420, 3.5),
        ("Zostel Hyderabad", "budget", 650, 3.7, "Begumpet, Hyderabad", 17.4440, 78.4711, 5.0),
    ],
    "Goa": [
        ("Taj Exotica", "luxury", 16000, 4.8, "Calwaddo, Benaulim, South Goa", 15.2552, 73.9236, 20.0),
        ("W Goa", "luxury", 18000, 4.7, "Vagator Beach, North Goa", 15.5979, 73.7346, 15.0),
        ("Park Hyatt Goa", "luxury", 14000, 4.7, "Arossim Beach, Cansaulim", 15.3210, 73.8910, 18.0),
        ("Novotel Goa Dona Sylvia", "medium", 6500, 4.2, "Cavelossim Beach, South Goa", 15.1742, 73.9403, 25.0),
        ("Lemon Tree Amarante", "medium", 4800, 4.0, "Candolim, North Goa", 15.5140, 73.7639, 12.0),
        ("Goa Marriott Resort", "medium", 7500, 4.3, "Miramar, Panaji", 15.4698, 73.8042, 3.0),
        ("Hotel Manvin's", "budget", 2200, 3.5, "Near Calangute Beach", 15.5438, 73.7558, 10.0),
        ("Zostel Goa", "budget", 550, 3.8, "Anjuna, North Goa", 15.5747, 73.7404, 13.0),
        ("OYO Baga Beach", "budget", 1500, 3.3, "Baga, North Goa", 15.5550, 73.7513, 11.0),
        ("The Hosteller Goa", "budget", 700, 3.6, "Vagator, North Goa", 15.5962, 73.7368, 15.0),
    ],
    "Jaipur": [
        ("Rambagh Palace", "luxury", 22000, 4.9, "Bhawani Singh Road", 26.8965, 75.8029, 3.0),
        ("Taj Jai Mahal Palace", "luxury", 12000, 4.7, "Jacob Road, Civil Lines", 26.9155, 75.7942, 2.0),
        ("ITC Rajputana", "luxury", 9000, 4.6, "Palace Road, Jaipur", 26.9124, 75.7867, 1.5),
        ("Holiday Inn", "medium", 4500, 4.0, "Amer Road, Jaipur", 26.9494, 75.8500, 5.0),
        ("Lemon Tree", "medium", 3800, 3.9, "Kukas, Delhi Road", 26.9750, 75.8342, 7.0),
        ("Hotel Pearl Palace", "medium", 3200, 4.4, "Hari Kishan Somani Marg, Hathroi", 26.9090, 75.7828, 1.0),
        ("Zostel Jaipur", "budget", 600, 3.8, "C-11 Sawai Jai Singh Highway", 26.9196, 75.7897, 1.5),
        ("Hotel Arya Niwas", "budget", 2000, 4.0, "Sansar Chandra Road", 26.9100, 75.7840, 1.2),
        ("Moustache Hostel", "budget", 500, 3.7, "Near Hawa Mahal", 26.9239, 75.8267, 1.0),
    ],
    "Kolkata": [
        ("The Oberoi Grand", "luxury", 11000, 4.7, "15 Jawaharlal Nehru Road", 22.5666, 88.3497, 0.3),
        ("ITC Royal Bengal", "luxury", 10000, 4.6, "1 JBS Haldane Avenue", 22.5360, 88.3990, 4.0),
        ("Taj Bengal", "luxury", 9500, 4.6, "34B Belvedere Road, Alipore", 22.5278, 88.3363, 3.5),
        ("The Park Kolkata", "medium", 5500, 4.2, "17 Park Street", 22.5556, 88.3528, 0.5),
        ("Lemon Tree", "medium", 3800, 3.9, "Rajarhat, New Town", 22.5850, 88.4650, 9.0),
        ("Treebo Trend", "budget", 2200, 3.5, "Sudder Street, Park Street Area", 22.5547, 88.3509, 0.5),
        ("Hotel Lindsay", "budget", 1800, 3.3, "8A/1 Lindsay Street", 22.5630, 88.3503, 0.2),
    ],
    "Ahmedabad": [
        ("ITC Narmada", "luxury", 9000, 4.5, "Vastrapur, Ahmedabad", 23.0308, 72.5277, 3.0),
        ("Hyatt Regency", "luxury", 8500, 4.4, "Ashram Road", 23.0241, 72.5704, 1.0),
        ("Courtyard by Marriott", "medium", 5000, 4.1, "Ramdev Nagar Cross Road", 23.0226, 72.5142, 4.0),
        ("Lemon Tree", "medium", 3500, 3.9, "Navrangpura", 23.0368, 72.5571, 1.5),
        ("Hotel Good Night", "budget", 1800, 3.4, "Khanpur, Ahmedabad", 23.0167, 72.5784, 1.0),
        ("Zostel Ahmedabad", "budget", 500, 3.7, "Near Sabarmati Ashram", 23.0606, 72.5802, 3.0),
    ],
    "Chennai": [
        ("ITC Grand Chola", "luxury", 12000, 4.8, "63 Mount Road, Guindy", 13.0103, 80.2209, 4.0),
        ("Taj Coromandel", "luxury", 10500, 4.7, "37 Mahatma Gandhi Road, Nungambakkam", 13.0607, 80.2440, 1.0),
        ("The Leela Palace", "luxury", 11000, 4.7, "Adyar Seaface, MRC Nagar", 13.0170, 80.2715, 3.5),
        ("Radisson Blu", "medium", 5500, 4.2, "531 GST Road, Pallavaram", 12.9650, 80.1860, 10.0),
        ("Fortune Select Grand", "medium", 4200, 4.0, "258 GST Road, Meenambakkam", 12.9798, 80.1735, 8.0),
        ("FabHotel Porur", "budget", 2200, 3.5, "Mount Poonamallee Road", 13.0350, 80.1631, 8.5),
        ("Zostel Chennai", "budget", 600, 3.7, "Mylapore, Chennai", 13.0340, 80.2691, 3.0),
        ("Treebo Trend", "budget", 2000, 3.4, "T. Nagar, Chennai", 13.0418, 80.2341, 2.0),
    ],
}

# ── Airline Review Templates ─────────────────────────────────

POSITIVE_REVIEWS = [
    "Excellent service on my {route} flight. The crew was very professional and the {aspect} was outstanding. Would definitely fly {airline} again.",
    "Smooth experience with {airline}. {aspect} exceeded my expectations. The flight from {source} to {dest} was comfortable and on time.",
    "I fly {airline} regularly on the {route} route. Always reliable, great {aspect}. One of the best domestic airlines in India.",
    "Really impressed with {airline}'s {aspect} on my recent trip. The boarding was quick and efficient. Highly recommended!",
    "Wonderful experience! {airline} never disappoints. The {aspect} was particularly noteworthy on this {route} journey.",
    "Had a fantastic flight with {airline}. Clean aircraft, friendly crew, and the {aspect} was top-notch. 10/10!",
    "As a frequent flyer, {airline} consistently delivers. The {route} flight was smooth, {aspect} was great. Keep it up!",
    "Best domestic airline experience in India. {airline}'s {aspect} is unmatched. The {route} flight was perfect.",
]

NEGATIVE_REVIEWS = [
    "Disappointing experience with {airline} on the {route} route. The {aspect} was below average. Flight was delayed by 45 minutes.",
    "Not happy with {airline}. The {aspect} was poor and the flight from {source} to {dest} was delayed without proper communication.",
    "{airline} has gone downhill. My {route} flight was delayed, {aspect} was terrible. Looking for alternatives now.",
    "Avoid {airline} if you can. The {aspect} is consistently bad. My luggage was delayed on the {route} flight.",
    "Very disappointing {aspect} on my {airline} flight. The crew seemed disinterested and the aircraft was dirty.",
    "Paid a premium for {airline} but the {aspect} didn't justify the cost. Flight was late by over an hour.",
]

NEUTRAL_REVIEWS = [
    "Average experience with {airline} on the {route} route. The {aspect} was okay, nothing special. Flight was mostly on time.",
    "Decent flight with {airline}. {aspect} was acceptable. The {route} flight got the job done but no frills.",
    "Standard domestic airline experience. {airline}'s {aspect} is average compared to competitors. Not bad, not great.",
    "{airline} gets you from {source} to {dest} reliably enough. {aspect} is middling. Adequate for the price.",
]

ASPECTS = ["food quality", "leg room", "punctuality", "staff behaviour", "in-flight entertainment",
           "cleanliness", "boarding process", "baggage handling", "value for money", "seat comfort"]


def generate_reviews():
    """Generate 200+ airline reviews with realistic text."""
    reviews = []
    route_pairs = [("BOM", "DEL"), ("DEL", "BLR"), ("BOM", "BLR"),
                   ("DEL", "CCU"), ("BOM", "HYD"), ("BOM", "GOI")]

    for airline_name, info in AIRLINES.items():
        num_reviews = random.randint(30, 50)
        sentiment_base = info["sentiment"]

        for _ in range(num_reviews):
            route = random.choice(route_pairs)
            aspect = random.choice(ASPECTS)
            route_str = f"{route[0]}-{route[1]}"

            # Weight review sentiment by airline score
            rand = random.random()
            if rand < sentiment_base * 0.7:
                template = random.choice(POSITIVE_REVIEWS)
                sentiment = "positive"
                overall = round(random.uniform(3.5, 5.0), 1)
            elif rand < 0.85:
                template = random.choice(NEUTRAL_REVIEWS)
                sentiment = "neutral"
                overall = round(random.uniform(2.5, 3.5), 1)
            else:
                template = random.choice(NEGATIVE_REVIEWS)
                sentiment = "negative"
                overall = round(random.uniform(1.0, 2.5), 1)

            text = template.format(
                airline=airline_name, route=route_str,
                aspect=aspect, source=route[0], dest=route[1]
            )

            # Generate aspect scores
            noise = lambda base, spread=0.15: round(min(max(base + random.uniform(-spread, spread), 0.1), 1.0), 2)
            base_score = overall / 5.0

            reviews.append({
                "airline": airline_name,
                "review_text": text,
                "overall_rating": overall,
                "punctuality_score": noise(base_score),
                "staff_score": noise(base_score),
                "comfort_score": noise(base_score),
                "value_score": noise(base_score),
                "food_score": noise(base_score, 0.20),
                "sentiment_label": sentiment,
                "source": "kaggle",
            })

    return reviews


def seed_database():
    """Main seed function: creates tables and populates with data."""
    print("[START] AI Travel Guardian+ -- Seeding Database...")

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("[OK] Tables created")

    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Flight).count() > 0:
            print("[SKIP] Database already seeded. Skipping.")
            return

        # ── Flights ──
        flights_data = generate_flights()
        print(f"[INFO] Generated {len(flights_data)} flight records")

        for fd in flights_data:
            db.add(Flight(**fd))
        db.commit()
        print(f"[OK] Inserted {len(flights_data)} flights")

        # ── Hotels ──
        hotel_count = 0
        for city, hotels in HOTEL_DATA.items():
            for h in hotels:
                hotel = Hotel(
                    name=h[0], city=city, budget_tier=h[1],
                    price_per_night=h[2], rating=h[3], address=h[4],
                    latitude=h[5], longitude=h[6], distance_centre_km=h[7],
                    review_count=random.randint(50, 2000),
                    amenities=json.dumps(random.sample(
                        ["wifi", "pool", "gym", "spa", "restaurant", "bar",
                         "parking", "room_service", "laundry", "airport_shuttle",
                         "business_centre", "concierge", "breakfast_included"],
                        k=random.randint(4, 9)
                    )),
                    safety_score=round(random.uniform(0.65, 0.98), 2),
                )
                db.add(hotel)
                hotel_count += 1
        db.commit()
        print(f"[OK] Inserted {hotel_count} hotels")

        # ── Reviews ──
        reviews_data = generate_reviews()
        for rd in reviews_data:
            db.add(AirlineReview(**rd))
        db.commit()
        print(f"[OK] Inserted {len(reviews_data)} airline reviews")

        # ── Export to CSV ──
        data_dir = Path(__file__).resolve().parent.parent.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        # Flights CSV
        with open(data_dir / "sample_flights.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=flights_data[0].keys())
            writer.writeheader()
            writer.writerows(flights_data)
        print(f"[OK] Exported {data_dir / 'sample_flights.csv'}")

        # Hotels CSV
        hotels_flat = []
        for city, hotels in HOTEL_DATA.items():
            for h in hotels:
                hotels_flat.append({
                    "name": h[0], "city": city, "budget_tier": h[1],
                    "price_per_night": h[2], "rating": h[3], "address": h[4],
                    "latitude": h[5], "longitude": h[6], "distance_centre_km": h[7],
                })
        with open(data_dir / "sample_hotels.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=hotels_flat[0].keys())
            writer.writeheader()
            writer.writerows(hotels_flat)
        print(f"[OK] Exported {data_dir / 'sample_hotels.csv'}")

        # Reviews CSV
        with open(data_dir / "sample_reviews.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=reviews_data[0].keys())
            writer.writeheader()
            writer.writerows(reviews_data)
        print(f"[OK] Exported {data_dir / 'sample_reviews.csv'}")

        print("[DONE] Database seeding complete!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
