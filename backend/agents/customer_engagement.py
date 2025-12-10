"""
Customer Engagement Agent - Handles personalized customer interactions
Implements persuasive conversational AI for service recommendations
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
import random

class CustomerEngagementAgent:
    """Worker agent for customer communication and engagement"""
    
    def __init__(self):
        self.agent_id = "customer_engagement_agent"
        self.name = "Customer Engagement Agent"
        self.permissions = ["read_customer", "read_diagnosis", "send_notification", "initiate_chat"]
        self.action_log = []
        self.conversation_state = {}
    
    def log_action(self, action: str, details: dict = None):
        """Log agent action for UEBA monitoring"""
        self.action_log.append({
            "agent_id": self.agent_id,
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def initiate_conversation(self, vehicle: Dict, diagnosis: Dict, owner: Dict) -> Dict[str, Any]:
        """Start a proactive conversation with vehicle owner"""
        self.log_action("initiate_conversation", {"vehicle_id": vehicle.get("id"), "owner": owner.get("name")})
        
        priority = diagnosis.get("priority", {}).get("level", "P4")
        failure_prob = diagnosis.get("overall_failure_probability", 0)
        
        # Select conversation approach based on urgency
        if priority == "P1":
            opening = self._get_urgent_opening(owner, vehicle, diagnosis)
        elif priority in ["P2", "P3"]:
            opening = self._get_concern_opening(owner, vehicle, diagnosis)
        else:
            opening = self._get_routine_opening(owner, vehicle, diagnosis)
        
        conversation_id = f"conv_{vehicle['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.conversation_state[conversation_id] = {
            "vehicle_id": vehicle["id"],
            "owner": owner,
            "diagnosis": diagnosis,
            "stage": "initial",
            "started_at": datetime.now().isoformat()
        }
        
        return {
            "conversation_id": conversation_id,
            "message": opening,
            "message_type": "proactive_outreach",
            "priority": priority,
            "suggested_responses": self._get_suggested_responses("initial", priority),
            "voice_enabled": True
        }
    
    def _get_urgent_opening(self, owner: Dict, vehicle: Dict, diagnosis: Dict) -> str:
        """Generate urgent outreach message"""
        name = owner.get("name", "").split()[0]
        make = vehicle.get("make", "")
        model = vehicle.get("model", "")
        
        critical_components = [r["component"] for r in diagnosis.get("component_risks", []) 
                              if r["risk_level"] == "critical"]
        
        component_text = ", ".join(critical_components[:2]) if critical_components else "critical systems"
        
        return (
            f"🚨 Hello {name}! This is an urgent notification from AutoCare AI.\n\n"
            f"Our monitoring system has detected a critical issue with your {make} {model}. "
            f"We've identified potential problems with your {component_text} that require immediate attention.\n\n"
            f"For your safety, we strongly recommend scheduling a service appointment within the next 24 hours. "
            f"Would you like me to find the nearest available slot for you?"
        )
    
    def _get_concern_opening(self, owner: Dict, vehicle: Dict, diagnosis: Dict) -> str:
        """Generate concerned but not urgent message"""
        name = owner.get("name", "").split()[0]
        make = vehicle.get("make", "")
        model = vehicle.get("model", "")
        
        high_risks = [r["component"] for r in diagnosis.get("component_risks", []) 
                     if r["risk_level"] in ["critical", "high"]]
        
        return (
            f"👋 Hi {name}! This is your AutoCare AI assistant.\n\n"
            f"I've been monitoring your {make} {model} and noticed some trends that I'd like to discuss with you. "
            f"Our predictive analysis indicates that your {high_risks[0] if high_risks else 'vehicle'} "
            f"may need attention soon.\n\n"
            f"The good news is, catching these issues early can prevent more costly repairs down the road! "
            f"Would you like to hear more about what we found, or shall I help you schedule a preventive checkup?"
        )
    
    def _get_routine_opening(self, owner: Dict, vehicle: Dict, diagnosis: Dict) -> str:
        """Generate routine maintenance reminder"""
        name = owner.get("name", "").split()[0]
        make = vehicle.get("make", "")
        model = vehicle.get("model", "")
        odometer = vehicle.get("odometer", 0)
        
        return (
            f"👋 Hello {name}! Your friendly AutoCare AI here.\n\n"
            f"Just checking in on your {make} {model}! With {odometer:,} km on the clock, "
            f"your vehicle is due for its regular maintenance check.\n\n"
            f"Regular servicing helps maintain your vehicle's performance and resale value. "
            f"Would you like to schedule a convenient appointment?"
        )
    
    def process_response(self, conversation_id: str, user_message: str) -> Dict[str, Any]:
        """Process user response and generate appropriate reply"""
        self.log_action("process_response", {"conversation_id": conversation_id})
        
        if conversation_id not in self.conversation_state:
            return {
                "error": "Conversation not found",
                "message": "I apologize, but I don't have context for this conversation. How can I help you today?"
            }
        
        state = self.conversation_state[conversation_id]
        user_intent = self._detect_intent(user_message)
        
        response = self._generate_response(state, user_intent, user_message)
        
        # Update conversation state
        state["stage"] = response.get("next_stage", state["stage"])
        state["last_intent"] = user_intent
        
        return response
    
    def _detect_intent(self, message: str) -> str:
        """Simple intent detection"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["yes", "sure", "okay", "ok", "schedule", "book", "appointment"]):
            return "accept_service"
        elif any(word in message_lower for word in ["no", "not now", "later", "busy", "can't"]):
            return "decline_service"
        elif any(word in message_lower for word in ["tell me more", "what", "explain", "details", "issue"]):
            return "request_info"
        elif any(word in message_lower for word in ["cost", "price", "how much", "expensive"]):
            return "ask_cost"
        elif any(word in message_lower for word in ["when", "time", "available", "slot"]):
            return "ask_availability"
        elif any(word in message_lower for word in ["thanks", "thank you", "great", "perfect"]):
            return "positive_acknowledgment"
        else:
            return "unclear"
    
    def _generate_response(self, state: Dict, intent: str, user_message: str) -> Dict[str, Any]:
        """Generate contextual response based on intent"""
        diagnosis = state.get("diagnosis", {})
        vehicle_id = state.get("vehicle_id")
        owner = state.get("owner", {})
        
        responses = {
            "accept_service": {
                "message": (
                    "Wonderful! I'm glad you're taking care of your vehicle. 🎉\n\n"
                    "Let me check the available slots at service centers near you. "
                    "Based on your location, I have a few convenient options. "
                    "Would you prefer a morning or afternoon appointment?"
                ),
                "next_stage": "scheduling",
                "action": "prepare_scheduling"
            },
            "decline_service": {
                "message": (
                    "I completely understand – everyone has a busy schedule! 😊\n\n"
                    "However, I want to make sure you're aware that delaying this service could "
                    "lead to more expensive repairs later. Our data shows that early intervention "
                    "saves customers an average of 40% on repair costs.\n\n"
                    "Would it help if I found a slot that works around your schedule? "
                    "Or I can send you a reminder for next week?"
                ),
                "next_stage": "persuasion",
                "action": "offer_alternative"
            },
            "request_info": {
                "message": self._generate_detailed_explanation(diagnosis),
                "next_stage": "informed",
                "action": None
            },
            "ask_cost": {
                "message": self._generate_cost_explanation(diagnosis),
                "next_stage": "cost_discussed",
                "action": None
            },
            "ask_availability": {
                "message": (
                    "Great question! 📅\n\n"
                    "We have multiple slots available this week:\n"
                    "• Tomorrow morning at 9:00 AM\n"
                    "• Tomorrow afternoon at 2:00 PM\n"
                    "• Day after at 10:00 AM\n\n"
                    "Which would work best for you? Or would you prefer a weekend slot?"
                ),
                "next_stage": "scheduling",
                "action": "show_slots"
            },
            "positive_acknowledgment": {
                "message": (
                    "You're welcome! 😊\n\n"
                    "Is there anything else I can help you with regarding your vehicle?"
                ),
                "next_stage": "closing",
                "action": None
            },
            "unclear": {
                "message": (
                    "I want to make sure I understand you correctly. 🤔\n\n"
                    "Are you interested in:\n"
                    "1. Scheduling a service appointment\n"
                    "2. Learning more about the issue we detected\n"
                    "3. Getting a cost estimate\n\n"
                    "Just let me know how I can best help you!"
                ),
                "next_stage": state.get("stage", "initial"),
                "action": None
            }
        }
        
        response = responses.get(intent, responses["unclear"])
        response["suggested_responses"] = self._get_suggested_responses(response["next_stage"], 
                                                                        diagnosis.get("priority", {}).get("level", "P4"))
        response["voice_enabled"] = True
        
        return response
    
    def _generate_detailed_explanation(self, diagnosis: Dict) -> str:
        """Generate detailed explanation of detected issues"""
        risks = diagnosis.get("component_risks", [])
        failure_prob = diagnosis.get("overall_failure_probability", 0)
        
        explanation = "Let me explain what our monitoring system detected:\n\n"
        
        for i, risk in enumerate(risks[:3], 1):
            if risk["risk_level"] in ["critical", "high", "medium"]:
                explanation += f"**{i}. {risk['component']}**: {risk['recommendation']}\n"
        
        explanation += (
            f"\n📊 Overall, our AI predicts a {failure_prob}% probability of needing repair "
            f"if these issues aren't addressed soon.\n\n"
            "Early maintenance is always more cost-effective and safer. Would you like to proceed with scheduling?"
        )
        
        return explanation
    
    def _generate_cost_explanation(self, diagnosis: Dict) -> str:
        """Generate cost explanation"""
        priority = diagnosis.get("priority", {}).get("level", "P4")
        
        cost_estimates = {
            "P1": ("₹15,000 - ₹35,000", "₹50,000 - ₹1,00,000"),
            "P2": ("₹8,000 - ₹20,000", "₹30,000 - ₹60,000"),
            "P3": ("₹4,000 - ₹12,000", "₹15,000 - ₹30,000"),
            "P4": ("₹2,500 - ₹6,000", "₹8,000 - ₹15,000")
        }
        
        now_cost, later_cost = cost_estimates.get(priority, cost_estimates["P4"])
        
        return (
            f"💰 Great question about costs!\n\n"
            f"Based on our diagnosis:\n"
            f"• **If addressed now**: Estimated {now_cost}\n"
            f"• **If delayed (potential breakdown)**: Could reach {later_cost}\n\n"
            f"Plus, preventive maintenance typically takes just 2-4 hours, "
            f"while breakdown repairs can leave you without your vehicle for days.\n\n"
            f"Would you like to schedule a service to save on potential future costs?"
        )
    
    def _get_suggested_responses(self, stage: str, priority: str) -> List[str]:
        """Get suggested quick responses based on conversation stage"""
        suggestions = {
            "initial": ["Yes, schedule now", "Tell me more", "How much will it cost?", "Not right now"],
            "informed": ["Schedule appointment", "What's the cost?", "I'll think about it"],
            "persuasion": ["Okay, let's schedule", "Remind me next week", "I need more time"],
            "scheduling": ["Morning works", "Afternoon is better", "Weekend please"],
            "cost_discussed": ["That's reasonable, let's proceed", "Still too expensive", "I'll decide later"],
            "closing": ["That's all, thanks!", "One more question"]
        }
        
        return suggestions.get(stage, ["Yes", "No", "Tell me more"])
    
    def generate_notification(self, vehicle: Dict, diagnosis: Dict, notification_type: str = "app") -> Dict:
        """Generate notification for mobile app or other channels"""
        self.log_action("generate_notification", {"vehicle_id": vehicle.get("id"), "type": notification_type})
        
        priority = diagnosis.get("priority", {}).get("level", "P4")
        
        notifications = {
            "P1": {
                "title": "🚨 Urgent: Vehicle Attention Required",
                "body": f"Critical issue detected in your {vehicle.get('make')} {vehicle.get('model')}. Tap to schedule immediate service.",
                "priority": "high"
            },
            "P2": {
                "title": "⚠️ Service Recommended Soon",
                "body": f"We've detected an issue with your {vehicle.get('make')} {vehicle.get('model')} that needs attention within 3 days.",
                "priority": "medium"
            },
            "P3": {
                "title": "🔧 Preventive Maintenance Suggested",
                "body": f"Your {vehicle.get('make')} {vehicle.get('model')} could benefit from a checkup. Schedule at your convenience.",
                "priority": "medium"
            },
            "P4": {
                "title": "📅 Service Reminder",
                "body": f"Time for regular maintenance on your {vehicle.get('make')} {vehicle.get('model')}!",
                "priority": "low"
            }
        }
        
        notification = notifications.get(priority, notifications["P4"])
        notification["vehicle_id"] = vehicle.get("id")
        notification["timestamp"] = datetime.now().isoformat()
        notification["action_url"] = f"/schedule?vehicle={vehicle.get('id')}"
        
        return notification
