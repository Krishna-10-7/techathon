"""
Master Agent - Main orchestrator coordinating all worker agents
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from .data_analysis import DataAnalysisAgent
from .diagnosis import DiagnosisAgent
from .customer_engagement import CustomerEngagementAgent
from .scheduling import SchedulingAgent
from .feedback import FeedbackAgent
from .manufacturing_insights import ManufacturingInsightsAgent

class MasterAgent:
    def __init__(self):
        self.agent_id = "master_agent"
        self.name = "Master Agent"
        self.workers = {
            "data_analysis": DataAnalysisAgent(),
            "diagnosis": DiagnosisAgent(),
            "customer_engagement": CustomerEngagementAgent(),
            "scheduling": SchedulingAgent(),
            "feedback": FeedbackAgent(),
            "manufacturing_insights": ManufacturingInsightsAgent()
        }
        self.action_log = []
        self.active_workflows = {}
    
    def log_action(self, action: str, details: dict = None):
        self.action_log.append({"agent_id": self.agent_id, "action": action, "details": details, "timestamp": datetime.now().isoformat()})
    
    def orchestrate_vehicle_check(self, vehicle: Dict, sensor_reading: Dict, maintenance_history: List) -> Dict:
        """Full orchestration: analyze, diagnose, and prepare for engagement"""
        self.log_action("orchestrate_vehicle_check", {"vehicle_id": vehicle.get("id")})
        
        # Step 1: Data Analysis
        anomalies = self.workers["data_analysis"].detect_anomalies(sensor_reading)
        risk_assessment = self.workers["data_analysis"].get_vehicle_risk_assessment(vehicle, maintenance_history)
        
        # Step 2: Diagnosis
        diagnosis = self.workers["diagnosis"].predict_failure(vehicle, sensor_reading)
        if sensor_reading.get("active_dtcs"):
            dtc_diagnosis = self.workers["diagnosis"].diagnose_dtc(sensor_reading["active_dtcs"])
            diagnosis["dtc_diagnosis"] = dtc_diagnosis
        
        # Step 3: Manufacturing Insights
        mfg_link = self.workers["manufacturing_insights"].link_prediction_to_rca(diagnosis)
        
        # Step 4: Prepare response
        needs_engagement = diagnosis.get("priority", {}).get("level") in ["P1", "P2", "P3"]
        
        return {
            "vehicle_id": vehicle.get("id"),
            "anomalies": anomalies,
            "risk_assessment": risk_assessment,
            "diagnosis": diagnosis,
            "manufacturing_feedback": mfg_link,
            "needs_customer_engagement": needs_engagement,
            "orchestration_timestamp": datetime.now().isoformat()
        }
    
    def initiate_customer_workflow(self, vehicle: Dict, diagnosis: Dict, owner: Dict) -> Dict:
        """Start customer engagement workflow"""
        self.log_action("initiate_customer_workflow", {"vehicle_id": vehicle.get("id")})
        
        conversation = self.workers["customer_engagement"].initiate_conversation(vehicle, diagnosis, owner)
        workflow_id = f"wf_{vehicle['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.active_workflows[workflow_id] = {
            "vehicle_id": vehicle["id"],
            "conversation_id": conversation["conversation_id"],
            "stage": "engagement",
            "diagnosis": diagnosis,
            "started_at": datetime.now().isoformat()
        }
        
        return {"workflow_id": workflow_id, "conversation": conversation}
    
    def process_chat_message(self, conversation_id: str, message: str) -> Dict:
        """Process incoming chat message"""
        self.log_action("process_chat", {"conversation_id": conversation_id})
        return self.workers["customer_engagement"].process_response(conversation_id, message)
    
    def schedule_service(self, vehicle: Dict, diagnosis: Dict, preferences: Optional[Dict] = None) -> Dict:
        """Find slots and prepare for scheduling"""
        self.log_action("schedule_service", {"vehicle_id": vehicle.get("id")})
        return self.workers["scheduling"].find_best_slots(vehicle, diagnosis, preferences)
    
    def complete_booking(self, vehicle_id: str, center_id: str, date: str, time: str, service_type: str, diagnosis: Dict) -> Dict:
        """Complete booking process"""
        self.log_action("complete_booking", {"vehicle_id": vehicle_id})
        return self.workers["scheduling"].create_booking(vehicle_id, center_id, date, time, service_type, diagnosis)
    
    def get_fleet_overview(self, vehicles: List[Dict]) -> Dict:
        """Get fleet-level overview"""
        self.log_action("fleet_overview")
        return self.workers["data_analysis"].forecast_service_demand(vehicles)
    
    def get_manufacturing_report(self) -> Dict:
        """Get manufacturing insights report"""
        return self.workers["manufacturing_insights"].generate_manufacturing_report()
    
    def get_agent_status(self) -> Dict:
        """Get status of all workers"""
        return {
            "master": {"id": self.agent_id, "status": "active", "active_workflows": len(self.active_workflows)},
            "workers": {name: {"id": agent.agent_id, "status": "active", "actions": len(agent.action_log)} for name, agent in self.workers.items()}
        }
