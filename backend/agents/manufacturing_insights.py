"""
Manufacturing Insights Agent - RCA/CAPA analysis for manufacturing feedback loop
"""
from datetime import datetime
from typing import List, Dict, Any
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.rca_capa import get_rca_records, get_capa_for_rca, get_manufacturing_insights, get_component_defect_pattern, get_feedback_summary

class ManufacturingInsightsAgent:
    def __init__(self):
        self.agent_id = "manufacturing_insights_agent"
        self.name = "Manufacturing Insights Agent"
        self.permissions = ["read_rca", "read_capa", "write_insights"]
        self.action_log = []
    
    def log_action(self, action: str, details: dict = None):
        self.action_log.append({"agent_id": self.agent_id, "action": action, "details": details, "timestamp": datetime.now().isoformat()})
    
    def analyze_failure_patterns(self, predictions: List[Dict]) -> Dict:
        """Analyze predicted failures for manufacturing patterns"""
        self.log_action("analyze_patterns", {"predictions_count": len(predictions)})
        
        component_counts = {}
        for pred in predictions:
            for risk in pred.get("component_risks", []):
                if risk["risk_level"] in ["critical", "high"]:
                    comp = risk["component"]
                    component_counts[comp] = component_counts.get(comp, 0) + 1
        
        patterns = []
        for component, count in component_counts.items():
            existing_pattern = get_component_defect_pattern(component)
            patterns.append({
                "component": component,
                "current_predictions": count,
                "historical_data": existing_pattern,
                "action_required": count >= 3 or existing_pattern.get("total_rca_records", 0) > 0
            })
        
        return {"patterns": sorted(patterns, key=lambda x: x["current_predictions"], reverse=True), "timestamp": datetime.now().isoformat()}
    
    def generate_manufacturing_report(self) -> Dict:
        """Generate comprehensive report for manufacturing team"""
        self.log_action("generate_report")
        
        rca_records = get_rca_records()
        insights = get_manufacturing_insights()
        summary = get_feedback_summary()
        
        high_priority = [r for r in rca_records if r["severity"] in ["critical", "high"]]
        
        return {
            "report_date": datetime.now().isoformat(),
            "summary": summary,
            "high_priority_issues": high_priority,
            "active_insights": insights,
            "recommendations": self._generate_recommendations(high_priority, insights)
        }
    
    def _generate_recommendations(self, issues: List, insights: List) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        for issue in issues[:3]:
            capa = get_capa_for_rca(issue["id"])
            pending_capa = [c for c in capa if c["status"] == "pending"]
            
            if pending_capa:
                recommendations.append({
                    "priority": "high",
                    "type": "implement_capa",
                    "issue": issue["defect_code"],
                    "action": f"Implement pending CAPA for {issue['component']}",
                    "impact": f"Affects {issue['affected_vehicles']} vehicles"
                })
            elif issue["status"] == "investigating":
                recommendations.append({
                    "priority": "high",
                    "type": "expedite_investigation",
                    "issue": issue["defect_code"],
                    "action": f"Expedite RCA for {issue['component']}",
                    "impact": f"{issue['occurrences']} occurrences reported"
                })
        
        return recommendations
    
    def link_prediction_to_rca(self, prediction: Dict) -> Dict:
        """Link a prediction to existing RCA records"""
        self.log_action("link_to_rca", {"vehicle_id": prediction.get("vehicle_id")})
        
        linked_issues = []
        for risk in prediction.get("component_risks", []):
            pattern = get_component_defect_pattern(risk["component"])
            if pattern.get("total_rca_records", 0) > 0:
                linked_issues.append({"component": risk["component"], "pattern": pattern, "risk_level": risk["risk_level"]})
        
        return {"prediction_id": prediction.get("vehicle_id"), "linked_rca_issues": linked_issues, "feedback_generated": len(linked_issues) > 0}
    
    def get_dashboard_data(self) -> Dict:
        """Get data for manufacturing insights dashboard"""
        return {"summary": get_feedback_summary(), "insights": get_manufacturing_insights(), "recent_rca": get_rca_records()[:5]}
