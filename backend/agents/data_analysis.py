"""
Data Analysis Agent - Analyzes streaming vehicle telematics and sensor data
Detects early warning signs and forecasts service demand
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import numpy as np

class DataAnalysisAgent:
    """Worker agent for analyzing vehicle telematics data"""
    
    def __init__(self):
        self.agent_id = "data_analysis_agent"
        self.name = "Data Analysis Agent"
        self.permissions = ["read_telematics", "read_maintenance", "write_analysis"]
        self.action_log = []
    
    def log_action(self, action: str, details: dict = None):
        """Log agent action for UEBA monitoring"""
        self.action_log.append({
            "agent_id": self.agent_id,
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def analyze_sensor_trends(self, readings: List[Dict]) -> Dict[str, Any]:
        """Analyze trends in sensor readings over time"""
        self.log_action("analyze_sensor_trends", {"readings_count": len(readings)})
        
        if not readings:
            return {"status": "no_data"}
        
        trends = {}
        for sensor_name in readings[0].get("sensors", {}).keys():
            values = [r["sensors"][sensor_name]["value"] for r in readings if sensor_name in r.get("sensors", {})]
            if values:
                trends[sensor_name] = {
                    "current": values[-1],
                    "average": round(np.mean(values), 2),
                    "min": round(min(values), 2),
                    "max": round(max(values), 2),
                    "trend": self._calculate_trend(values),
                    "volatility": round(np.std(values), 2) if len(values) > 1 else 0
                }
        
        return trends
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 2:
            return "stable"
        
        # Simple linear regression slope
        n = len(values)
        x = list(range(n))
        slope = (n * sum(x[i] * values[i] for i in range(n)) - sum(x) * sum(values)) / \
                (n * sum(i**2 for i in x) - sum(x)**2) if n > 1 else 0
        
        if slope > 0.5:
            return "increasing"
        elif slope < -0.5:
            return "decreasing"
        return "stable"
    
    def detect_anomalies(self, current_reading: Dict, historical_avg: Dict = None) -> List[Dict]:
        """Detect anomalies in current readings"""
        self.log_action("detect_anomalies", {"vehicle_id": current_reading.get("vehicle_id")})
        
        anomalies = []
        sensors = current_reading.get("sensors", {})
        
        for sensor_name, data in sensors.items():
            if data["status"] in ["warning", "critical"]:
                anomaly = {
                    "sensor": sensor_name,
                    "value": data["value"],
                    "unit": data["unit"],
                    "severity": data["status"],
                    "timestamp": current_reading.get("timestamp"),
                    "recommendation": self._get_sensor_recommendation(sensor_name, data)
                }
                anomalies.append(anomaly)
        
        # Add DTCs as anomalies
        for dtc in current_reading.get("active_dtcs", []):
            anomalies.append({
                "type": "dtc",
                "code": dtc["code"],
                "description": dtc["description"],
                "severity": dtc["severity"],
                "component": dtc["component"],
                "first_occurrence": dtc.get("first_occurrence")
            })
        
        return anomalies
    
    def _get_sensor_recommendation(self, sensor: str, data: Dict) -> str:
        """Get recommendation based on sensor reading"""
        recommendations = {
            "engine_temp": "Schedule cooling system inspection",
            "oil_pressure": "Check oil level and quality, possible pump issue",
            "battery_voltage": "Battery health check required",
            "brake_pad_wear": "Brake pad replacement needed",
            "tire_pressure": "Check tire condition and inflation",
            "coolant_level": "Coolant top-up or leak inspection needed",
            "transmission_temp": "Transmission fluid check recommended",
            "air_filter_health": "Air filter replacement due"
        }
        
        for key, rec in recommendations.items():
            if key in sensor:
                return rec
        return "Inspection recommended"
    
    def forecast_service_demand(self, fleet_data: List[Dict]) -> Dict[str, Any]:
        """Forecast service demand based on fleet patterns"""
        self.log_action("forecast_service_demand", {"fleet_size": len(fleet_data)})
        
        # Analyze which vehicles need service soon
        urgent_services = []
        scheduled_services = []
        
        for vehicle in fleet_data:
            health = vehicle.get("health_score", 100)
            alerts = vehicle.get("active_alerts", 0)
            
            if health < 60 or alerts >= 2:
                urgent_services.append({
                    "vehicle_id": vehicle["id"],
                    "health_score": health,
                    "alerts": alerts,
                    "priority": "urgent"
                })
            elif health < 80 or alerts >= 1:
                scheduled_services.append({
                    "vehicle_id": vehicle["id"],
                    "health_score": health,
                    "alerts": alerts,
                    "priority": "scheduled"
                })
        
        forecast = {
            "forecast_date": datetime.now().isoformat(),
            "next_7_days": {
                "urgent_services": len(urgent_services),
                "scheduled_services": len(scheduled_services),
                "total_expected": len(urgent_services) + len(scheduled_services)
            },
            "urgent_vehicles": urgent_services,
            "scheduled_vehicles": scheduled_services,
            "recommendation": self._get_demand_recommendation(len(urgent_services), len(scheduled_services))
        }
        
        return forecast
    
    def _get_demand_recommendation(self, urgent: int, scheduled: int) -> str:
        """Generate staffing/capacity recommendation"""
        total = urgent + scheduled
        if total > 5:
            return "High demand expected. Consider extending operating hours."
        elif total > 2:
            return "Moderate demand expected. Ensure standard staffing."
        return "Normal demand expected."
    
    def get_vehicle_risk_assessment(self, vehicle_data: Dict, maintenance_history: List) -> Dict:
        """Assess overall risk for a vehicle"""
        self.log_action("risk_assessment", {"vehicle_id": vehicle_data.get("id")})
        
        risk_score = 0
        risk_factors = []
        
        # Check health score
        health = vehicle_data.get("health_score", 100)
        if health < 60:
            risk_score += 40
            risk_factors.append("Low health score")
        elif health < 80:
            risk_score += 20
            risk_factors.append("Moderate health score")
        
        # Check active alerts
        alerts = vehicle_data.get("active_alerts", 0)
        risk_score += alerts * 15
        if alerts > 0:
            risk_factors.append(f"{alerts} active alerts")
        
        # Check maintenance history
        unscheduled = sum(1 for m in maintenance_history if m.get("type") == "unscheduled")
        if unscheduled >= 2:
            risk_score += 25
            risk_factors.append("Recurring unscheduled repairs")
        
        # Check odometer
        odometer = vehicle_data.get("odometer", 0)
        if odometer > 75000:
            risk_score += 15
            risk_factors.append("High mileage vehicle")
        
        return {
            "vehicle_id": vehicle_data.get("id"),
            "risk_score": min(100, risk_score),
            "risk_level": "high" if risk_score >= 60 else "medium" if risk_score >= 30 else "low",
            "risk_factors": risk_factors,
            "recommendation": "Immediate attention required" if risk_score >= 60 else 
                            "Schedule preventive maintenance" if risk_score >= 30 else
                            "Continue monitoring"
        }
