import './globals.css'
// @ts-nocheck
import './globals.css'
import CustomCssInjector from '@/components/common/CustomCssInjector'
import type { Metadata } from 'next'
import Link from 'next/link'
import Navbar from '@/components/layout/Navbar'
import { LiveDataProvider } from '@/context/LiveDataContext'
import WhatsAppButton from '@/components/common/WhatsAppButton'
import NotificationsClient from '@/components/common/NotificationsClient'

export const metadata: Metadata = {
  title: 'VelkiList',
  description: 'Betting platform UI for VelkiList',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>
        <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur">
          <div className="container">
            <Navbar />
          </div>
        </header>
        <LiveDataProvider>
          <CustomCssInjector />
          <NotificationsClient />
          <main className="container py-6">
            {children}
          </main>
          <WhatsAppButton />
        </LiveDataProvider>
      </body>
    </html>
  )
}
