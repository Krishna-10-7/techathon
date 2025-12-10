"""
Service Centers - Locations, capacity, and scheduling availability
"""
from datetime import datetime, timedelta
import random

# Service Centers across India
SERVICE_CENTERS = [
    {
        "id": "SC001",
        "name": "AutoCare Mumbai Central",
        "city": "Mumbai",
        "address": "123 Andheri West, Mumbai 400058",
        "phone": "+91-22-12345678",
        "capacity": {"bays": 8, "daily_capacity": 24},
        "operating_hours": {"open": "08:00", "close": "20:00"},
        "services": ["regular", "major", "ev", "body"],
        "rating": 4.5
    },
    {
        "id": "SC002",
        "name": "Mahindra Service Hub Delhi",
        "city": "Delhi",
        "address": "456 Connaught Place, New Delhi 110001",
        "phone": "+91-11-23456789",
        "capacity": {"bays": 10, "daily_capacity": 30},
        "operating_hours": {"open": "08:00", "close": "21:00"},
        "services": ["regular", "major", "offroad", "body"],
        "rating": 4.3
    },
    {
        "id": "SC003",
        "name": "Maruti Arena Bangalore",
        "city": "Bangalore",
        "address": "789 MG Road, Bangalore 560001",
        "phone": "+91-80-34567890",
        "capacity": {"bays": 12, "daily_capacity": 36},
        "operating_hours": {"open": "07:30", "close": "20:30"},
        "services": ["regular", "major", "hybrid", "body"],
        "rating": 4.7
    },
    {
        "id": "SC004",
        "name": "Hyundai Prime Hyderabad",
        "city": "Hyderabad",
        "address": "321 Banjara Hills, Hyderabad 500034",
        "phone": "+91-40-45678901",
        "capacity": {"bays": 8, "daily_capacity": 24},
        "operating_hours": {"open": "08:00", "close": "20:00"},
        "services": ["regular", "major", "ev", "body"],
        "rating": 4.4
    },
    {
        "id": "SC005",
        "name": "Kia Service Chennai",
        "city": "Chennai",
        "address": "654 Anna Nagar, Chennai 600040",
        "phone": "+91-44-56789012",
        "capacity": {"bays": 6, "daily_capacity": 18},
        "operating_hours": {"open": "08:30", "close": "19:30"},
        "services": ["regular", "major", "body"],
        "rating": 4.2
    },
    {
        "id": "SC006",
        "name": "Toyota Platinum Kochi",
        "city": "Kochi",
        "address": "987 MG Road, Kochi 682011",
        "phone": "+91-484-67890123",
        "capacity": {"bays": 6, "daily_capacity": 18},
        "operating_hours": {"open": "09:00", "close": "19:00"},
        "services": ["regular", "major", "hybrid", "body"],
        "rating": 4.6
    },
    {
        "id": "SC007",
        "name": "Honda Express Ahmedabad",
        "city": "Ahmedabad",
        "address": "147 CG Road, Ahmedabad 380006",
        "phone": "+91-79-78901234",
        "capacity": {"bays": 8, "daily_capacity": 24},
        "operating_hours": {"open": "08:00", "close": "20:00"},
        "services": ["regular", "major", "body"],
        "rating": 4.3
    },
    {
        "id": "SC008",
        "name": "Skoda Volkswagen Kolkata",
        "city": "Kolkata",
        "address": "258 Park Street, Kolkata 700016",
        "phone": "+91-33-89012345",
        "capacity": {"bays": 6, "daily_capacity": 18},
        "operating_hours": {"open": "09:00", "close": "19:00"},
        "services": ["regular", "major", "body"],
        "rating": 4.1
    }
]

# Pre-booked appointments (simulated current load)
EXISTING_BOOKINGS = {
    "SC001": {"2024-12-11": 18, "2024-12-12": 20, "2024-12-13": 15, "2024-12-14": 22},
    "SC002": {"2024-12-11": 25, "2024-12-12": 22, "2024-12-13": 28, "2024-12-14": 20},
    "SC003": {"2024-12-11": 30, "2024-12-12": 28, "2024-12-13": 32, "2024-12-14": 25},
    "SC004": {"2024-12-11": 15, "2024-12-12": 18, "2024-12-13": 12, "2024-12-14": 20},
}

# Confirmed appointments
APPOINTMENTS = []


