import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Dashboard from './components/Dashboard'
import VehicleDetail from './components/VehicleDetail'
import ChatInterface from './components/ChatInterface'
import InsightsDashboard from './components/InsightsDashboard'
import UEBAPanel from './components/UEBAPanel'

function App() {
    const [activeTab, setActiveTab] = useState('dashboard')
    const [selectedVehicle, setSelectedVehicle] = useState(null)

    const tabs = [
        { id: 'dashboard', label: '📊 Dashboard', icon: '📊' },
        { id: 'chat', label: '💬 AI Assistant', icon: '💬' },
        { id: 'insights', label: '🏭 Manufacturing', icon: '🏭' },
        { id: 'security', label: '🔐 UEBA Security', icon: '🔐' }
    ]

    const handleVehicleSelect = (vehicle) => {
        setSelectedVehicle(vehicle)
        if (vehicle) setActiveTab('chat')
    }

    return (
        <div className="app">
            <header className="header">
                <div className="logo">
                    <span>🚗</span>
                    <span>AutoCare AI</span>
                </div>
                <nav className="nav-tabs">
                    {tabs.map(tab => (
                        <button
                            key={tab.id}
                            className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
                            onClick={() => setActiveTab(tab.id)}
                        >
                            {tab.label}
                        </button>
                    ))}
                </nav>
            </header>

            <motion.main
                className="main-content"
                key={activeTab}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2 }}
            >
                {activeTab === 'dashboard' && (
                    <Dashboard
                        onVehicleSelect={handleVehicleSelect}
                        selectedVehicle={selectedVehicle}
                    />
                )}
                {activeTab === 'chat' && (
                    <ChatInterface vehicle={selectedVehicle} />
                )}
                {activeTab === 'insights' && <InsightsDashboard />}
                {activeTab === 'security' && <UEBAPanel />}
            </motion.main>
        </div>
    )
}

export default App
