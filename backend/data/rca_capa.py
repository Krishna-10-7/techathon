"""
RCA/CAPA Data - Root Cause Analysis and Corrective Action/Preventive Action records
for manufacturing feedback loop
"""
from datetime import datetime, timedelta

# Root Cause Analysis Records
RCA_RECORDS = [
    {
        "id": "RCA001",
        "defect_code": "DEF-ABS-001",
        "component": "ABS Sensor",
        "vehicle_models": ["XUV700", "XUV500"],
        "manufacturer": "Mahindra",
        "description": "Premature failure of left front ABS wheel speed sensor",
        "occurrences": 156,
        "affected_vehicles": 89,
        "root_cause": "Inadequate sealing leading to moisture ingress in harsh conditions",
        "severity": "high",
        "detection_date": "2024-02-15",
        "status": "investigating"
    },
    {
        "id": "RCA002",
        "defect_code": "DEF-CAT-001",
        "component": "Catalytic Converter",
        "vehicle_models": ["Creta", "Venue"],
        "manufacturer": "Hyundai",
        "description": "Catalyst efficiency degradation before expected lifespan",
        "occurrences": 234,
        "affected_vehicles": 178,
        "root_cause": "Suboptimal fuel mixture causing catalyst contamination",
        "severity": "medium",
        "detection_date": "2024-01-20",
        "status": "capa_in_progress"
    },
    {
        "id": "RCA003",
        "defect_code": "DEF-ENG-001",
        "component": "Cylinder Head Gasket",
        "vehicle_models": ["Innova Crysta", "Fortuner"],
        "manufacturer": "Toyota",
        "description": "Head gasket failure in high-mileage vehicles",
        "occurrences": 67,
        "affected_vehicles": 45,
        "root_cause": "Material fatigue under extended high-temperature operation",
        "severity": "critical",
        "detection_date": "2023-11-10",
        "status": "capa_implemented"
    },
    {
        "id": "RCA004",
        "defect_code": "DEF-ELE-001",
        "component": "Wiring Harness",
        "vehicle_models": ["XUV700"],
        "manufacturer": "Mahindra",
        "description": "Intermittent electrical failures due to wiring issues",
        "occurrences": 89,
        "affected_vehicles": 62,
        "root_cause": "Connector corrosion from inadequate waterproofing",
        "severity": "medium",
        "detection_date": "2024-03-05",
        "status": "investigating"
    },
    {
        "id": "RCA005",
        "defect_code": "DEF-COOL-001",
        "component": "Thermostat",
        "vehicle_models": ["Innova Crysta"],
        "manufacturer": "Toyota",
        "description": "Thermostat stuck in open position causing overcooling",
        "occurrences": 45,
        "affected_vehicles": 38,
        "root_cause": "Wax element degradation due to prolonged coolant contamination",
        "severity": "medium",
        "detection_date": "2023-12-01",
        "status": "capa_implemented"
    },
    {
        "id": "RCA006",
        "defect_code": "DEF-FUEL-001",
        "component": "Fuel Injector",
        "vehicle_models": ["Creta", "i20"],
        "manufacturer": "Hyundai",
        "description": "Fuel injector clogging causing lean mixture",
        "occurrences": 178,
        "affected_vehicles": 134,
        "root_cause": "Deposit buildup from fuel quality variations",
        "severity": "high",
        "detection_date": "2024-04-10",
        "status": "capa_in_progress"
    }
]

# Corrective Action / Preventive Action Records
CAPA_RECORDS = [
    {
        "id": "CAPA001",
        "rca_id": "RCA003",
        "type": "corrective",
        "action": "Upgraded head gasket material specification",
        "description": "Changed to multi-layer steel (MLS) gasket with improved heat resistance",
        "implementation_date": "2024-02-01",
        "manufacturing_update": True,
        "cost_impact": 120,  # per unit increase
        "effectiveness": 95,  # percentage
        "status": "implemented"
    },
    {
        "id": "CAPA002",
        "rca_id": "RCA003",
        "type": "preventive",
        "action": "Enhanced cooling system maintenance protocol",
        "description": "Reduced coolant flush interval from 100k to 60k km for affected models",
        "implementation_date": "2024-02-15",
        "manufacturing_update": False,
        "cost_impact": 0,
        "effectiveness": 80,
        "status": "implemented"
    },
    {
        "id": "CAPA003",
        "rca_id": "RCA005",
        "type": "corrective",
        "action": "Thermostat redesign with improved wax element",
        "description": "New thermostat with synthetic wax element resistant to contamination",
        "implementation_date": "2024-01-20",
        "manufacturing_update": True,
        "cost_impact": 45,
        "effectiveness": 92,
        "status": "implemented"
    },
    {
        "id": "CAPA004",
        "rca_id": "RCA002",
        "type": "corrective",
        "action": "ECU software update for fuel mixture optimization",
        "description": "Updated fuel mapping to prevent lean conditions under various loads",
        "implementation_date": "2024-05-01",
        "manufacturing_update": True,
        "cost_impact": 0,
        "effectiveness": 78,
        "status": "in_progress"
    },
    {
        "id": "CAPA005",
        "rca_id": "RCA006",
        "type": "preventive",
        "action": "Fuel system cleaning service recommendation",
        "description": "Added fuel injector cleaning to 40k km service schedule",
        "implementation_date": "2024-05-15",
        "manufacturing_update": False,
        "cost_impact": 0,
        "effectiveness": 70,
        "status": "in_progress"
    },
    {
        "id": "CAPA006",
        "rca_id": "RCA001",
        "type": "corrective",
        "action": "ABS sensor housing redesign",
        "description": "New IP68-rated housing with improved sealing for sensor protection",
        "implementation_date": None,
        "manufacturing_update": True,
        "cost_impact": 85,
        "effectiveness": None,
        "status": "pending"
    },
    {
        "id": "CAPA007",
        "rca_id": "RCA004",
        "type": "corrective",
        "action": "Connector redesign with enhanced waterproofing",
        "description": "New connector design with conformal coating on terminals",
        "implementation_date": None,
        "manufacturing_update": True,
        "cost_impact": 35,
        "effectiveness": None,
        "status": "pending"
    }
]

