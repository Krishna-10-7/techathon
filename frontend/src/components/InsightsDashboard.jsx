import { useState } from 'react'
import { motion } from 'framer-motion'
import { Factory, ClipboardList, Lightbulb, TrendingUp, AlertCircle, CheckCircle, Clock, FileText, BarChart3, ArrowRight, Wrench } from 'lucide-react'

const mockRCA = [
    { id: 'RCA001', defect_code: 'DEF-ABS-001', component: 'ABS Sensor', models: ['XUV700'], occurrences: 156, severity: 'high', status: 'investigating', root_cause: 'Water ingress through sensor housing seal', affected_vehicles: 234 },
    { id: 'RCA002', defect_code: 'DEF-CAT-002', component: 'Catalytic Converter', models: ['Creta', 'Venue'], occurrences: 234, severity: 'medium', status: 'capa_in_progress', root_cause: 'Substandard substrate material from Batch #4521', affected_vehicles: 189 },
    { id: 'RCA003', defect_code: 'DEF-ENG-003', component: 'Cylinder Head Gasket', models: ['Innova Crysta'], occurrences: 67, severity: 'critical', status: 'capa_implemented', root_cause: 'Torque spec deviation in assembly line B2', affected_vehicles: 67 },
    { id: 'RCA004', defect_code: 'DEF-ELC-004', component: 'Wiring Harness', models: ['XUV700'], occurrences: 89, severity: 'medium', status: 'investigating', root_cause: 'Connector degradation under high temperature', affected_vehicles: 112 },
]

const mockCAPA = [
    { id: 'CAPA001', rca_id: 'RCA003', action: 'Updated torque specifications from 45Nm to 52Nm', type: 'corrective', status: 'implemented', effectiveness: 98 },
    { id: 'CAPA002', rca_id: 'RCA002', action: 'Supplier quality audit initiated for substrate batches', type: 'corrective', status: 'in_progress', effectiveness: null },
    { id: 'CAPA003', rca_id: 'RCA003', action: 'Added torque verification step in QC checklist', type: 'preventive', status: 'implemented', effectiveness: 100 },
    { id: 'CAPA004', rca_id: 'RCA001', action: 'Redesign sensor housing with improved IP67 sealing', type: 'preventive', status: 'pending', effectiveness: null },
]

const mockInsights = [
    { id: 'INS001', title: 'ABS Sensor Sealing Enhancement', description: 'Implement improved IP67 sealing design based on RCA-001 findings. Reduces water ingress by 95%.', priority: 'high', potential_savings: '₹8.5L', category: 'design', impact: 'Affects 234 vehicles in field' },
    { id: 'INS002', title: 'Fuel Injector Quality Audit', description: 'Initiate supplier quality program for injector batches. 3 suppliers flagged for variation.', priority: 'medium', potential_savings: '₹12L', category: 'supplier', impact: 'Proactive - prevents future issues' },
    { id: 'INS003', title: 'Wiring Assembly Process Review', description: 'Review connector crimping process on Line 3. Temperature cycle testing recommended.', priority: 'medium', potential_savings: '₹4.5L', category: 'process', impact: 'Affects 112 vehicles' },
    { id: 'INS004', title: 'Predictive Model Improvement', description: 'Engine temperature prediction model shows 15% improvement after retraining with field data.', priority: 'low', potential_savings: '₹2L', category: 'analytics', impact: 'Better prediction accuracy' },
]

