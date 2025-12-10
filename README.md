# 🚗 AutoCare AI - Autonomous Predictive Maintenance System

An Agentic AI solution for automotive OEM aftersales with Master-Worker agent orchestration, predictive maintenance, customer engagement, and manufacturing feedback loop.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Master Agent (Orchestrator)               │
├──────────┬──────────┬──────────┬──────────┬─────────────────┤
│  Data    │Diagnosis │ Customer │Scheduling│  Manufacturing  │
│ Analysis │  Agent   │Engagement│  Agent   │    Insights     │
│  Agent   │   (ML)   │  Agent   │          │     Agent       │
└──────────┴──────────┴──────────┴──────────┴─────────────────┘
                           │
                    UEBA Security Monitor
```

## ✨ Key Features

### 1. Continuous Vehicle Monitoring
- Real-time telematics data analysis
- Sensor health tracking for 10 synthetic vehicles
- Diagnostic Trouble Code (DTC) detection

### 2. Predictive Failure Detection
- ML-based failure probability scoring (RandomForest)
- Component-level risk assessment
- Priority-based alert system (P1-P4)

### 3. Autonomous Scheduling
- Smart slot recommendations
- Service center capacity optimization
- Multi-vehicle fleet scheduling

### 4. Voice/Chat AI Agent
- Natural language customer interactions
- Persuasive service recommendations
- Intelligent response generation

### 5. Manufacturing Feedback Loop
- RCA/CAPA pattern analysis
- Actionable insights for production team
- Defect reduction recommendations

### 6. UEBA Security
- Agent behavior monitoring
- Anomaly detection with alerts
- Unauthorized access prevention

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11, FastAPI, Uvicorn |
| ML/AI | scikit-learn, pandas, numpy |
| Frontend | React 18, Vite |
| Styling | Modern CSS (Glassmorphism, Dark Theme) |
| Charts | Recharts, Framer Motion |

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# API docs: http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# App: http://localhost:5173
```

## 📁 Project Structure

```
techathon/
├── backend/
│   ├── main.py              # FastAPI entry
│   ├── agents/              # AI Agents
│   │   ├── master_agent.py
│   │   ├── data_analysis.py
│   │   ├── diagnosis.py
│   │   ├── customer_engagement.py
│   │   ├── scheduling.py
│   │   ├── feedback.py
│   │   └── manufacturing_insights.py
│   ├── data/                # Synthetic data
│   ├── security/            # UEBA monitor
│   └── api/                 # REST routes
│
└── frontend/
    └── src/
        ├── App.jsx
        ├── components/
        │   ├── Dashboard.jsx
        │   ├── ChatInterface.jsx
        │   ├── InsightsDashboard.jsx
        │   └── UEBAPanel.jsx
        └── api/client.js
```

## 🔌 API Endpoints

| Endpoint | Description |
|----------|-------------|
| GET `/api/vehicles` | List all vehicles with health |
| GET `/api/vehicles/{id}` | Vehicle diagnosis |
| POST `/api/chat/start/{id}` | Start AI conversation |
| POST `/api/chat` | Send message |
| GET `/api/schedule/slots/{id}` | Get available slots |
| POST `/api/schedule/book` | Book appointment |
| GET `/api/insights` | Manufacturing insights |
| GET `/api/ueba/status` | Security status |
| POST `/api/ueba/simulate/{type}` | Demo anomaly |

## 🎯 Demo Scenarios

1. **Critical Vehicle Alert** - Select VH007 (35% health) to see urgent outreach
2. **Chat Flow** - Complete booking conversation with AI
3. **UEBA Demo** - Simulate unauthorized data access
4. **Manufacturing Insights** - View RCA patterns and CAPA progress

## 👥 Team

Built for Techathon 2024
