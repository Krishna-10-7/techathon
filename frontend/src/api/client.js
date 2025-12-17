const API_BASE = '/api';

// Mock data for demo mode (when backend is unavailable)
const MOCK_VEHICLES = [
    { id: 'VH001', make: 'Tata', model: 'Nexon EV', year: 2023, health_score: 92, status: 'Good', last_service: '2024-10-15' },
    { id: 'VH002', make: 'Mahindra', model: 'XUV700', year: 2022, health_score: 78, status: 'Fair', last_service: '2024-08-20' },
    { id: 'VH003', make: 'Maruti', model: 'Grand Vitara', year: 2023, health_score: 85, status: 'Good', last_service: '2024-09-10' },
    { id: 'VH004', make: 'Hyundai', model: 'Creta', year: 2021, health_score: 65, status: 'Needs Attention', last_service: '2024-06-05' },
    { id: 'VH005', make: 'Kia', model: 'Seltos', year: 2022, health_score: 88, status: 'Good', last_service: '2024-11-01' },
    { id: 'VH007', make: 'Tata', model: 'Harrier', year: 2020, health_score: 35, status: 'Critical', last_service: '2024-03-15' },
];

const MOCK_INSIGHTS = {
    patterns: [
        { component: 'Brake Pads', occurrences: 45, severity: 'High', recommendation: 'Review supplier quality' },
        { component: 'Battery', occurrences: 32, severity: 'Medium', recommendation: 'Update charging protocol' },
        { component: 'Suspension', occurrences: 28, severity: 'Medium', recommendation: 'Improve road testing' },
    ],
    capa_progress: 67,
    defect_reduction: 23,
};

const MOCK_UEBA = {
    status: 'Active',
    agents_monitored: 6,
    anomalies_detected: 2,
    last_alert: '2024-12-15T10:30:00Z',
    alerts: [
        { type: 'Unauthorized Access Attempt', agent: 'Scheduling Agent', timestamp: '2024-12-15T10:30:00Z', severity: 'High' },
        { type: 'Unusual Data Query', agent: 'Data Analysis Agent', timestamp: '2024-12-14T15:45:00Z', severity: 'Medium' },
    ]
};

async function safeFetch(url, options = {}) {
    try {
        const res = await fetch(url, options);
        if (!res.ok) throw new Error('API unavailable');
        return res.json();
    } catch (e) {
        return null; // Return null to trigger mock data
    }
}

export const api = {
    // Vehicles
    async getVehicles() {
        const data = await safeFetch(`${API_BASE}/vehicles`);
        return data || MOCK_VEHICLES;
    },

    async getVehicle(id) {
        const data = await safeFetch(`${API_BASE}/vehicles/${id}`);
        return data || MOCK_VEHICLES.find(v => v.id === id) || MOCK_VEHICLES[0];
    },

    async getVehicleAlerts(id) {
        const data = await safeFetch(`${API_BASE}/vehicles/${id}/alerts`);
        return data || [{ type: 'Brake Warning', severity: 'High', message: 'Brake pads need replacement soon' }];
    },

    // Chat
    async startChat(vehicleId) {
        const data = await safeFetch(`${API_BASE}/chat/start/${vehicleId}`, { method: 'POST' });
        return data || { conversation_id: 'demo-123', message: 'Hello! I can help you with your vehicle maintenance. This is demo mode.' };
    },

    async sendMessage(conversationId, message) {
        const data = await safeFetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversation_id: conversationId, message })
        });
        return data || { response: 'This is demo mode. Backend is not connected. Your message: ' + message };
    },

    // Scheduling
    async getSlots(vehicleId) {
        const data = await safeFetch(`${API_BASE}/schedule/slots/${vehicleId}`);
        return data || [
            { id: 1, date: '2024-12-20', time: '10:00 AM', center: 'AutoCare Mumbai' },
            { id: 2, date: '2024-12-21', time: '2:00 PM', center: 'AutoCare Pune' },
        ];
    },

    async bookSlot(data) {
        const res = await safeFetch(`${API_BASE}/schedule/book`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res || { success: true, message: 'Demo booking confirmed!' };
    },

    async getServiceCenters() {
        const data = await safeFetch(`${API_BASE}/service-centers`);
        return data || [
            { id: 1, name: 'AutoCare Mumbai', location: 'Mumbai', capacity: 20 },
            { id: 2, name: 'AutoCare Pune', location: 'Pune', capacity: 15 },
        ];
    },

    // Fleet
    async getFleetOverview() {
        const data = await safeFetch(`${API_BASE}/fleet/overview`);
        return data || { total: 10, healthy: 6, attention: 3, critical: 1 };
    },

    // Manufacturing Insights
    async getInsights() {
        const data = await safeFetch(`${API_BASE}/insights`);
        return data || MOCK_INSIGHTS;
    },

    async getRCA() {
        const data = await safeFetch(`${API_BASE}/insights/rca`);
        return data || MOCK_INSIGHTS.patterns;
    },

    // UEBA Security
    async getUEBAStatus() {
        const data = await safeFetch(`${API_BASE}/ueba/status`);
        return data || MOCK_UEBA;
    },

    async getAnomalies() {
        const data = await safeFetch(`${API_BASE}/ueba/anomalies`);
        return data || MOCK_UEBA.alerts;
    },

    async simulateAnomaly(type) {
        const data = await safeFetch(`${API_BASE}/ueba/simulate/${type}`, { method: 'POST' });
        return data || { success: true, message: 'Demo anomaly simulated: ' + type };
    },

    // Agent Status
    async getAgentStatus() {
        const data = await safeFetch(`${API_BASE}/agents/status`);
        return data || [
            { name: 'Master Agent', status: 'Active' },
            { name: 'Data Analysis', status: 'Active' },
            { name: 'Diagnosis', status: 'Active' },
            { name: 'Customer Engagement', status: 'Active' },
            { name: 'Scheduling', status: 'Active' },
            { name: 'Manufacturing Insights', status: 'Active' },
        ];
    }
};
