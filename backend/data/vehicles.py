"""
Synthetic Vehicle Data - 10 vehicles with sensor readings, usage patterns, and DTCs
"""
import random
from datetime import datetime, timedelta

# 10 Synthetic Vehicles
VEHICLES = [
    {
        "id": "VH001",
        "vin": "1HGBH41JXMN109186",
        "make": "Tata",
        "model": "Nexon EV",
        "year": 2023,
        "owner": {"name": "Rahul Sharma", "phone": "+91-9876543210", "email": "rahul.sharma@email.com"},
        "odometer": 25420,
        "last_service": "2024-09-15",
        "city": "Mumbai"
    },
    {
        "id": "VH002",
        "vin": "2HGBH41JXMN209287",
        "make": "Mahindra",
        "model": "XUV700",
        "year": 2022,
        "owner": {"name": "Priya Patel", "phone": "+91-9876543211", "email": "priya.patel@email.com"},
        "odometer": 45780,
        "last_service": "2024-08-20",
        "city": "Delhi"
    },
    {
        "id": "VH003",
        "vin": "3HGBH41JXMN309388",
        "make": "Maruti",
        "model": "Grand Vitara",
        "year": 2023,
        "owner": {"name": "Amit Kumar", "phone": "+91-9876543212", "email": "amit.kumar@email.com"},
        "odometer": 18950,
        "last_service": "2024-10-01",
        "city": "Bangalore"
    },
    {
        "id": "VH004",
        "vin": "4HGBH41JXMN409489",
        "make": "Hyundai",
        "model": "Creta",
        "year": 2021,
        "owner": {"name": "Sneha Reddy", "phone": "+91-9876543213", "email": "sneha.reddy@email.com"},
        "odometer": 62340,
        "last_service": "2024-07-10",
        "city": "Hyderabad"
    },
    {
        "id": "VH005",
        "vin": "5HGBH41JXMN509590",
        "make": "Kia",
        "model": "Seltos",
        "year": 2022,
        "owner": {"name": "Vikram Singh", "phone": "+91-9876543214", "email": "vikram.singh@email.com"},
        "odometer": 38920,
        "last_service": "2024-09-25",
        "city": "Chennai"
    },
    {
        "id": "VH006",
        "vin": "6HGBH41JXMN609691",
        "make": "Tata",
        "model": "Harrier",
        "year": 2023,
        "owner": {"name": "Neha Gupta", "phone": "+91-9876543215", "email": "neha.gupta@email.com"},
        "odometer": 21560,
        "last_service": "2024-10-15",
        "city": "Pune"
    },
    {
        "id": "VH007",
        "vin": "7HGBH41JXMN709792",
        "make": "Toyota",
        "model": "Innova Crysta",
        "year": 2020,
        "owner": {"name": "Rajesh Menon", "phone": "+91-9876543216", "email": "rajesh.menon@email.com"},
        "odometer": 89450,
        "last_service": "2024-06-20",
        "city": "Kochi"
    },
    {
        "id": "VH008",
        "vin": "8HGBH41JXMN809893",
        "make": "Honda",
        "model": "City",
        "year": 2022,
        "owner": {"name": "Ananya Joshi", "phone": "+91-9876543217", "email": "ananya.joshi@email.com"},
        "odometer": 34120,
        "last_service": "2024-08-30",
        "city": "Ahmedabad"
    },
    {
        "id": "VH009",
        "vin": "9HGBH41JXMN909994",
        "make": "Mahindra",
        "model": "Thar",
        "year": 2023,
        "owner": {"name": "Arjun Nair", "phone": "+91-9876543218", "email": "arjun.nair@email.com"},
        "odometer": 15780,
        "last_service": "2024-11-01",
        "city": "Jaipur"
    },
    {
        "id": "VH010",
        "vin": "0HGBH41JXMN010095",
        "make": "Skoda",
        "model": "Kushaq",
        "year": 2022,
        "owner": {"name": "Meera Iyer", "phone": "+91-9876543219", "email": "meera.iyer@email.com"},
        "odometer": 42890,
        "last_service": "2024-07-25",
        "city": "Kolkata"
    }
]

# Sensor baseline values and thresholds
SENSOR_CONFIG = {
    "engine_temp": {"min": 85, "max": 105, "critical": 110, "unit": "°C"},
    "oil_pressure": {"min": 25, "max": 65, "critical_low": 20, "unit": "psi"},
    "battery_voltage": {"min": 12.4, "max": 14.8, "critical_low": 12.0, "unit": "V"},
    "brake_pad_wear": {"min": 0, "max": 100, "critical": 85, "unit": "%"},
    "tire_pressure_fl": {"min": 30, "max": 35, "critical_low": 28, "unit": "psi"},
    "tire_pressure_fr": {"min": 30, "max": 35, "critical_low": 28, "unit": "psi"},
    "tire_pressure_rl": {"min": 30, "max": 35, "critical_low": 28, "unit": "psi"},
    "tire_pressure_rr": {"min": 30, "max": 35, "critical_low": 28, "unit": "psi"},
    "fuel_level": {"min": 0, "max": 100, "critical_low": 10, "unit": "%"},
    "coolant_level": {"min": 0, "max": 100, "critical_low": 20, "unit": "%"},
    "transmission_temp": {"min": 70, "max": 95, "critical": 110, "unit": "°C"},
    "air_filter_health": {"min": 0, "max": 100, "critical": 75, "unit": "% degraded"}
}

