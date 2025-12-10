import { useState } from 'react'
import { motion } from 'framer-motion'
import { Factory, ClipboardList, Lightbulb, TrendingUp, AlertCircle, CheckCircle, Clock, FileText } from 'lucide-react'

const mockRCA = [
    { id: 'RCA001', component: 'ABS Sensor', models: ['XUV700'], occurrences: 156, severity: 'high', status: 'investigating' },
    { id: 'RCA002', component: 'Catalytic Converter', models: ['Creta', 'Venue'], occurrences: 234, severity: 'medium', status: 'capa_in_progress' },
    { id: 'RCA003', component: 'Cylinder Head Gasket', models: ['Innova Crysta'], occurrences: 67, severity: 'critical', status: 'capa_implemented' },
    { id: 'RCA004', component: 'Wiring Harness', models: ['XUV700'], occurrences: 89, severity: 'medium', status: 'investigating' },
]

const mockInsights = [
    { id: 'INS001', title: 'ABS Sensor Sealing Enhancement', priority: 'high', potential_savings: '₹8.5L', category: 'design' },
    { id: 'INS002', title: 'Fuel Injector Quality Audit', priority: 'medium', potential_savings: '₹12L', category: 'supplier' },
    { id: 'INS003', title: 'Wiring Assembly Process Review', priority: 'medium', potential_savings: '₹4.5L', category: 'process' },
]

export default function InsightsDashboard() {
    const [activeTab, setActiveTab] = useState('overview')

    const summary = {
        totalRCA: 6,
        investigating: 2,
        capaInProgress: 2,
        resolved: 2,
        potentialSavings: '₹25L'
    }

    const getStatusIcon = (status) => {
        switch (status) {
            case 'capa_implemented': return <CheckCircle size={16} style={{ color: 'var(--success)' }} />
            case 'capa_in_progress': return <Clock size={16} style={{ color: 'var(--info)' }} />
            default: return <AlertCircle size={16} style={{ color: 'var(--warning)' }} />
        }
    }

    return (
        <div className="dashboard-grid">
            {/* Summary Stats */}
            <div className="card full-width">
                <div className="card-header">
                    <h2 className="card-title"><Factory size={20} /> Manufacturing Feedback Loop</h2>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <button className={`nav-tab ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>Overview</button>
                        <button className={`nav-tab ${activeTab === 'rca' ? 'active' : ''}`} onClick={() => setActiveTab('rca')}>RCA Records</button>
                        <button className={`nav-tab ${activeTab === 'insights' ? 'active' : ''}`} onClick={() => setActiveTab('insights')}>Insights</button>
                    </div>
                </div>
                <div className="stats-grid">
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Total RCA</span>
                        <span className="stat-value">{summary.totalRCA}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Investigating</span>
                        <span className="stat-value warning">{summary.investigating}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">CAPA In Progress</span>
                        <span className="stat-value" style={{ color: 'var(--info)' }}>{summary.capaInProgress}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Resolved</span>
                        <span className="stat-value success">{summary.resolved}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Potential Savings</span>
                        <span className="stat-value success">{summary.potentialSavings}</span>
                    </motion.div>
                </div>
            </div>

            {/* RCA Records */}
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title"><ClipboardList size={20} /> Root Cause Analysis</h2>
                </div>
                <div className="vehicle-list">
                    {mockRCA.map((rca, i) => (
                        <motion.div
                            key={rca.id}
                            className={`alert-item ${rca.severity}`}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.1 }}
                        >
                            <span className="alert-icon"><FileText size={20} /></span>
                            <div className="alert-content">
                                <div className="alert-title">{rca.component}</div>
                                <div className="alert-description">
                                    {rca.models.join(', ')} • {rca.occurrences} occurrences
                                </div>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                {getStatusIcon(rca.status)}
                                <span className={`badge ${rca.status === 'capa_implemented' ? 'success' : rca.status === 'capa_in_progress' ? 'info' : 'warning'}`}>
                                    {rca.status.replace(/_/g, ' ')}
                                </span>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Manufacturing Insights */}
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title"><Lightbulb size={20} /> Actionable Insights</h2>
                </div>
                <div className="vehicle-list">
                    {mockInsights.map((insight, i) => (
                        <motion.div
                            key={insight.id}
                            className="vehicle-item"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.1 }}
                        >
                            <div className="vehicle-icon" style={{ background: insight.priority === 'high' ? 'var(--danger)' : 'var(--accent-gradient)' }}>
                                <TrendingUp size={20} />
                            </div>
                            <div className="vehicle-info">
                                <div className="vehicle-name">{insight.title}</div>
                                <div className="vehicle-meta">Category: {insight.category} • Savings: {insight.potential_savings}</div>
                            </div>
                            <span className={`badge ${insight.priority === 'high' ? 'danger' : 'warning'}`}>{insight.priority}</span>
                        </motion.div>
                    ))}
                </div>
            </div>
        </div>
    )
}
