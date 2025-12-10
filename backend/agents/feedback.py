"""
Feedback Agent - Handles post-service follow-up and customer satisfaction tracking
"""
from datetime import datetime
from typing import List, Dict, Any

class FeedbackAgent:
    def __init__(self):
        self.agent_id = "feedback_agent"
        self.name = "Feedback Agent"
        self.permissions = ["read_service", "write_feedback", "update_records"]
        self.action_log = []
        self.feedback_store = []
    
    def log_action(self, action: str, details: dict = None):
        self.action_log.append({"agent_id": self.agent_id, "action": action, "details": details, "timestamp": datetime.now().isoformat()})
    
    def initiate_followup(self, appointment: Dict, vehicle: Dict, owner: Dict) -> Dict:
        """Initiate post-service follow-up conversation"""
        self.log_action("initiate_followup", {"appointment_id": appointment.get("id")})
        
        message = (
            f"Hi {owner.get('name', '').split()[0]}! 👋\n\n"
            f"Thank you for choosing our service center for your {vehicle.get('make')} {vehicle.get('model')}.\n\n"
            f"We hope everything went smoothly! Could you take a moment to share your experience? "
            f"Your feedback helps us improve our service.\n\n"
            f"How would you rate your overall experience? (1-5 stars)"
        )
        
        return {
            "type": "followup",
            "appointment_id": appointment.get("id"),
            "vehicle_id": vehicle.get("id"),
            "message": message,
            "rating_options": [1, 2, 3, 4, 5],
            "followup_questions": ["How was the staff behavior?", "Was the service completed on time?", "Would you recommend us?"]
        }
    
    def collect_feedback(self, appointment_id: str, rating: int, comments: str = "", details: Dict = None) -> Dict:
        """Collect and store customer feedback"""
        self.log_action("collect_feedback", {"appointment_id": appointment_id, "rating": rating})
        
        feedback = {
            "id": f"FB{len(self.feedback_store) + 1001}",
            "appointment_id": appointment_id,
            "rating": rating,
            "comments": comments,
            "details": details or {},
            "timestamp": datetime.now().isoformat(),
            "sentiment": "positive" if rating >= 4 else "neutral" if rating == 3 else "negative"
        }
        
        self.feedback_store.append(feedback)
        
        response_message = self._generate_response(rating)
        
        return {"success": True, "feedback_id": feedback["id"], "message": response_message}
    
    def _generate_response(self, rating: int) -> str:
        if rating >= 4:
            return "Thank you for the wonderful feedback! 🌟 We're thrilled you had a great experience. See you next time!"
        elif rating == 3:
            return "Thank you for your feedback. We're always working to improve. Please let us know how we can serve you better!"
        else:
            return "We're sorry to hear about your experience. 😔 A manager will contact you shortly to address your concerns."
    
    def analyze_feedback_trends(self) -> Dict:
        """Analyze feedback trends for insights"""
        if not self.feedback_store:
            return {"message": "No feedback data available"}
        
        ratings = [f["rating"] for f in self.feedback_store]
        avg_rating = sum(ratings) / len(ratings)
        
        return {
            "total_responses": len(self.feedback_store),
            "average_rating": round(avg_rating, 2),
            "positive_percentage": round(sum(1 for r in ratings if r >= 4) / len(ratings) * 100, 1),
            "needs_attention": [f for f in self.feedback_store if f["rating"] <= 2]
        }
    
    def update_vehicle_records(self, vehicle_id: str, service_data: Dict) -> Dict:
        """Update vehicle maintenance records after service"""
        self.log_action("update_records", {"vehicle_id": vehicle_id})
        return {"success": True, "vehicle_id": vehicle_id, "records_updated": True, "timestamp": datetime.now().isoformat()}
