'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const router = useRouter()
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [emails, setEmails] = useState([])
  const [userEmail, setUserEmail] = useState('')

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('mailpilot_token')
    const email = localStorage.getItem('user_email')
    
    if (!token) {
      router.push('/landing')
      return
    }
    
    setUserEmail(email || '')
    loadEmails()
  }, [])

  const loadEmails = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/emails/list`, {
        query: 'in:inbox',
        max_results: 10
      })
      setEmails(JSON.parse(response.data.emails))
    } catch (error) {
      console.error('Error loading emails:', error)
    }
  }

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/agent/query`, {
        message: input,
        user_id: userEmail || localStorage.getItem('user_email') || 'demo-user'
      })

      const aiMessage = { role: 'assistant', content: response.data.response }
      setMessages(prev => [...prev, aiMessage])
      
      // Reload emails if action was performed
      if (input.toLowerCase().includes('send') || 
          input.toLowerCase().includes('archive') ||
          input.toLowerCase().includes('delete')) {
        loadEmails()
      }
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, an error occurred. Please try again.' 
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Top Navigation */}
      <nav className="border-b border-gray-200 bg-white sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white text-lg">✉</span>
              </div>
              <span className="text-xl font-semibold text-gray-900">MailPilot</span>
            </div>
            
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">{userEmail}</span>
              <button
                onClick={() => {
                  localStorage.removeItem('mailpilot_token')
                  localStorage.removeItem('user_email')
                  router.push('/landing')
                }}
                className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-12 gap-6 h-[calc(100vh-140px)]">
          
          {/* Sidebar - Email List */}
          <div className="col-span-4 flex flex-col h-full">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Inbox</h2>
              <button 
                onClick={loadEmails}
                className="text-sm text-blue-600 hover:text-blue-700 transition-colors"
              >
                Refresh
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto space-y-2 pr-2">
              {emails.map((email: any) => (
                <div 
                  key={email.id} 
                  className="p-4 bg-gray-50 hover:bg-gray-100 rounded-lg cursor-pointer transition-colors border border-transparent hover:border-gray-200"
                >
                  <div className="flex items-start justify-between mb-1">
                    <p className="text-sm font-medium text-gray-900 truncate flex-1">
                      {email.from.split('<')[0].trim()}
                    </p>
                    <span className="text-xs text-gray-500 ml-2 whitespace-nowrap">
                      {new Date(email.date).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-gray-700 truncate mb-1">
                    {email.subject}
                  </p>
                  <p className="text-xs text-gray-500 line-clamp-2">
                    {email.snippet}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Main Chat Area */}
          <div className="col-span-8 flex flex-col h-full">
            <div className="mb-4">
              <h2 className="text-lg font-semibold text-gray-900">AI Assistant</h2>
              <p className="text-sm text-gray-500">Ask me anything about your emails</p>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto mb-4 space-y-4">
              {messages.length === 0 && (
                <div className="h-full flex flex-col items-center justify-center text-center px-8">
                  <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4">
                    <span className="text-3xl">🤖</span>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Welcome to MailPilot
                  </h3>
                  <p className="text-sm text-gray-600 mb-6 max-w-md">
                    I'm your AI email assistant. I can help you manage your inbox, send emails, and stay organized.
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center">
                    {['Show unread emails', 'Summarize my inbox', 'Check urgent emails'].map(suggestion => (
                      <button
                        key={suggestion}
                        onClick={() => {
                          setInput(suggestion)
                          setTimeout(() => sendMessage(), 100)
                        }}
                        className="px-4 py-2 text-sm bg-white border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-2xl ${
                    msg.role === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 text-gray-900'
                  } rounded-2xl px-4 py-3`}>
                    <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                  </div>
                </div>
              ))}
              
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-2xl px-4 py-3">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 pt-4">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
                  placeholder="Type your message..."
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  disabled={loading}
                />
                <button
                  onClick={sendMessage}
                  disabled={loading || !input.trim()}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium text-sm"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
