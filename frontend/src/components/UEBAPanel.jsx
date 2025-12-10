import { useState } from 'react'
import { motion } from 'framer-motion'
import { Shield, Bot, AlertTriangle, Activity, Eye, Zap, ShieldAlert, ShieldCheck, Clock } from 'lucide-react'

const agents = [
    { id: 'master_agent', name: 'Master Agent', role: 'Orchestrator', status: 'active', actions: 45 },
    { id: 'data_analysis', name: 'Data Analysis', role: 'Telematics', status: 'active', actions: 128 },
    { id: 'diagnosis', name: 'Diagnosis', role: 'Prediction', status: 'active', actions: 67 },
    { id: 'customer_engagement', name: 'Customer Engagement', role: 'Chat', status: 'active', actions: 34 },
    { id: 'scheduling', name: 'Scheduling', role: 'Booking', status: 'active', actions: 23 },
    { id: 'feedback', name: 'Feedback', role: 'Follow-up', status: 'active', actions: 12 },
    { id: 'manufacturing_insights', name: 'Manufacturing', role: 'RCA/CAPA', status: 'active', actions: 18 },
]

const mockAnomalies = [
    { id: 'ANM1001', agent: 'scheduling_agent', type: 'unauthorized_data_access', severity: 'critical', description: 'Attempted access to telematics data', time: '2 min ago' },
    { id: 'ANM1002', agent: 'feedback_agent', type: 'unauthorized_action', severity: 'high', description: 'Attempted to modify vehicle records', time: '5 min ago' },
    { id: 'ANM1003', agent: 'data_analysis', type: 'high_frequency', severity: 'medium', description: 'Unusual action frequency: 45 actions/min', time: '12 min ago' },
]

export default function UEBAPanel() {
    const [showSimulate, setShowSimulate] = useState(false)
    const [anomalies, setAnomalies] = useState(mockAnomalies)

    const simulateAnomaly = (type) => {
        const newAnomaly = {
            id: `ANM${1000 + anomalies.length + 1}`,
            agent: type === 'unauthorized_data_access' ? 'scheduling_agent' : 'feedback_agent',
            type,
            severity: 'critical',
            description: type === 'unauthorized_data_access'
                ? 'SIMULATED: Scheduling agent accessed telematics data (unauthorized)'
                : 'SIMULATED: Feedback agent attempted data modification',
            time: 'Just now'
        }
        setAnomalies([newAnomaly, ...anomalies])
        setShowSimulate(false)
    }

    const stats = {
        total: 327,
        critical: anomalies.filter(a => a.severity === 'critical').length,
        high: anomalies.filter(a => a.severity === 'high').length,
        agentsMonitored: agents.length
    }

    return (
        <div className="dashboard-grid">
            {/* Security Status */}
            <div className="card full-width">
                <div className="card-header">
                    <h2 className="card-title"><Shield size={20} /> UEBA Security Monitor</h2>
                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                        <span className={`badge ${stats.critical > 0 ? 'danger' : 'success'}`}>
                            {stats.critical > 0 ? <><ShieldAlert size={12} /> ALERT</> : <><ShieldCheck size={12} /> SECURE</>}
                        </span>
                        <button className="btn btn-secondary" onClick={() => setShowSimulate(!showSimulate)}>
                            <Zap size={14} /> Simulate Anomaly
                        </button>
                    </div>
                </div>

                {showSimulate && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        style={{ marginBottom: '1rem', padding: '1rem', background: 'var(--bg-card)', borderRadius: 'var(--radius-md)' }}
                    >
                        <p style={{ marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Simulate an anomaly to see UEBA in action:</p>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button className="btn btn-primary" onClick={() => simulateAnomaly('unauthorized_data_access')}>
                                <Eye size={14} /> Data Access Violation
                            </button>
                            <button className="btn btn-primary" onClick={() => simulateAnomaly('unauthorized_action')}>
                                <AlertTriangle size={14} /> Unauthorized Action
                            </button>
                        </div>
                    </motion.div>
                )}

                <div className="stats-grid">
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Actions Monitored</span>
                        <span className="stat-value">{stats.total}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Critical Alerts</span>
                        <span className="stat-value danger">{stats.critical}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">High Severity</span>
                        <span className="stat-value warning">{stats.high}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Agents Monitored</span>
                        <span className="stat-value">{stats.agentsMonitored}</span>
                    </motion.div>
                </div>
            </div>

            {/* Agent Status */}
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title"><Bot size={20} /> Agent Activity</h2>
                </div>
                <div>
                    {agents.map((agent, i) => (
                        <motion.div
                            key={agent.id}
                            className="agent-node"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.05 }}
                        >
                            <div className="agent-dot" />
                            <div style={{ flex: 1 }}>
                                <div style={{ fontWeight: 600 }}>{agent.name}</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{agent.role}</div>
                            </div>
                            <span className="badge success">{agent.actions} actions</span>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Detected Anomalies */}
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title"><AlertTriangle size={20} /> Detected Anomalies</h2>
                </div>
                <div className="vehicle-list">
                    {anomalies.map((anomaly, i) => (
                        <motion.div
                            key={anomaly.id}
                            className={`alert-item ${anomaly.severity}`}
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: i * 0.05 }}
                        >
                            <span className="alert-icon">
                                {anomaly.severity === 'critical' ? <ShieldAlert size={20} /> :
                                    anomaly.severity === 'high' ? <AlertTriangle size={20} /> : <Activity size={20} />}
                            </span>
                            <div className="alert-content">
                                <div className="alert-title">{anomaly.type.replace(/_/g, ' ').toUpperCase()}</div>
                                <div className="alert-description">
                                    Agent: {anomaly.agent} • {anomaly.description}
                                </div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem', display: 'flex', alignItems: 'center', gap: '4px' }}>
                                    <Clock size={12} /> {anomaly.time}
                                </div>
                            </div>
                            <span className={`badge ${anomaly.severity === 'critical' ? 'danger' : anomaly.severity === 'high' ? 'warning' : 'info'}`}>
                                {anomaly.severity}
                            </span>
                        </motion.div>
                    ))}
                </div>
            </div>
        </div>
    )
}
