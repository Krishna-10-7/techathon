"""
Scheduling Agent - Manages appointment scheduling and service center coordination
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.service_centers import get_available_slots, book_appointment, get_recommended_center, get_center_load

class SchedulingAgent:
    def __init__(self):
        self.agent_id = "scheduling_agent"
        self.name = "Scheduling Agent"
        self.permissions = ["read_schedule", "write_booking", "read_capacity"]
        self.action_log = []
    
    def log_action(self, action: str, details: dict = None):
        self.action_log.append({"agent_id": self.agent_id, "action": action, "details": details, "timestamp": datetime.now().isoformat()})
    
    def find_best_slots(self, vehicle: Dict, diagnosis: Dict, preferences: Optional[Dict] = None) -> Dict:
        self.log_action("find_best_slots", {"vehicle_id": vehicle.get("id")})
        city = vehicle.get("city", "Mumbai")
        priority = diagnosis.get("priority", {}).get("level", "P4")
        recommended_center = get_recommended_center(city, "regular")
        if not recommended_center:
            return {"error": "No service centers available"}
        
        days_map = {"P1": 2, "P2": 5, "P3": 7, "P4": 14}
        available_slots = get_available_slots(recommended_center["id"], days_ahead=days_map.get(priority, 7))
        ranked_slots = self._rank_slots(available_slots, preferences, priority)
        
        return {
            "vehicle_id": vehicle.get("id"),
            "recommended_center": {"id": recommended_center["id"], "name": recommended_center["name"], "address": recommended_center["address"], "rating": recommended_center["rating"]},
            "priority": priority,
            "available_slots": ranked_slots[:5]
        }
    
    def _rank_slots(self, slots: List[Dict], preferences: Optional[Dict], priority: str) -> List[Dict]:
        ranked = []
        preferred_time = preferences.get("preferred_time", "any") if preferences else "any"
        for slot in slots:
            for ts in slot.get("time_slots", []):
                score = 100
                hour = int(ts["time"].split(":")[0])
                if preferred_time == "morning" and hour < 12: score += 15
                elif preferred_time == "afternoon" and hour >= 12: score += 15
                ranked.append({"date": slot["date"], "day": slot["day"], "time": ts["time"], "spots_available": ts.get("available", 1), "score": score})
        return sorted(ranked, key=lambda x: x["score"], reverse=True)
    
    def create_booking(self, vehicle_id: str, center_id: str, date: str, time: str, service_type: str, diagnosis: Dict) -> Dict:
        self.log_action("create_booking", {"vehicle_id": vehicle_id, "center_id": center_id})
        notes = f"Priority: {diagnosis.get('priority', {}).get('level', 'P4')}"
        result = book_appointment(vehicle_id, center_id, date, time, service_type, notes)
        if result.get("success"):
            return {"success": True, "confirmation_number": result["appointment"]["id"], "message": f"✅ Appointment confirmed for {date} at {time}!"}
        return {"success": False, "error": result.get("error", "Booking failed")}
    
    def check_capacity(self, center_id: str) -> Dict:
        self.log_action("check_capacity", {"center_id": center_id})
        return get_center_load(center_id)
