"""
UEBA Monitor - User and Entity Behavior Analytics for Agentic AI security
Monitors agent behavior, detects anomalies, and prevents unauthorized actions
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
from collections import defaultdict

class UEBAMonitor:
    def __init__(self):
        self.agent_id = "ueba_monitor"
        self.name = "UEBA Security Monitor"
        self.behavioral_baselines = {}
        self.anomaly_log = []
        self.action_history = defaultdict(list)
        self.alert_thresholds = {
            "action_frequency": 50,  # Max actions per minute
            "unauthorized_access": 1,  # Any unauthorized access triggers alert
            "unusual_time": {"start": 0, "end": 5}  # Unusual hours (12am-5am)
        }
        self._initialize_baselines()
    
    def _initialize_baselines(self):
        """Initialize behavioral baselines for each agent"""
        self.behavioral_baselines = {
            "data_analysis_agent": {
                "allowed_actions": ["analyze_sensor_trends", "detect_anomalies", "forecast_service_demand", "risk_assessment"],
                "allowed_data_access": ["telematics", "maintenance", "vehicles"],
                "max_actions_per_minute": 30
            },
            "diagnosis_agent": {
                "allowed_actions": ["predict_failure", "diagnose_dtc", "analyze_component_risks"],
                "allowed_data_access": ["analysis_results", "maintenance", "vehicles"],
                "max_actions_per_minute": 20
            },
            "customer_engagement_agent": {
                "allowed_actions": ["initiate_conversation", "process_response", "generate_notification"],
                "allowed_data_access": ["diagnosis", "customer", "vehicles"],
                "max_actions_per_minute": 40
            },
            "scheduling_agent": {
                "allowed_actions": ["find_best_slots", "create_booking", "check_capacity", "reschedule", "cancel"],
                "allowed_data_access": ["service_centers", "appointments", "diagnosis"],
                "max_actions_per_minute": 25
            },
            "feedback_agent": {
                "allowed_actions": ["initiate_followup", "collect_feedback", "update_records"],
                "allowed_data_access": ["appointments", "vehicles", "customer"],
                "max_actions_per_minute": 15
            },
            "manufacturing_insights_agent": {
                "allowed_actions": ["analyze_patterns", "generate_report", "link_to_rca"],
                "allowed_data_access": ["rca_capa", "predictions", "maintenance"],
                "max_actions_per_minute": 10
            },
            "master_agent": {
                "allowed_actions": ["orchestrate", "initiate_workflow", "process_chat", "schedule_service"],
                "allowed_data_access": ["all"],
                "max_actions_per_minute": 100
            }
        }
    
    def record_action(self, agent_id: str, action: str, data_accessed: List[str] = None, details: dict = None):
        """Record an action for behavior analysis"""
        record = {
            "agent_id": agent_id,
            "action": action,
            "data_accessed": data_accessed or [],
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.action_history[agent_id].append(record)
        
        # Check for anomalies
        anomalies = self._check_anomalies(agent_id, action, data_accessed or [])
        if anomalies:
            for anomaly in anomalies:
                self._log_anomaly(agent_id, anomaly, record)
        
        return {"recorded": True, "anomalies_detected": len(anomalies) if anomalies else 0}
    
    def _check_anomalies(self, agent_id: str, action: str, data_accessed: List[str]) -> List[Dict]:
        """Check for anomalous behavior"""
        anomalies = []
        baseline = self.behavioral_baselines.get(agent_id, {})
        
        # Check 1: Unauthorized action
        allowed_actions = baseline.get("allowed_actions", [])
        if allowed_actions and not any(allowed in action for allowed in allowed_actions):
            anomalies.append({
                "type": "unauthorized_action",
                "severity": "high",
                "description": f"Agent attempted unauthorized action: {action}"
            })
        
        # Check 2: Unauthorized data access
        allowed_data = baseline.get("allowed_data_access", [])
        if "all" not in allowed_data:
            for data in data_accessed:
                if data not in allowed_data:
                    anomalies.append({
                        "type": "unauthorized_data_access",
                        "severity": "critical",
                        "description": f"Agent accessed unauthorized data: {data}"
                    })
        
        # Check 3: Action frequency (rate limiting)
        recent_actions = [a for a in self.action_history[agent_id] 
                        if datetime.fromisoformat(a["timestamp"]) > datetime.now() - timedelta(minutes=1)]
        max_actions = baseline.get("max_actions_per_minute", 50)
        if len(recent_actions) > max_actions:
            anomalies.append({
                "type": "high_frequency",
                "severity": "medium",
                "description": f"Unusual action frequency: {len(recent_actions)} actions/min (limit: {max_actions})"
            })
        
        # Check 4: Unusual time
        hour = datetime.now().hour
        if self.alert_thresholds["unusual_time"]["start"] <= hour < self.alert_thresholds["unusual_time"]["end"]:
            anomalies.append({
                "type": "unusual_time",
                "severity": "low",
                "description": f"Activity detected during unusual hours ({hour}:00)"
            })
        
        return anomalies
    
    def _log_anomaly(self, agent_id: str, anomaly: Dict, action_record: Dict):
        """Log detected anomaly"""
        log_entry = {
            "id": f"ANM{len(self.anomaly_log) + 1001}",
            "agent_id": agent_id,
            "anomaly": anomaly,
            "trigger_action": action_record,
            "status": "detected",
            "detected_at": datetime.now().isoformat()
        }
        self.anomaly_log.append(log_entry)
        
        # Auto-response for critical anomalies
        if anomaly["severity"] == "critical":
            self._trigger_alert(log_entry)
    
    def _trigger_alert(self, anomaly_log: Dict):
        """Trigger alert for critical anomalies"""
        anomaly_log["alert_triggered"] = True
        anomaly_log["alert_time"] = datetime.now().isoformat()
    
    def get_anomalies(self, severity: str = None, agent_id: str = None) -> List[Dict]:
        """Get detected anomalies with optional filtering"""
        anomalies = self.anomaly_log
        if severity:
            anomalies = [a for a in anomalies if a["anomaly"]["severity"] == severity]
        if agent_id:
            anomalies = [a for a in anomalies if a["agent_id"] == agent_id]
        return anomalies
    
    def get_agent_behavior_report(self, agent_id: str) -> Dict:
        """Get behavior analysis for an agent"""
        actions = self.action_history.get(agent_id, [])
        anomalies = [a for a in self.anomaly_log if a["agent_id"] == agent_id]
        
        return {
            "agent_id": agent_id,
            "total_actions": len(actions),
            "anomalies_detected": len(anomalies),
            "risk_level": "high" if len(anomalies) >= 3 else "medium" if len(anomalies) >= 1 else "low",
            "recent_actions": actions[-10:] if actions else [],
            "baseline": self.behavioral_baselines.get(agent_id, {})
        }
    
    def get_security_dashboard(self) -> Dict:
        """Get security dashboard data"""
        total_actions = sum(len(actions) for actions in self.action_history.values())
        critical = sum(1 for a in self.anomaly_log if a["anomaly"]["severity"] == "critical")
        
        return {
            "status": "alert" if critical > 0 else "monitoring",
            "total_actions_monitored": total_actions,
            "total_anomalies": len(self.anomaly_log),
            "by_severity": {
                "critical": critical,
                "high": sum(1 for a in self.anomaly_log if a["anomaly"]["severity"] == "high"),
                "medium": sum(1 for a in self.anomaly_log if a["anomaly"]["severity"] == "medium"),
                "low": sum(1 for a in self.anomaly_log if a["anomaly"]["severity"] == "low")
            },
            "agents_monitored": list(self.behavioral_baselines.keys()),
            "recent_anomalies": self.anomaly_log[-5:] if self.anomaly_log else []
        }
    
    def simulate_anomaly(self, anomaly_type: str) -> Dict:
        """Simulate an anomaly for demonstration"""
        simulations = {
            "unauthorized_data_access": {
                "agent_id": "scheduling_agent",
                "action": "access_telematics",
                "data_accessed": ["telematics"],
                "details": {"simulation": True}
            },
            "unauthorized_action": {
                "agent_id": "feedback_agent",
                "action": "modify_vehicle_data",
                "data_accessed": ["vehicles"],
                "details": {"simulation": True}
            }
        }
        
        if anomaly_type in simulations:
            sim = simulations[anomaly_type]
            return self.record_action(sim["agent_id"], sim["action"], sim["data_accessed"], sim["details"])
        return {"error": "Unknown simulation type"}

# Global UEBA instance
ueba_monitor = UEBAMonitor()
