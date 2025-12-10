"""
API Routes - REST API endpoints for the Predictive Maintenance System
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.vehicles import get_all_vehicles, get_vehicle_by_id, generate_sensor_reading
from data.maintenance import get_vehicle_maintenance_history, get_pending_maintenance, get_all_maintenance_summary
from data.service_centers import get_all_service_centers, get_available_slots, book_appointment
from data.rca_capa import get_rca_records, get_manufacturing_insights, get_feedback_summary
from agents.master_agent import MasterAgent
from security.ueba import ueba_monitor

router = APIRouter()
master_agent = MasterAgent()

# Pydantic models
class ChatMessage(BaseModel):
    conversation_id: str
    message: str

class BookingRequest(BaseModel):
    vehicle_id: str
    center_id: str
    date: str
    time: str
    service_type: str = "regular"

# Vehicle endpoints
@router.get("/vehicles")
async def list_vehicles():
    """Get all vehicles with health status"""
    vehicles = get_all_vehicles()
    return {"vehicles": vehicles, "total": len(vehicles)}

@router.get("/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: str):
    """Get vehicle details with current reading and diagnosis"""
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    reading = generate_sensor_reading(vehicle_id)
    history = get_vehicle_maintenance_history(vehicle_id)
    
    result = master_agent.orchestrate_vehicle_check(vehicle, reading, history)
    return {"vehicle": vehicle, **result}

@router.get("/vehicles/{vehicle_id}/alerts")
async def get_vehicle_alerts(vehicle_id: str):
    """Get active alerts for a vehicle"""
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    reading = generate_sensor_reading(vehicle_id)
    anomalies = master_agent.workers["data_analysis"].detect_anomalies(reading)
    return {"vehicle_id": vehicle_id, "alerts": anomalies}

# Chat endpoints
@router.post("/chat/start/{vehicle_id}")
async def start_chat(vehicle_id: str):
    """Start a chat conversation for a vehicle"""
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    reading = generate_sensor_reading(vehicle_id)
    history = get_vehicle_maintenance_history(vehicle_id)
    check_result = master_agent.orchestrate_vehicle_check(vehicle, reading, history)
    
    workflow = master_agent.initiate_customer_workflow(vehicle, check_result["diagnosis"], vehicle["owner"])
    return workflow

@router.post("/chat")
async def process_chat(chat: ChatMessage):
    """Process a chat message"""
    response = master_agent.process_chat_message(chat.conversation_id, chat.message)
    return response

# Scheduling endpoints
@router.get("/schedule/slots/{vehicle_id}")
async def get_slots(vehicle_id: str):
    """Get available slots for a vehicle"""
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    reading = generate_sensor_reading(vehicle_id)
    diagnosis = master_agent.workers["diagnosis"].predict_failure(vehicle, reading)
    slots = master_agent.schedule_service(vehicle, diagnosis)
    return slots

@router.post("/schedule/book")
async def book_slot(booking: BookingRequest):
    """Book an appointment"""
    vehicle = get_vehicle_by_id(booking.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    reading = generate_sensor_reading(booking.vehicle_id)
    diagnosis = master_agent.workers["diagnosis"].predict_failure(vehicle, reading)
    
    result = master_agent.complete_booking(
        booking.vehicle_id, booking.center_id, booking.date, 
        booking.time, booking.service_type, diagnosis
    )
    return result

@router.get("/service-centers")
async def list_service_centers():
    """Get all service centers"""
    return {"centers": get_all_service_centers()}

# Manufacturing insights endpoints
@router.get("/insights")
async def get_insights():
    """Get manufacturing insights"""
    return master_agent.get_manufacturing_report()

@router.get("/insights/rca")
async def get_rca():
    """Get RCA records"""
    return {"records": get_rca_records()}

@router.get("/insights/summary")
async def get_mfg_summary():
    """Get manufacturing feedback summary"""
    return get_feedback_summary()

# UEBA Security endpoints
@router.get("/ueba/status")
async def ueba_status():
    """Get UEBA security status"""
    return ueba_monitor.get_security_dashboard()

@router.get("/ueba/anomalies")
async def get_anomalies(severity: Optional[str] = None):
    """Get detected anomalies"""
    return {"anomalies": ueba_monitor.get_anomalies(severity=severity)}

@router.post("/ueba/simulate/{anomaly_type}")
async def simulate_anomaly(anomaly_type: str):
    """Simulate an anomaly for demo"""
    return ueba_monitor.simulate_anomaly(anomaly_type)

# Fleet and dashboard endpoints
@router.get("/fleet/overview")
async def fleet_overview():
    """Get fleet overview with demand forecast"""
    vehicles = get_all_vehicles()
    return master_agent.get_fleet_overview(vehicles)

@router.get("/maintenance/summary")
async def maintenance_summary():
    """Get maintenance summary"""
    return get_all_maintenance_summary()

@router.get("/agents/status")
async def agent_status():
    """Get status of all agents"""
    return master_agent.get_agent_status()
