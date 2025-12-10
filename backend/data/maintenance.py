"""
Maintenance Records - Historical repairs, service visits, and maintenance patterns
"""
from datetime import datetime, timedelta
import random

# Historical maintenance records
MAINTENANCE_RECORDS = [
    # VH001 - Tata Nexon EV
    {"id": "MR001", "vehicle_id": "VH001", "date": "2024-09-15", "type": "scheduled", 
     "service": "Regular Service", "description": "Oil change, filter replacement, brake inspection",
     "cost": 4500, "center_id": "SC001", "technician": "Ravi Kumar", "status": "completed"},
    {"id": "MR002", "vehicle_id": "VH001", "date": "2024-06-10", "type": "scheduled",
     "service": "Battery Check", "description": "EV battery health check, software update",
     "cost": 2000, "center_id": "SC001", "technician": "Suresh Patil", "status": "completed"},
    
    # VH002 - Mahindra XUV700 (has issues)
    {"id": "MR003", "vehicle_id": "VH002", "date": "2024-08-20", "type": "scheduled",
     "service": "Major Service", "description": "Full service with transmission fluid change",
     "cost": 12000, "center_id": "SC002", "technician": "Ajay Sharma", "status": "completed"},
    {"id": "MR004", "vehicle_id": "VH002", "date": "2024-05-12", "type": "unscheduled",
     "service": "ABS Repair", "description": "ABS sensor replacement - recurring issue",
     "cost": 8500, "center_id": "SC002", "technician": "Ajay Sharma", "status": "completed"},
    {"id": "MR005", "vehicle_id": "VH002", "date": "2024-02-18", "type": "unscheduled",
     "service": "Electrical Fix", "description": "Wiring harness repair, alternator check",
     "cost": 6200, "center_id": "SC002", "technician": "Mohan Reddy", "status": "completed"},
    
    # VH003 - Maruti Grand Vitara
    {"id": "MR006", "vehicle_id": "VH003", "date": "2024-10-01", "type": "scheduled",
     "service": "First Service", "description": "Initial checkup, fluid top-up",
     "cost": 2500, "center_id": "SC003", "technician": "Prakash Jain", "status": "completed"},
    
    # VH004 - Hyundai Creta (has issues)
    {"id": "MR007", "vehicle_id": "VH004", "date": "2024-07-10", "type": "scheduled",
     "service": "Regular Service", "description": "Oil change, brake pad replacement",
     "cost": 7800, "center_id": "SC004", "technician": "Anand Murthy", "status": "completed"},
    {"id": "MR008", "vehicle_id": "VH004", "date": "2024-04-22", "type": "unscheduled",
     "service": "Fuel System", "description": "Fuel injector cleaning, O2 sensor replacement",
     "cost": 9500, "center_id": "SC004", "technician": "Kiran Rao", "status": "completed"},
    {"id": "MR009", "vehicle_id": "VH004", "date": "2024-01-15", "type": "unscheduled",
     "service": "Exhaust Repair", "description": "Catalytic converter replacement",
     "cost": 25000, "center_id": "SC004", "technician": "Anand Murthy", "status": "completed"},
    
    # VH005 - Kia Seltos
    {"id": "MR010", "vehicle_id": "VH005", "date": "2024-09-25", "type": "scheduled",
     "service": "Regular Service", "description": "Full checkup, AC servicing",
     "cost": 5500, "center_id": "SC005", "technician": "Deepak Nair", "status": "completed"},
    
    # VH006 - Tata Harrier
    {"id": "MR011", "vehicle_id": "VH006", "date": "2024-10-15", "type": "scheduled",
     "service": "Regular Service", "description": "Oil change, tire rotation",
     "cost": 4800, "center_id": "SC001", "technician": "Ravi Kumar", "status": "completed"},
    
    # VH007 - Toyota Innova Crysta (has issues - high mileage)
    {"id": "MR012", "vehicle_id": "VH007", "date": "2024-06-20", "type": "scheduled",
     "service": "Major Service", "description": "Full service, timing belt replacement",
     "cost": 18000, "center_id": "SC006", "technician": "Vijay Menon", "status": "completed"},
    {"id": "MR013", "vehicle_id": "VH007", "date": "2024-03-08", "type": "unscheduled",
     "service": "Engine Repair", "description": "Cylinder head gasket replacement",
     "cost": 32000, "center_id": "SC006", "technician": "Vijay Menon", "status": "completed"},
    {"id": "MR014", "vehicle_id": "VH007", "date": "2023-11-22", "type": "unscheduled",
     "service": "Cooling System", "description": "Thermostat and water pump replacement",
     "cost": 12500, "center_id": "SC006", "technician": "Samir Das", "status": "completed"},
    
    # VH008 - Honda City
    {"id": "MR015", "vehicle_id": "VH008", "date": "2024-08-30", "type": "scheduled",
     "service": "Regular Service", "description": "Standard maintenance",
     "cost": 4200, "center_id": "SC007", "technician": "Arun Pillai", "status": "completed"},
    
    # VH009 - Mahindra Thar
    {"id": "MR016", "vehicle_id": "VH009", "date": "2024-11-01", "type": "scheduled",
     "service": "Off-road Check", "description": "Suspension check, 4WD system inspection",
     "cost": 5500, "center_id": "SC002", "technician": "Ajay Sharma", "status": "completed"},
    
    # VH010 - Skoda Kushaq
    {"id": "MR017", "vehicle_id": "VH010", "date": "2024-07-25", "type": "scheduled",
     "service": "Regular Service", "description": "Oil change, brake inspection",
     "cost": 6800, "center_id": "SC008", "technician": "Nitin Ghosh", "status": "completed"},
]