# Manufacturing insights generated from patterns
MANUFACTURING_INSIGHTS = [
    {
        "id": "INS001",
        "category": "design_improvement",
        "priority": "high",
        "title": "ABS Sensor Sealing Enhancement Required",
        "description": "Pattern of ABS sensor failures in XUV700 indicates inadequate sealing. Recommend IP68 rating for new production.",
        "affected_components": ["ABS Sensor"],
        "affected_models": ["XUV700", "XUV500"],
        "potential_savings": 850000,  # INR
        "generated_date": "2024-12-01"
    },
    {
        "id": "INS002",
        "category": "supplier_quality",
        "priority": "medium",
        "title": "Fuel Injector Quality Audit Recommended",
        "description": "Recurring injector issues suggest supplier quality variation. Recommend supplier audit and incoming inspection enhancement.",
        "affected_components": ["Fuel Injector"],
        "affected_models": ["Creta", "i20"],
        "potential_savings": 1200000,
        "generated_date": "2024-12-05"
    },
    {
        "id": "INS003",
        "category": "process_improvement",
        "priority": "medium",
        "title": "Wiring Harness Assembly Process Review",
        "description": "Electrical failures pattern suggests connector application process needs validation. Recommend assembly line audit.",
        "affected_components": ["Wiring Harness", "Connectors"],
        "affected_models": ["XUV700"],
        "potential_savings": 450000,
        "generated_date": "2024-12-08"
    }
]


def get_rca_records(status: str = None, severity: str = None) -> list:
    """Get RCA records with optional filtering"""
    records = RCA_RECORDS
    if status:
        records = [r for r in records if r["status"] == status]
    if severity:
        records = [r for r in records if r["severity"] == severity]
    return records


def get_capa_for_rca(rca_id: str) -> list:
    """Get CAPA records for a specific RCA"""
    return [c for c in CAPA_RECORDS if c["rca_id"] == rca_id]


def get_all_capa(status: str = None) -> list:
    """Get all CAPA records"""
    if status:
        return [c for c in CAPA_RECORDS if c["status"] == status]
    return CAPA_RECORDS


def get_manufacturing_insights(priority: str = None) -> list:
    """Get manufacturing insights"""
    if priority:
        return [i for i in MANUFACTURING_INSIGHTS if i["priority"] == priority]
    return MANUFACTURING_INSIGHTS


def get_component_defect_pattern(component: str) -> dict:
    """Analyze defect patterns for a component"""
    related_rca = [r for r in RCA_RECORDS if r["component"].lower() == component.lower()]
    
    if not related_rca:
        return {"component": component, "pattern": "no_issues_detected"}
    
    total_occurrences = sum(r["occurrences"] for r in related_rca)
    total_affected = sum(r["affected_vehicles"] for r in related_rca)
    
    return {
        "component": component,
        "total_rca_records": len(related_rca),
        "total_occurrences": total_occurrences,
        "total_affected_vehicles": total_affected,
        "severity_distribution": {
            "critical": sum(1 for r in related_rca if r["severity"] == "critical"),
            "high": sum(1 for r in related_rca if r["severity"] == "high"),
            "medium": sum(1 for r in related_rca if r["severity"] == "medium")
        },
        "related_capa": len([c for c in CAPA_RECORDS if any(
            c["rca_id"] == r["id"] for r in related_rca
        )])
    }


def generate_insight_from_prediction(vehicle_id: str, component: str, failure_prob: float) -> dict:
    """Generate manufacturing insight from a prediction"""
    # Check if similar pattern exists
    existing_rca = [r for r in RCA_RECORDS if r["component"] == component]
    
    insight = {
        "type": "predictive_pattern",
        "vehicle_id": vehicle_id,
        "component": component,
        "failure_probability": failure_prob,
        "timestamp": datetime.now().isoformat()
    }
    
    if existing_rca:
        insight["related_rca"] = existing_rca[0]["id"]
        insight["recommendation"] = f"Pattern matches existing RCA {existing_rca[0]['id']}. Consider proactive intervention."
    else:
        insight["recommendation"] = "New failure pattern detected. Recommend creating RCA for investigation."
    
    return insight


def get_feedback_summary() -> dict:
    """Get summary of manufacturing feedback loop status"""
    return {
        "total_rca": len(RCA_RECORDS),
        "active_investigations": sum(1 for r in RCA_RECORDS if r["status"] == "investigating"),
        "capa_in_progress": sum(1 for r in RCA_RECORDS if r["status"] == "capa_in_progress"),
        "resolved": sum(1 for r in RCA_RECORDS if r["status"] == "capa_implemented"),
        "total_capa": len(CAPA_RECORDS),
        "implemented_capa": sum(1 for c in CAPA_RECORDS if c["status"] == "implemented"),
        "pending_insights": len(MANUFACTURING_INSIGHTS),
        "potential_savings": sum(i["potential_savings"] for i in MANUFACTURING_INSIGHTS)
    }