# Diagnostic Trouble Codes (DTCs)
DTC_CODES = {
    "P0300": {"description": "Random/Multiple Cylinder Misfire Detected", "severity": "high", "component": "engine"},
    "P0171": {"description": "System Too Lean (Bank 1)", "severity": "medium", "component": "fuel_system"},
    "P0420": {"description": "Catalyst System Efficiency Below Threshold", "severity": "medium", "component": "exhaust"},
    "P0128": {"description": "Coolant Thermostat Temperature Below Regulating", "severity": "low", "component": "cooling"},
    "P0455": {"description": "Evaporative Emission System Leak Detected", "severity": "low", "component": "emissions"},
    "P0507": {"description": "Idle Air Control System RPM Higher Than Expected", "severity": "medium", "component": "engine"},
    "C0035": {"description": "Left Front Wheel Speed Sensor Circuit", "severity": "high", "component": "abs"},
    "B0100": {"description": "Electronic Frontal Sensor 1 Performance", "severity": "high", "component": "airbag"},
    "U0100": {"description": "Lost Communication with ECM/PCM", "severity": "critical", "component": "ecu"},
    "P0562": {"description": "System Voltage Low", "severity": "medium", "component": "electrical"}
}


def generate_sensor_reading(vehicle_id: str, anomaly_chance: float = 0.15):
    """Generate real-time sensor readings for a vehicle with optional anomalies"""
    reading = {
        "vehicle_id": vehicle_id,
        "timestamp": datetime.now().isoformat(),
        "sensors": {}
    }
    
    # Add some vehicles with persistent issues for demo
    has_issue = vehicle_id in ["VH004", "VH007", "VH002"]
    
    for sensor, config in SENSOR_CONFIG.items():
        base_value = (config["min"] + config["max"]) / 2
        variance = (config["max"] - config["min"]) / 4
        
        # Generate normal reading
        value = base_value + random.uniform(-variance, variance)
        
        # Inject anomalies
        if has_issue or random.random() < anomaly_chance:
            if "critical" in config:
                value = config["critical"] + random.uniform(0, 10)
            elif "critical_low" in config:
                value = config["critical_low"] - random.uniform(0, 5)
        
        reading["sensors"][sensor] = {
            "value": round(value, 2),
            "unit": config["unit"],
            "status": get_sensor_status(sensor, value, config)
        }
    
    # Add active DTCs
    reading["active_dtcs"] = generate_active_dtcs(vehicle_id, has_issue)
    
    return reading


def get_sensor_status(sensor: str, value: float, config: dict) -> str:
    """Determine sensor status based on value"""
    if "critical" in config and value >= config["critical"]:
        return "critical"
    if "critical_low" in config and value <= config["critical_low"]:
        return "critical"
    if value < config["min"] or value > config["max"]:
        return "warning"
    return "normal"


def generate_active_dtcs(vehicle_id: str, has_issue: bool) -> list:
    """Generate active diagnostic trouble codes"""
    dtcs = []
    
    # Vehicles with issues have persistent DTCs
    issue_map = {
        "VH004": ["P0171", "P0420"],  # Fuel and exhaust issues
        "VH007": ["P0300", "P0128"],  # Engine and cooling issues
        "VH002": ["C0035", "P0562"]   # ABS and electrical issues
    }
    
    if vehicle_id in issue_map:
        for code in issue_map[vehicle_id]:
            dtcs.append({
                "code": code,
                **DTC_CODES[code],
                "first_occurrence": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            })
    elif has_issue:
        code = random.choice(list(DTC_CODES.keys()))
        dtcs.append({
            "code": code,
            **DTC_CODES[code],
            "first_occurrence": datetime.now().isoformat()
        })
    
    return dtcs


def get_vehicle_by_id(vehicle_id: str):
    """Get vehicle by ID"""
    for vehicle in VEHICLES:
        if vehicle["id"] == vehicle_id:
            return vehicle
    return None


def get_all_vehicles():
    """Get all vehicles with current health status"""
    vehicles_with_status = []
    for vehicle in VEHICLES:
        reading = generate_sensor_reading(vehicle["id"])
        health_score = calculate_health_score(reading)
        vehicles_with_status.append({
            **vehicle,
            "health_score": health_score,
            "active_alerts": len(reading["active_dtcs"]),
            "current_reading": reading
        })
    return vehicles_with_status


def calculate_health_score(reading: dict) -> int:
    """Calculate overall vehicle health score (0-100)"""
    score = 100
    
    for sensor, data in reading["sensors"].items():
        if data["status"] == "critical":
            score -= 15
        elif data["status"] == "warning":
            score -= 5
    
    # Deduct for DTCs
    for dtc in reading["active_dtcs"]:
        if dtc["severity"] == "critical":
            score -= 20
        elif dtc["severity"] == "high":
            score -= 10
        elif dtc["severity"] == "medium":
            score -= 5
    
    return max(0, min(100, score))
