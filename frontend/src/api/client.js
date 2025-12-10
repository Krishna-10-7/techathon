const API_BASE = '/api';

export const api = {
    // Vehicles
    async getVehicles() {
        const res = await fetch(`${API_BASE}/vehicles`);
        return res.json();
    },

    async getVehicle(id) {
        const res = await fetch(`${API_BASE}/vehicles/${id}`);
        return res.json();
    },

    async getVehicleAlerts(id) {
        const res = await fetch(`${API_BASE}/vehicles/${id}/alerts`);
        return res.json();
    },

    // Chat
    async startChat(vehicleId) {
        const res = await fetch(`${API_BASE}/chat/start/${vehicleId}`, { method: 'POST' });
        return res.json();
    },

    async sendMessage(conversationId, message) {
        const res = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversation_id: conversationId, message })
        });
        return res.json();
    },

    // Scheduling
    async getSlots(vehicleId) {
        const res = await fetch(`${API_BASE}/schedule/slots/${vehicleId}`);
        return res.json();
    },

    async bookSlot(data) {
        const res = await fetch(`${API_BASE}/schedule/book`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    async getServiceCenters() {
        const res = await fetch(`${API_BASE}/service-centers`);
        return res.json();
    },

    // Fleet
    async getFleetOverview() {
        const res = await fetch(`${API_BASE}/fleet/overview`);
        return res.json();
    },

    // Manufacturing Insights
    async getInsights() {
        const res = await fetch(`${API_BASE}/insights`);
        return res.json();
    },

    async getRCA() {
        const res = await fetch(`${API_BASE}/insights/rca`);
        return res.json();
    },

    // UEBA Security
    async getUEBAStatus() {
        const res = await fetch(`${API_BASE}/ueba/status`);
        return res.json();
    },

    async getAnomalies() {
        const res = await fetch(`${API_BASE}/ueba/anomalies`);
        return res.json();
    },

    async simulateAnomaly(type) {
        const res = await fetch(`${API_BASE}/ueba/simulate/${type}`, { method: 'POST' });
        return res.json();
    },

    // Agent Status
    async getAgentStatus() {
        const res = await fetch(`${API_BASE}/agents/status`);
        return res.json();
    }
};