def get_service_center(center_id: str) -> dict:
    """Get service center by ID"""
    for center in SERVICE_CENTERS:
        if center["id"] == center_id:
            return center
    return None


def get_service_centers_by_city(city: str) -> list:
    """Get service centers in a city"""
    return [c for c in SERVICE_CENTERS if c["city"].lower() == city.lower()]


def get_all_service_centers() -> list:
    """Get all service centers"""
    return SERVICE_CENTERS


def get_available_slots(center_id: str, date: str = None, days_ahead: int = 7) -> list:
    """Get available appointment slots for a service center"""
    center = get_service_center(center_id)
    if not center:
        return []
    
    slots = []
    start_date = datetime.now() + timedelta(days=1)  # Start from tomorrow
    
    for day_offset in range(days_ahead):
        slot_date = start_date + timedelta(days=day_offset)
        date_str = slot_date.strftime("%Y-%m-%d")
        
        if date and date_str != date:
            continue
        
        # Get current bookings for this date
        booked = EXISTING_BOOKINGS.get(center_id, {}).get(date_str, 0)
        available = center["capacity"]["daily_capacity"] - booked
        
        if available > 0:
            # Generate time slots
            time_slots = []
            open_hour = int(center["operating_hours"]["open"].split(":")[0])
            close_hour = int(center["operating_hours"]["close"].split(":")[0])
            
            for hour in range(open_hour, close_hour - 1, 2):  # 2-hour slots
                time_str = f"{hour:02d}:00"
                time_slots.append({
                    "time": time_str,
                    "available": random.randint(1, 3)  # Random availability per slot
                })
            
            slots.append({
                "date": date_str,
                "day": slot_date.strftime("%A"),
                "total_available": available,
                "time_slots": time_slots
            })
    
    return slots


def book_appointment(vehicle_id: str, center_id: str, date: str, time: str, 
                    service_type: str, notes: str = "") -> dict:
    """Book a service appointment"""
    center = get_service_center(center_id)
    if not center:
        return {"success": False, "error": "Service center not found"}
    
    appointment = {
        "id": f"APT{len(APPOINTMENTS) + 1001}",
        "vehicle_id": vehicle_id,
        "center_id": center_id,
        "center_name": center["name"],
        "date": date,
        "time": time,
        "service_type": service_type,
        "notes": notes,
        "status": "confirmed",
        "created_at": datetime.now().isoformat()
    }
    
    APPOINTMENTS.append(appointment)
    
    # Update bookings count
    if center_id not in EXISTING_BOOKINGS:
        EXISTING_BOOKINGS[center_id] = {}
    if date not in EXISTING_BOOKINGS[center_id]:
        EXISTING_BOOKINGS[center_id][date] = 0
    EXISTING_BOOKINGS[center_id][date] += 1
    
    return {"success": True, "appointment": appointment}


def get_vehicle_appointments(vehicle_id: str) -> list:
    """Get appointments for a vehicle"""
    return [a for a in APPOINTMENTS if a["vehicle_id"] == vehicle_id]


def get_center_load(center_id: str) -> dict:
    """Get current load and capacity for a service center"""
    center = get_service_center(center_id)
    if not center:
        return {}
    
    today = datetime.now().strftime("%Y-%m-%d")
    current_bookings = EXISTING_BOOKINGS.get(center_id, {}).get(today, 0)
    
    return {
        "center_id": center_id,
        "center_name": center["name"],
        "capacity": center["capacity"]["daily_capacity"],
        "current_bookings": current_bookings,
        "utilization": round(current_bookings / center["capacity"]["daily_capacity"] * 100, 1),
        "available_today": center["capacity"]["daily_capacity"] - current_bookings
    }


def get_recommended_center(city: str, service_type: str = "regular") -> dict:
    """Get recommended service center based on city and availability"""
    centers = get_service_centers_by_city(city)
    if not centers:
        # Return nearest center from any city
        centers = SERVICE_CENTERS
    
    # Score centers based on rating and availability
    best_center = None
    best_score = 0
    
    for center in centers:
        if service_type not in center["services"]:
            continue
        
        load = get_center_load(center["id"])
        availability_score = (100 - load.get("utilization", 100)) / 100
        rating_score = center["rating"] / 5
        
        score = (availability_score * 0.6) + (rating_score * 0.4)
        
        if score > best_score:
            best_score = score
            best_center = center
    
    return best_center
