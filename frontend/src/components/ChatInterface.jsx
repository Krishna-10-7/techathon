import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Car, User, MapPin, Gauge, AlertCircle, Mic, Send, Calendar, CheckCircle } from 'lucide-react'

export default function ChatInterface({ vehicle }) {
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState('')
    const [conversationId, setConversationId] = useState(null)
    const [suggestions, setSuggestions] = useState(['Yes, schedule now', 'Tell me more', 'How much?', 'Not now'])
    const [isTyping, setIsTyping] = useState(false)

    const startConversation = async () => {
        if (!vehicle) return

        setIsTyping(true)

        let opening = ''
        if (vehicle.health_score < 50) {
            opening = `Hello ${vehicle.owner.name.split(' ')[0]}! This is an urgent notification from AutoCare AI.\n\nOur monitoring system has detected critical issues with your ${vehicle.make} ${vehicle.model}. We've identified potential problems that require immediate attention.\n\nFor your safety, we strongly recommend scheduling a service appointment within 24 hours. Would you like me to find the nearest available slot?`
        } else if (vehicle.health_score < 70) {
            opening = `Hi ${vehicle.owner.name.split(' ')[0]}! This is your AutoCare AI assistant.\n\nI've been monitoring your ${vehicle.make} ${vehicle.model} and noticed some trends I'd like to discuss. Our predictive analysis indicates some components may need attention soon.\n\nCatching issues early can prevent costly repairs! Would you like to hear more, or schedule a preventive checkup?`
        } else {
            opening = `Hello ${vehicle.owner.name.split(' ')[0]}! Your friendly AutoCare AI here.\n\nJust checking in on your ${vehicle.make} ${vehicle.model}! With ${vehicle.odometer.toLocaleString()} km on the clock, your vehicle is looking good.\n\nWould you like to schedule a routine maintenance check?`
        }

        setTimeout(() => {
            setMessages([{ type: 'bot', text: opening }])
            setConversationId(`conv_${vehicle.id}_${Date.now()}`)
            setIsTyping(false)
        }, 1000)
    }

    const sendMessage = async (text) => {
        if (!text.trim()) return

        setMessages(prev => [...prev, { type: 'user', text }])
        setInput('')
        setIsTyping(true)

        setTimeout(() => {
            let response = ''
            let newSuggestions = []
            const lowerText = text.toLowerCase()

            if (lowerText.includes('yes') || lowerText.includes('schedule') || lowerText.includes('book')) {
                response = `Wonderful! I'm glad you're taking care of your vehicle.\n\nLet me check available slots at service centers near ${vehicle.city}. Based on your location, I have these options:\n\n• Tomorrow at 9:00 AM\n• Tomorrow at 2:00 PM\n• Day after at 10:00 AM\n\nWhich works best for you?`
                newSuggestions = ['Tomorrow morning', 'Tomorrow afternoon', 'Day after', 'Weekend']
            } else if (lowerText.includes('no') || lowerText.includes('later') || lowerText.includes('not now')) {
                response = `I understand – everyone has a busy schedule!\n\nHowever, delaying service could lead to more expensive repairs. Our data shows early intervention saves 40% on average.\n\nWould it help if I found a slot that fits your schedule? Or I can send a reminder for next week?`
                newSuggestions = ['Okay, let\'s schedule', 'Remind me next week', 'I need more time']
            } else if (lowerText.includes('cost') || lowerText.includes('price') || lowerText.includes('how much')) {
                response = `Great question about costs!\n\nBased on our diagnosis:\n• If addressed now: ₹8,000 - ₹15,000\n• If delayed: Could reach ₹25,000 - ₹40,000\n\nPlus, preventive maintenance takes just 2-4 hours, while breakdown repairs can take days.\n\nWould you like to save by scheduling now?`
                newSuggestions = ['That\'s reasonable, proceed', 'Still thinking', 'Tell me more']
            } else if (lowerText.includes('morning') || lowerText.includes('9')) {
                response = `Appointment Confirmed!\n\n📅 Tomorrow at 9:00 AM\n📍 AutoCare ${vehicle.city} Central\n🚗 ${vehicle.make} ${vehicle.model}\n\nPre-service checklist:\n• Remove valuables from vehicle\n• Bring registration documents\n• Ensure 1/4 tank fuel\n\nYou'll receive a reminder 2 hours before. See you tomorrow!`
                newSuggestions = ['Thanks!', 'Need to reschedule', 'Any other questions']
            } else if (lowerText.includes('afternoon') || lowerText.includes('2')) {
                response = `Appointment Confirmed!\n\n📅 Tomorrow at 2:00 PM\n📍 AutoCare ${vehicle.city} Central\n🚗 ${vehicle.make} ${vehicle.model}\n\nWe'll send you a reminder. See you tomorrow!`
                newSuggestions = ['Thanks!', 'Need to reschedule']
            } else if (lowerText.includes('tell') || lowerText.includes('more') || lowerText.includes('detail')) {
                response = `Let me explain what we detected:\n\n1. Engine System: ${vehicle.health_score < 60 ? 'High risk - needs attention' : 'Moderate - monitoring required'}\n2. Brakes: ${vehicle.health_score < 70 ? 'Wear detected' : 'Good condition'}\n\nOur AI predicts ${100 - vehicle.health_score}% probability of needing repair if not addressed.\n\nEarly maintenance is always more cost-effective. Want to proceed with scheduling?`
                newSuggestions = ['Yes, schedule', 'What\'s the cost?', 'I\'ll think about it']
            } else if (lowerText.includes('thank')) {
                response = `You're welcome! Is there anything else I can help you with regarding your ${vehicle.make} ${vehicle.model}?`
                newSuggestions = ['That\'s all, thanks!', 'One more question']
            } else {
                response = `I want to make sure I understand you correctly.\n\nAre you interested in:\n1. Scheduling a service appointment\n2. Learning more about the detected issues\n3. Getting a cost estimate\n\nJust let me know how I can help!`
                newSuggestions = ['Schedule appointment', 'Tell me more', 'Cost estimate']
            }

            setMessages(prev => [...prev, { type: 'bot', text: response }])
            setSuggestions(newSuggestions)
            setIsTyping(false)
        }, 1200)
    }

    if (!vehicle) {
        return (
            <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
                <MessageSquareIcon />
                <h2 style={{ marginBottom: '1rem', marginTop: '1rem' }}>AI Customer Engagement</h2>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
                    Select a vehicle from the Dashboard to start a conversation
                </p>
            </div>
        )
    }

    return (
        <div className="dashboard-grid">
            {/* Vehicle Info */}
            <div className="card">
                <div className="card-header">
                    <h2 className="card-title"><Car size={20} /> Vehicle Details</h2>
                    <span className={`badge ${vehicle.health_score >= 70 ? 'success' : vehicle.health_score >= 50 ? 'warning' : 'danger'}`}>
                        {vehicle.health_score}% Health
                    </span>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Car size={16} style={{ color: 'var(--text-muted)' }} />
                        <span><strong>Vehicle:</strong> {vehicle.make} {vehicle.model}</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <User size={16} style={{ color: 'var(--text-muted)' }} />
                        <span><strong>Owner:</strong> {vehicle.owner.name}</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <MapPin size={16} style={{ color: 'var(--text-muted)' }} />
                        <span><strong>Location:</strong> {vehicle.city}</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Gauge size={16} style={{ color: 'var(--text-muted)' }} />
                        <span><strong>Odometer:</strong> {vehicle.odometer.toLocaleString()} km</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <AlertCircle size={16} style={{ color: 'var(--text-muted)' }} />
                        <span><strong>Active Alerts:</strong></span>
                        <span className="badge danger">{vehicle.active_alerts}</span>
                    </div>
                </div>
                {messages.length === 0 && (
                    <button className="btn btn-primary" onClick={startConversation} style={{ marginTop: '1.5rem', width: '100%' }}>
                        <Mic size={16} /> Start Voice Conversation
                    </button>
                )}
            </div>

            {/* Chat */}
            <div className="card" style={{ padding: 0 }}>
                <div className="chat-container">
                    <div className="chat-messages">
                        <AnimatePresence>
                            {messages.map((msg, i) => (
                                <motion.div
                                    key={i}
                                    className={`message ${msg.type}`}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    style={{ whiteSpace: 'pre-wrap' }}
                                >
                                    {msg.text}
                                </motion.div>
                            ))}
                            {isTyping && (
                                <motion.div className="message bot" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                                    <span className="typing-indicator">
                                        <span></span><span></span><span></span>
                                    </span>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>

                    {messages.length > 0 && suggestions.length > 0 && (
                        <div className="suggested-responses">
                            {suggestions.map((s, i) => (
                                <button key={i} className="suggested-btn" onClick={() => sendMessage(s)}>{s}</button>
                            ))}
                        </div>
                    )}

                    <div className="chat-input-container">
                        <input
                            className="chat-input"
                            placeholder="Type your message..."
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            onKeyPress={e => e.key === 'Enter' && sendMessage(input)}
                        />
                        <button className="btn btn-primary" onClick={() => sendMessage(input)}>
                            <Send size={16} />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

function MessageSquareIcon() {
    return (
        <div style={{ display: 'flex', justifyContent: 'center' }}>
            <div style={{ width: 64, height: 64, borderRadius: 16, background: 'var(--accent-gradient)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
            </div>
        </div>
    )
}
