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
      const response = await axios.post(`${API_URL}/api/agent/query`, {
        message: 'show my inbox emails',
        user_id: userEmail || localStorage.getItem('user_email') || 'demo-user'
      })
      
      // Try to parse the response as email list
      try {
        const emailData = JSON.parse(response.data.response)
        if (Array.isArray(emailData)) {
          setEmails(emailData)
        }
      } catch {
        console.log('Could not parse emails from response')
      }
    } catch (error) {
      console.error('Error loading emails:', error)
    }
  }

  const sendMessage = async (customInput?: string) => {
    const messageToSend = customInput || input
    if (!messageToSend.trim()) return

    const userMessage = { role: 'user', content: messageToSend }
    setMessages(prev => [...prev, userMessage])
    if (!customInput) setInput('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/agent/query`, {
        message: messageToSend,
        user_id: userEmail || localStorage.getItem('user_email') || 'demo-user'
      })

      const aiMessage = { role: 'assistant', content: response.data.response }
      setMessages(prev => [...prev, aiMessage])
      
      // Reload emails if action was performed
      if (messageToSend.toLowerCase().includes('send') || 
          messageToSend.toLowerCase().includes('archive') ||
          messageToSend.toLowerCase().includes('delete') ||
          messageToSend.toLowerCase().includes('show') ||
          messageToSend.toLowerCase().includes('list')) {
        setTimeout(() => loadEmails(), 1000) // Reload after 1 second
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

  const formatResponse = (content: string) => {
    // Try to parse as JSON for email lists
    try {
      const parsed = JSON.parse(content)
      if (Array.isArray(parsed) && parsed.length > 0 && parsed[0].id) {
        // It's an email list
        return (
          <div className="space-y-3">
            <p className="text-sm font-medium text-gray-700 mb-3">
              Found {parsed.length} email{parsed.length !== 1 ? 's' : ''}:
            </p>
            {parsed.map((email: any) => (
              <div 
                key={email.id} 
                className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-gray-900 truncate">
                      {email.from.split('<')[0].trim()}
                    </p>
                    <p className="text-xs text-gray-500 truncate">
                      {email.from.match(/<(.+)>/)?.[1] || email.from}
                    </p>
                  </div>
                  <span className="text-xs text-gray-400 ml-3 whitespace-nowrap">
                    {new Date(email.date).toLocaleDateString('en-US', { 
                      month: 'short', 
                      day: 'numeric',
                      year: new Date(email.date).getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
                    })}
                  </span>
                </div>
                <p className="text-sm font-medium text-gray-800 mb-2 line-clamp-1">
                  {email.subject}
                </p>
                <p className="text-xs text-gray-600 line-clamp-2">
                  {email.snippet.replace(/&#39;/g, "'").replace(/&quot;/g, '"')}
                </p>
                <div className="mt-3 flex gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      sendMessage(`Read email ${email.id}`)
                    }}
                    className="text-xs px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors font-medium"
                  >
                    📖 Read
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      sendMessage(`Archive email ${email.id}`)
                    }}
                    className="text-xs px-3 py-1.5 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors font-medium"
                  >
                    📦 Archive
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      sendMessage(`Star email ${email.id}`)
                    }}
                    className="text-xs px-3 py-1.5 bg-yellow-500 text-white rounded-md hover:bg-yellow-600 transition-colors font-medium"
                  >
                    ⭐ Star
                  </button>
                </div>
              </div>
            ))}
          </div>
        )
      }
    } catch (e) {
      // Not JSON, return as regular text
    }
    
    // Regular text response
    return <p className="text-sm whitespace-pre-wrap leading-relaxed">{content}</p>
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
              {emails.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <p className="text-sm">No emails to display</p>
                  <button
                    onClick={loadEmails}
                    className="mt-2 text-sm text-blue-600 hover:text-blue-700"
                  >
                    Load emails
                  </button>
                </div>
              ) : (
                emails.map((email: any) => (
                  <div 
                    key={email.id} 
                    onClick={() => setInput(`Read email ${email.id}`)}
                    className="p-4 bg-white border border-gray-200 hover:border-blue-300 hover:shadow-md rounded-lg cursor-pointer transition-all group"
                  >
                    <div className="flex items-start justify-between mb-1">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-gray-900 truncate group-hover:text-blue-600 transition-colors">
                          {email.from.split('<')[0].trim()}
                        </p>
                      </div>
                      <span className="text-xs text-gray-500 ml-2 whitespace-nowrap">
                        {new Date(email.date).toLocaleDateString('en-US', { 
                          month: 'short', 
                          day: 'numeric'
                        })}
                      </span>
                    </div>
                    <p className="text-sm font-medium text-gray-800 truncate mb-1">
                      {email.subject}
                    </p>
                    <p className="text-xs text-gray-500 line-clamp-2">
                      {email.snippet.replace(/&#39;/g, "'").replace(/&quot;/g, '"')}
                    </p>
                  </div>
                ))
              )}
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
                        onClick={() => sendMessage(suggestion)}
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
                    {msg.role === 'user' ? (
                      <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                    ) : (
                      formatResponse(msg.content)
                    )}
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