# Pending/Recommended maintenance
PENDING_MAINTENANCE = [
    {"vehicle_id": "VH002", "type": "urgent", "service": "ABS System Check",
     "reason": "Recurring ABS sensor issues detected", "priority": "high", "due_km": 46500},
    {"vehicle_id": "VH004", "type": "predicted", "service": "Fuel System Service",
     "reason": "Lean mixture detected, potential injector issues", "priority": "high", "due_km": 63000},
    {"vehicle_id": "VH007", "type": "urgent", "service": "Engine Diagnostic",
     "reason": "Misfire detected, coolant issues recurring", "priority": "critical", "due_km": 90000},
    {"vehicle_id": "VH001", "type": "scheduled", "service": "Regular Service",
     "reason": "Due for 30,000 km service", "priority": "medium", "due_km": 30000},
    {"vehicle_id": "VH005", "type": "scheduled", "service": "Brake Service",
     "reason": "Brake pad wear at 70%", "priority": "medium", "due_km": 45000},
]


def get_vehicle_maintenance_history(vehicle_id: str) -> list:
    """Get maintenance history for a specific vehicle"""
    records = [r for r in MAINTENANCE_RECORDS if r["vehicle_id"] == vehicle_id]
    return sorted(records, key=lambda x: x["date"], reverse=True)


def get_pending_maintenance(vehicle_id: str = None) -> list:
    """Get pending/recommended maintenance"""
    if vehicle_id:
        return [p for p in PENDING_MAINTENANCE if p["vehicle_id"] == vehicle_id]
    return PENDING_MAINTENANCE


def get_maintenance_patterns(vehicle_id: str) -> dict:
    """Analyze maintenance patterns for a vehicle"""
    history = get_vehicle_maintenance_history(vehicle_id)
    
    if not history:
        return {"pattern": "new_vehicle", "risk_level": "low"}
    
    unscheduled_count = sum(1 for r in history if r["type"] == "unscheduled")
    total_cost = sum(r["cost"] for r in history)
    
    # Pattern analysis
    pattern = {
        "total_services": len(history),
        "unscheduled_ratio": unscheduled_count / len(history) if history else 0,
        "total_cost": total_cost,
        "avg_cost_per_service": total_cost / len(history) if history else 0,
        "risk_level": "high" if unscheduled_count >= 2 else "medium" if unscheduled_count >= 1 else "low"
    }
    
    # Identify recurring issues
    issues = {}
    for record in history:
        if record["type"] == "unscheduled":
            service_type = record["service"]
            if service_type not in issues:
                issues[service_type] = 0
            issues[service_type] += 1
    
    pattern["recurring_issues"] = issues
    return pattern


def get_all_maintenance_summary() -> dict:
    """Get overall maintenance summary"""
    total_services = len(MAINTENANCE_RECORDS)
    total_cost = sum(r["cost"] for r in MAINTENANCE_RECORDS)
    unscheduled = sum(1 for r in MAINTENANCE_RECORDS if r["type"] == "unscheduled")
    
    return {
        "total_services": total_services,
        "total_cost": total_cost,
        "unscheduled_count": unscheduled,
        "scheduled_count": total_services - unscheduled,
        "pending_count": len(PENDING_MAINTENANCE),
        "critical_pending": sum(1 for p in PENDING_MAINTENANCE if p["priority"] == "critical"),
        "high_priority_pending": sum(1 for p in PENDING_MAINTENANCE if p["priority"] == "high")
    }
