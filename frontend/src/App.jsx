import { useState } from 'react'
import { motion } from 'framer-motion'
import { LayoutDashboard, MessageSquare, Factory, Shield, Car } from 'lucide-react'
import Dashboard from './components/Dashboard'
import ChatInterface from './components/ChatInterface'
import InsightsDashboard from './components/InsightsDashboard'
import UEBAPanel from './components/UEBAPanel'

function App() {
    const [activeTab, setActiveTab] = useState('dashboard')
    const [selectedVehicle, setSelectedVehicle] = useState(null)

    const tabs = [
        { id: 'dashboard', label: 'Dashboard', shortLabel: 'Home', icon: LayoutDashboard },
        { id: 'chat', label: 'AI Assistant', shortLabel: 'Chat', icon: MessageSquare },
        { id: 'insights', label: 'Manufacturing', shortLabel: 'Insights', icon: Factory },
        { id: 'security', label: 'UEBA Security', shortLabel: 'UEBA', icon: Shield }
    ]

    const handleVehicleSelect = (vehicle) => {
        setSelectedVehicle(vehicle)
        if (vehicle) setActiveTab('chat')
    }

    return (
        <div className="app">
            <header className="header">
                <div className="logo">
                    <Car size={28} />
                    <span>AutoCare AI</span>
                </div>
                <nav className="nav-tabs">
                    {tabs.map(tab => {
                        const Icon = tab.icon
                        return (
                            <button
                                key={tab.id}
                                className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
                                onClick={() => setActiveTab(tab.id)}
                            >
                                <Icon size={16} />
                                <span className="tab-label-full">{tab.label}</span>
                                <span className="tab-label-short">{tab.shortLabel}</span>
                            </button>
                        )
                    })}
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
