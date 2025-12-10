"""
Diagnosis Agent - Runs predictive failure models and assigns priority levels
Uses ML-based failure prediction for component assessment
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class DiagnosisAgent:
    """Worker agent for predictive diagnosis and failure modeling"""
    
    def __init__(self):
        self.agent_id = "diagnosis_agent"
        self.name = "Diagnosis Agent"
        self.permissions = ["read_analysis", "read_maintenance", "write_diagnosis"]
        self.action_log = []
        self.model = self._train_failure_model()
        self.scaler = StandardScaler()
    
    def log_action(self, action: str, details: dict = None):
        """Log agent action for UEBA monitoring"""
        self.action_log.append({
            "agent_id": self.agent_id,
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def _train_failure_model(self):
        """Train a simple failure prediction model"""
        # Simulated training data: [engine_temp, oil_pressure, battery_voltage, brake_wear, mileage]
        # This would normally be trained on historical data
        np.random.seed(42)
        
        # Generate synthetic training data
        n_samples = 500
        X = np.random.rand(n_samples, 5) * np.array([30, 40, 3, 100, 100000])  # Scale to realistic ranges
        X[:, 0] += 80  # Engine temp base
        X[:, 1] += 25  # Oil pressure base
        X[:, 2] += 12  # Battery voltage base
        
        # Create labels: 1 = failure likely, 0 = healthy
        y = ((X[:, 0] > 105) | (X[:, 1] < 25) | (X[:, 2] < 12.2) | 
             (X[:, 3] > 80) | (X[:, 4] > 80000)).astype(int)
        
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X, y)
        
        return model
    
    def predict_failure(self, vehicle_data: Dict, sensor_reading: Dict) -> Dict[str, Any]:
        """Predict probability of component failures"""
        self.log_action("predict_failure", {"vehicle_id": vehicle_data.get("id")})
        
        sensors = sensor_reading.get("sensors", {})
        
        # Extract features for prediction
        features = np.array([[
            sensors.get("engine_temp", {}).get("value", 90),
            sensors.get("oil_pressure", {}).get("value", 45),
            sensors.get("battery_voltage", {}).get("value", 12.8),
            sensors.get("brake_pad_wear", {}).get("value", 50),
            vehicle_data.get("odometer", 30000)
        ]])
        
        # Get prediction probability
        failure_prob = self.model.predict_proba(features)[0][1]
        
        # Component-level analysis
        component_risks = self._analyze_component_risks(sensors, vehicle_data)
        
        return {
            "vehicle_id": vehicle_data.get("id"),
            "overall_failure_probability": round(failure_prob * 100, 1),
            "prediction_confidence": round(0.85 + random.uniform(-0.1, 0.1), 2),
            "component_risks": component_risks,
            "priority": self._assign_priority(failure_prob, component_risks),
            "timestamp": datetime.now().isoformat(),
            "next_check_recommended": self._recommend_next_check(failure_prob)
        }
    
    def _analyze_component_risks(self, sensors: Dict, vehicle_data: Dict) -> List[Dict]:
        """Analyze risk for each major component"""
        risks = []
        
        component_mappings = {
            "Engine": ["engine_temp", "oil_pressure"],
            "Electrical": ["battery_voltage"],
            "Brakes": ["brake_pad_wear"],
            "Tires": ["tire_pressure_fl", "tire_pressure_fr", "tire_pressure_rl", "tire_pressure_rr"],
            "Cooling": ["coolant_level", "engine_temp"],
            "Transmission": ["transmission_temp"],
            "Air Intake": ["air_filter_health"]
        }
        
        for component, sensor_keys in component_mappings.items():
            component_sensors = {k: sensors.get(k, {}) for k in sensor_keys if k in sensors}
            
            # Calculate risk based on sensor status
            critical_count = sum(1 for s in component_sensors.values() if s.get("status") == "critical")
            warning_count = sum(1 for s in component_sensors.values() if s.get("status") == "warning")
            
            risk_score = critical_count * 40 + warning_count * 15
            
            # Add mileage factor for certain components
            if component in ["Engine", "Transmission", "Brakes"]:
                mileage = vehicle_data.get("odometer", 0)
                if mileage > 60000:
                    risk_score += 10
                if mileage > 80000:
                    risk_score += 15
            
            if risk_score > 0 or random.random() < 0.1:  # Include some low-risk items for completeness
                risks.append({
                    "component": component,
                    "risk_score": min(100, risk_score),
                    "risk_level": "critical" if risk_score >= 60 else "high" if risk_score >= 40 else 
                                 "medium" if risk_score >= 20 else "low",
                    "sensors_affected": list(component_sensors.keys()),
                    "recommendation": self._get_component_recommendation(component, risk_score)
                })
        
        return sorted(risks, key=lambda x: x["risk_score"], reverse=True)
    
    def _get_component_recommendation(self, component: str, risk_score: int) -> str:
        """Get specific recommendation for a component"""
        if risk_score >= 60:
            actions = {
                "Engine": "Urgent engine inspection required. Risk of major failure.",
                "Electrical": "Battery replacement or charging system repair needed immediately.",
                "Brakes": "Brake system requires immediate attention for safety.",
                "Cooling": "Cooling system repair needed. Risk of overheating damage.",
                "Transmission": "Transmission fluid flush and inspection urgently required."
            }
        elif risk_score >= 40:
            actions = {
                "Engine": "Schedule engine diagnostic within 7 days.",
                "Electrical": "Battery health check recommended soon.",
                "Brakes": "Brake pad replacement should be scheduled.",
                "Cooling": "Coolant system inspection recommended.",
                "Transmission": "Transmission service due soon."
            }
        else:
            actions = {
                "Engine": "Continue regular monitoring.",
                "Electrical": "Normal operation. Check during next service.",
                "Brakes": "Satisfactory condition. Monitor wear rate.",
                "Cooling": "System functioning normally.",
                "Transmission": "No issues detected."
            }
        
        return actions.get(component, "Schedule inspection during next service.")
    
    def _assign_priority(self, failure_prob: float, risks: List[Dict]) -> Dict[str, Any]:
        """Assign service priority based on failure probability and risks"""
        critical_risks = sum(1 for r in risks if r["risk_level"] == "critical")
        high_risks = sum(1 for r in risks if r["risk_level"] == "high")
        
        if failure_prob > 0.7 or critical_risks >= 1:
            level = "P1"
            description = "Critical - Immediate attention required"
            max_delay_days = 1
        elif failure_prob > 0.5 or high_risks >= 1:
            level = "P2"
            description = "High - Service within 3 days"
            max_delay_days = 3
        elif failure_prob > 0.3 or high_risks >= 1:
            level = "P3"
            description = "Medium - Service within 7 days"
            max_delay_days = 7
        else:
            level = "P4"
            description = "Low - Schedule at convenience"
            max_delay_days = 30
        
        return {
            "level": level,
            "description": description,
            "max_delay_days": max_delay_days,
            "critical_components": critical_risks,
            "high_risk_components": high_risks
        }
    
    def _recommend_next_check(self, failure_prob: float) -> str:
        """Recommend when to next check the vehicle"""
        if failure_prob > 0.7:
            return "Immediately"
        elif failure_prob > 0.5:
            return (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        elif failure_prob > 0.3:
            return (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        return (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    def diagnose_dtc(self, dtc_codes: List[Dict]) -> List[Dict]:
        """Provide detailed diagnosis for DTCs"""
        self.log_action("diagnose_dtc", {"codes": [d["code"] for d in dtc_codes]})
        
        diagnoses = []
        for dtc in dtc_codes:
            diagnosis = {
                "code": dtc["code"],
                "description": dtc["description"],
                "component": dtc["component"],
                "severity": dtc["severity"],
                "probable_causes": self._get_probable_causes(dtc["code"]),
                "repair_estimate": self._estimate_repair(dtc["component"], dtc["severity"]),
                "parts_likely_needed": self._suggest_parts(dtc["component"])
            }
            diagnoses.append(diagnosis)
        
        return diagnoses
    
    def _get_probable_causes(self, dtc_code: str) -> List[str]:
        """Get probable causes for a DTC"""
        causes_map = {
            "P0300": ["Worn spark plugs", "Faulty ignition coils", "Fuel delivery issues", "Vacuum leak"],
            "P0171": ["Dirty MAF sensor", "Vacuum leak", "Weak fuel pump", "Clogged fuel filter"],
            "P0420": ["Worn catalytic converter", "Faulty O2 sensor", "Engine misfire", "Rich fuel mixture"],
            "P0128": ["Stuck open thermostat", "Low coolant", "Faulty coolant sensor", "Cooling fan issue"],
            "C0035": ["Damaged wheel speed sensor", "Wiring issue", "ABS module fault", "Magnetic interference"],
            "P0562": ["Weak battery", "Faulty alternator", "Loose connections", "Parasitic drain"]
        }
        return causes_map.get(dtc_code, ["Requires diagnostic inspection"])
    
    def _estimate_repair(self, component: str, severity: str) -> Dict:
        """Estimate repair cost and time"""
        estimates = {
            "engine": {"low": (3000, 2), "medium": (8000, 4), "high": (15000, 6), "critical": (30000, 8)},
            "fuel_system": {"low": (2000, 1), "medium": (5000, 3), "high": (10000, 4)},
            "exhaust": {"low": (3000, 2), "medium": (8000, 4), "high": (25000, 6)},
            "cooling": {"low": (1500, 1), "medium": (4000, 2), "high": (8000, 4)},
            "abs": {"low": (2000, 1), "medium": (5000, 3), "high": (12000, 5)},
            "electrical": {"low": (1000, 1), "medium": (3000, 2), "high": (6000, 4)}
        }
        
        comp_key = component.lower().replace(" ", "_")
        if comp_key in estimates and severity in estimates[comp_key]:
            cost, hours = estimates[comp_key][severity]
            return {"estimated_cost_inr": cost, "estimated_hours": hours}
        
        return {"estimated_cost_inr": 5000, "estimated_hours": 3}
    
    def _suggest_parts(self, component: str) -> List[str]:
        """Suggest parts likely needed for repair"""
        parts_map = {
            "engine": ["Spark plugs", "Ignition coils", "Gaskets"],
            "fuel_system": ["Fuel filter", "O2 sensor", "Fuel injector"],
            "exhaust": ["Catalytic converter", "O2 sensor", "Exhaust gasket"],
            "cooling": ["Thermostat", "Coolant", "Temperature sensor"],
            "abs": ["Wheel speed sensor", "ABS module", "Wiring harness"],
            "electrical": ["Battery", "Alternator", "Wiring harness"]
        }
        return parts_map.get(component.lower(), ["Diagnostic required"])
