import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

export default function VehicleDetail({ vehicle }) {
    if (!vehicle) return null

    const sensors = [
        { name: 'Engine Temp', value: 92, unit: '°C', status: vehicle.health_score < 50 ? 'warning' : 'normal' },
        { name: 'Oil Pressure', value: 45, unit: 'psi', status: 'normal' },
        { name: 'Battery', value: 12.6, unit: 'V', status: vehicle.health_score < 60 ? 'warning' : 'normal' },
        { name: 'Brake Wear', value: vehicle.health_score < 50 ? 85 : 45, unit: '%', status: vehicle.health_score < 50 ? 'critical' : 'normal' },
        { name: 'Tire Pressure', value: 32, unit: 'psi', status: 'normal' },
        { name: 'Coolant Level', value: 78, unit: '%', status: 'normal' },
    ]

    return (
        <div className="card">
            <div className="card-header">
                <h2 className="card-title">📊 Real-Time Sensors</h2>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '1rem' }}>
                {sensors.map((sensor, i) => (
                    <motion.div
                        key={sensor.name}
                        className="stat-card"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: i * 0.05 }}
                    >
                        <span className="stat-label">{sensor.name}</span>
                        <span className={`stat-value ${sensor.status === 'critical' ? 'danger' : sensor.status === 'warning' ? 'warning' : ''}`}
                            style={{ fontSize: '1.5rem' }}>
                            {sensor.value}{sensor.unit}
                        </span>
                        <span className={`badge ${sensor.status === 'critical' ? 'danger' : sensor.status === 'warning' ? 'warning' : 'success'}`}>
                            {sensor.status}
                        </span>
                    </motion.div>
                ))}
            </div>
        </div>
    )
}