export default function InsightsDashboard() {
    const [activeTab, setActiveTab] = useState('overview')

    const summary = {
        totalRCA: mockRCA.length,
        investigating: mockRCA.filter(r => r.status === 'investigating').length,
        capaInProgress: mockRCA.filter(r => r.status === 'capa_in_progress').length,
        resolved: mockRCA.filter(r => r.status === 'capa_implemented').length,
        potentialSavings: '₹27L',
        affectedVehicles: mockRCA.reduce((sum, r) => sum + r.affected_vehicles, 0)
    }

    const getStatusIcon = (status) => {
        switch (status) {
            case 'capa_implemented': case 'implemented': return <CheckCircle size={16} style={{ color: 'var(--success)' }} />
            case 'capa_in_progress': case 'in_progress': return <Clock size={16} style={{ color: 'var(--info)' }} />
            default: return <AlertCircle size={16} style={{ color: 'var(--warning)' }} />
        }
    }

    return (
        <div className="dashboard-grid">
            {/* Header with Tabs */}
            <div className="card full-width">
                <div className="card-header">
                    <h2 className="card-title"><Factory size={20} /> Manufacturing Feedback Loop</h2>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <button className={`nav-tab ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>
                            <BarChart3 size={14} /> Overview
                        </button>
                        <button className={`nav-tab ${activeTab === 'rca' ? 'active' : ''}`} onClick={() => setActiveTab('rca')}>
                            <ClipboardList size={14} /> RCA Records
                        </button>
                        <button className={`nav-tab ${activeTab === 'insights' ? 'active' : ''}`} onClick={() => setActiveTab('insights')}>
                            <Lightbulb size={14} /> Insights
                        </button>
                    </div>
                </div>

                {/* Stats - Always visible */}
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

            {/* OVERVIEW TAB */}
            {activeTab === 'overview' && (
                <>
                    <div className="card">
                        <div className="card-header">
                            <h2 className="card-title"><TrendingUp size={20} /> Recent Activity</h2>
                        </div>
                        <div className="vehicle-list">
                            <div className="alert-item medium" style={{ borderLeftColor: 'var(--info)' }}>
                                <span className="alert-icon"><CheckCircle size={20} style={{ color: 'var(--success)' }} /></span>
                                <div className="alert-content">
                                    <div className="alert-title">CAPA Implemented - Cylinder Head Gasket</div>
                                    <div className="alert-description">Torque spec updated. 98% effectiveness confirmed.</div>
                                </div>
                                <span className="badge success">Completed</span>
                            </div>
                            <div className="alert-item high">
                                <span className="alert-icon"><Wrench size={20} /></span>
                                <div className="alert-content">
                                    <div className="alert-title">New RCA Opened - ABS Sensor</div>
                                    <div className="alert-description">156 occurrences detected. Investigation started.</div>
                                </div>
                                <span className="badge warning">In Progress</span>
                            </div>
                            <div className="alert-item medium" style={{ borderLeftColor: 'var(--accent-primary)' }}>
                                <span className="alert-icon"><Lightbulb size={20} /></span>
                                <div className="alert-content">
                                    <div className="alert-title">New Insight Generated</div>
                                    <div className="alert-description">AI detected pattern in fuel injector failures across 3 suppliers.</div>
                                </div>
                                <span className="badge info">Review</span>
                            </div>
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <h2 className="card-title"><BarChart3 size={20} /> Defect Distribution</h2>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {mockRCA.map(rca => (
                                <div key={rca.id} style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                    <span style={{ width: '120px', fontSize: '0.875rem' }}>{rca.component}</span>
                                    <div style={{ flex: 1, height: '24px', background: 'var(--bg-secondary)', borderRadius: '4px', overflow: 'hidden' }}>
                                        <motion.div
                                            initial={{ width: 0 }}
                                            animate={{ width: `${(rca.occurrences / 250) * 100}%` }}
                                            transition={{ duration: 0.8, delay: 0.2 }}
                                            style={{
                                                height: '100%',
                                                background: rca.severity === 'critical' ? 'var(--danger)' : rca.severity === 'high' ? 'var(--warning)' : 'var(--info)',
                                                borderRadius: '4px'
                                            }}
                                        />
                                    </div>
                                    <span style={{ width: '50px', fontSize: '0.875rem', fontWeight: 600 }}>{rca.occurrences}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </>
            )}

            {/* RCA RECORDS TAB */}
            {activeTab === 'rca' && (
                <>
                    <div className="card">
                        <div className="card-header">
                            <h2 className="card-title"><ClipboardList size={20} /> Root Cause Analysis Records</h2>
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
                                        <div className="alert-title">{rca.defect_code}: {rca.component}</div>
                                        <div className="alert-description">
                                            <strong>Root Cause:</strong> {rca.root_cause}
                                        </div>
                                        <div className="alert-description" style={{ marginTop: '4px' }}>
                                            Models: {rca.models.join(', ')} • {rca.affected_vehicles} affected vehicles
                                        </div>
                                    </div>
                                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.25rem' }}>
                                        {getStatusIcon(rca.status)}
                                        <span className={`badge ${rca.status === 'capa_implemented' ? 'success' : rca.status === 'capa_in_progress' ? 'info' : 'warning'}`}>
                                            {rca.status.replace(/_/g, ' ')}
                                        </span>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <h2 className="card-title"><Wrench size={20} /> CAPA Actions</h2>
                        </div>
                        <div className="vehicle-list">
                            {mockCAPA.map((capa, i) => (
                                <motion.div
                                    key={capa.id}
                                    className="vehicle-item"
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: i * 0.1 }}
                                >
                                    <div className="vehicle-icon" style={{ background: capa.type === 'corrective' ? 'var(--warning)' : 'var(--info)' }}>
                                        {capa.type === 'corrective' ? <Wrench size={20} /> : <CheckCircle size={20} />}
                                    </div>
                                    <div className="vehicle-info">
                                        <div className="vehicle-name">{capa.action}</div>
                                        <div className="vehicle-meta">
                                            Linked to {capa.rca_id} • Type: {capa.type}
                                            {capa.effectiveness && ` • ${capa.effectiveness}% effective`}
                                        </div>
                                    </div>
                                    {getStatusIcon(capa.status)}
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </>
            )}

            {/* INSIGHTS TAB */}
            {activeTab === 'insights' && (
                <>
                    <div className="card full-width">
                        <div className="card-header">
                            <h2 className="card-title"><Lightbulb size={20} /> AI-Generated Manufacturing Insights</h2>
                        </div>
                        <div className="vehicle-list">
                            {mockInsights.map((insight, i) => (
                                <motion.div
                                    key={insight.id}
                                    className="vehicle-item"
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: i * 0.1 }}
                                    style={{ flexDirection: 'column', alignItems: 'stretch', gap: '0.75rem' }}
                                >
                                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                                        <div className="vehicle-icon" style={{ background: insight.priority === 'high' ? 'var(--danger)' : insight.priority === 'medium' ? 'var(--warning)' : 'var(--accent-gradient)' }}>
                                            <TrendingUp size={20} />
                                        </div>
                                        <div style={{ flex: 1 }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                                                <span style={{ fontWeight: 600 }}>{insight.title}</span>
                                                <span className={`badge ${insight.priority === 'high' ? 'danger' : insight.priority === 'medium' ? 'warning' : 'info'}`}>
                                                    {insight.priority}
                                                </span>
                                                <span className="badge success">{insight.potential_savings}</span>
                                            </div>
                                            <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                                {insight.description}
                                            </div>
                                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', gap: '1rem' }}>
                                                <span>Category: <strong>{insight.category}</strong></span>
                                                <span>Impact: {insight.impact}</span>
                                            </div>
                                        </div>
                                        <button className="btn btn-secondary" style={{ alignSelf: 'center' }}>
                                            <ArrowRight size={14} /> Action
                                        </button>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </>
            )}
        </div>
    )
}
