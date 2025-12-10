import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

// Mock data for demo (when backend is not running)
const mockVehicles = [
    { id: 'VH001', make: 'Tata', model: 'Nexon EV', owner: { name: 'Rahul Sharma' }, odometer: 25420, city: 'Mumbai', health_score: 92, active_alerts: 0 },
    { id: 'VH002', make: 'Mahindra', model: 'XUV700', owner: { name: 'Priya Patel' }, odometer: 45780, city: 'Delhi', health_score: 58, active_alerts: 2 },
    { id: 'VH003', make: 'Maruti', model: 'Grand Vitara', owner: { name: 'Amit Kumar' }, odometer: 18950, city: 'Bangalore', health_score: 95, active_alerts: 0 },
    { id: 'VH004', make: 'Hyundai', model: 'Creta', owner: { name: 'Sneha Reddy' }, odometer: 62340, city: 'Hyderabad', health_score: 45, active_alerts: 3 },
    { id: 'VH005', make: 'Kia', model: 'Seltos', owner: { name: 'Vikram Singh' }, odometer: 38920, city: 'Chennai', health_score: 78, active_alerts: 1 },
    { id: 'VH006', make: 'Tata', model: 'Harrier', owner: { name: 'Neha Gupta' }, odometer: 21560, city: 'Pune', health_score: 88, active_alerts: 0 },
    { id: 'VH007', make: 'Toyota', model: 'Innova Crysta', owner: { name: 'Rajesh Menon' }, odometer: 89450, city: 'Kochi', health_score: 35, active_alerts: 4 },
    { id: 'VH008', make: 'Honda', model: 'City', owner: { name: 'Ananya Joshi' }, odometer: 34120, city: 'Ahmedabad', health_score: 82, active_alerts: 0 },
    { id: 'VH009', make: 'Mahindra', model: 'Thar', owner: { name: 'Arjun Nair' }, odometer: 15780, city: 'Jaipur', health_score: 90, active_alerts: 0 },
    { id: 'VH010', make: 'Skoda', model: 'Kushaq', owner: { name: 'Meera Iyer' }, odometer: 42890, city: 'Kolkata', health_score: 72, active_alerts: 1 }
]

export default function Dashboard({ onVehicleSelect, selectedVehicle }) {
    const [vehicles, setVehicles] = useState(mockVehicles)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        // Try to fetch from API, fallback to mock
        fetch('/api/vehicles')
            .then(res => res.json())
            .then(data => setVehicles(data.vehicles || mockVehicles))
            .catch(() => setVehicles(mockVehicles))
    }, [])

    const stats = {
        total: vehicles.length,
        healthy: vehicles.filter(v => v.health_score >= 80).length,
        warning: vehicles.filter(v => v.health_score >= 50 && v.health_score < 80).length,
        critical: vehicles.filter(v => v.health_score < 50).length,
        totalAlerts: vehicles.reduce((sum, v) => sum + v.active_alerts, 0)
    }

    const getHealthClass = (score) => {
        if (score >= 80) return 'good'
        if (score >= 50) return 'warning'
        return 'critical'
    }

    return (
        <div className="dashboard-grid">
            {/* Stats Overview */}
            <div className="card full-width">
                <div className="card-header">
                    <h2 className="card-title">🚗 Fleet Overview</h2>
                    <span className="badge info">{vehicles.length} Vehicles</span>
                </div>
                <div className="stats-grid">
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Total Vehicles</span>
                        <span className="stat-value">{stats.total}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Healthy</span>
                        <span className="stat-value success">{stats.healthy}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Warning</span>
                        <span className="stat-value warning">{stats.warning}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Critical</span>
                        <span className="stat-value danger">{stats.critical}</span>
                    </motion.div>
                    <motion.div className="stat-card" whileHover={{ scale: 1.02 }}>
                        <span className="stat-label">Active Alerts</span>
                        <span className="stat-value danger">{stats.totalAlerts}</span>
                    </motion.div>
                </div>
            </div>

            {/* Vehicle List */}
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title">📋 Vehicle Status</h2>
                </div>
                <div className="vehicle-list">
                    {vehicles.map((vehicle, i) => (
                        <motion.div
                            key={vehicle.id}
                            className={`vehicle-item ${selectedVehicle?.id === vehicle.id ? 'selected' : ''}`}
                            onClick={() => onVehicleSelect(vehicle)}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.05 }}
                            whileHover={{ scale: 1.01 }}
                            style={{ borderColor: selectedVehicle?.id === vehicle.id ? 'var(--accent-primary)' : 'transparent' }}
                        >
                            <div className="vehicle-icon">🚗</div>
                            <div className="vehicle-info">
                                <div className="vehicle-name">{vehicle.make} {vehicle.model}</div>
                                <div className="vehicle-meta">{vehicle.owner.name} • {vehicle.city} • {vehicle.odometer.toLocaleString()} km</div>
                            </div>
                            <div className="vehicle-health">
                                <div className="health-bar">
                                    <div
                                        className={`health-fill ${getHealthClass(vehicle.health_score)}`}
                                        style={{ width: `${vehicle.health_score}%` }}
                                    />
                                </div>
                                <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>{vehicle.health_score}%</span>
                                {vehicle.active_alerts > 0 && (
                                    <span className="badge danger">{vehicle.active_alerts}</span>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Priority Alerts */}
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title">⚠️ Priority Alerts</h2>
                </div>
                <div className="vehicle-list">
                    {vehicles.filter(v => v.health_score < 60).map((vehicle, i) => (
                        <motion.div
                            key={vehicle.id}
                            className="alert-item critical"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: i * 0.1 }}
                        >
                            <span className="alert-icon">🚨</span>
                            <div className="alert-content">
                                <div className="alert-title">{vehicle.make} {vehicle.model} - {vehicle.owner.name}</div>
                                <div className="alert-description">
                                    Health score at {vehicle.health_score}% • {vehicle.active_alerts} active issues detected
                                </div>
                            </div>
                            <button className="btn btn-primary" onClick={() => onVehicleSelect(vehicle)}>
                                Contact
                            </button>
                        </motion.div>
                    ))}
                    {vehicles.filter(v => v.health_score < 60).length === 0 && (
                        <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                            ✅ No critical alerts at this time
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
