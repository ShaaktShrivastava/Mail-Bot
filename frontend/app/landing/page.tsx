'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function LandingPage() {
  const router = useRouter()
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('mailpilot_token')
    if (token) {
      setIsLoggedIn(true)
      router.push('/')
    }
  }, [router])

  const handleConnectGmail = () => {
    router.push('/auth')
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="border-b border-gray-100 sticky top-0 bg-white/95 backdrop-blur-sm z-50">
        <div className="max-w-6xl mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white text-xl">✉</span>
              </div>
              <span className="text-xl font-semibold text-gray-900">MailPilot</span>
            </div>
            <button
              onClick={handleConnectGmail}
              className="px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Sign in
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-6 pt-20 pb-24 text-center">
        <div className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-50 rounded-full mb-8">
          <span className="text-sm font-medium text-blue-700">🎉 AI-Powered Email Management</span>
        </div>
        
        <h1 className="text-6xl font-bold text-gray-900 mb-6 leading-tight">
          Email made simple<br />with AI
        </h1>
        
        <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed">
          Let AI handle your inbox. Send emails, get summaries, and stay organized—all through natural conversation.
        </p>
        
        <button
          onClick={handleConnectGmail}
          className="inline-flex items-center px-8 py-4 bg-blue-600 text-white text-lg font-medium rounded-lg hover:bg-blue-700 transition-all shadow-sm hover:shadow-md"
        >
          <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Continue with Gmail
        </button>
        
        <p className="mt-4 text-sm text-gray-500">Free forever • No credit card required</p>
      </section>

      {/* Features Grid */}
      <section className="max-w-6xl mx-auto px-6 py-20">
        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: '💬',
              title: 'Natural Conversation',
              description: 'Just type what you want in plain English. No complex commands.'
            },
            {
              icon: '⚡',
              title: 'Instant Actions',
              description: 'Send emails, archive messages, and organize your inbox in seconds.'
            },
            {
              icon: '🧠',
              title: 'Smart Summaries',
              description: 'Get AI-powered summaries of your inbox and individual threads.'
            },
            {
              icon: '🎯',
              title: 'Priority Detection',
              description: 'Automatically identifies urgent emails that need attention.'
            },
            {
              icon: '🔐',
              title: 'Secure & Private',
              description: 'Your data stays yours. Built on Google\'s secure OAuth.'
            },
            {
              icon: '📊',
              title: 'Daily Insights',
              description: 'Start each day with an intelligent digest of what matters.'
            }
          ].map((feature, idx) => (
            <div key={idx} className="p-6">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
              <p className="text-gray-600 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it Works */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">How it works</h2>
            <p className="text-gray-600">Get started in under a minute</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-12">
            {[
              { num: '1', title: 'Connect Gmail', desc: 'Sign in with your Google account securely' },
              { num: '2', title: 'Start Chatting', desc: 'Ask anything about your emails naturally' },
              { num: '3', title: 'Stay Organized', desc: 'Let AI handle the busy work' }
            ].map((step, idx) => (
              <div key={idx} className="text-center">
                <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-600 text-white text-xl font-bold rounded-full mb-4">
                  {step.num}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{step.title}</h3>
                <p className="text-gray-600">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-6xl mx-auto px-6 py-24 text-center">
        <h2 className="text-4xl font-bold text-gray-900 mb-6">
          Ready to transform your inbox?
        </h2>
        <p className="text-xl text-gray-600 mb-10">
          Join thousands using AI to manage email effortlessly
        </p>
        <button
          onClick={handleConnectGmail}
          className="inline-flex items-center px-8 py-4 bg-blue-600 text-white text-lg font-medium rounded-lg hover:bg-blue-700 transition-all shadow-sm hover:shadow-md"
        >
          Get Started Free
          <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 py-8">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <p>© 2026 MailPilot. All rights reserved.</p>
            <div className="flex space-x-6">
              <a href="#" className="hover:text-gray-900 transition-colors">Privacy</a>
              <a href="#" className="hover:text-gray-900 transition-colors">Terms</a>
              <a href="#" className="hover:text-gray-900 transition-colors">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
