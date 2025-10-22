// @ts-nocheck
import React from 'react'
import Link from 'next/link'

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-12 gap-4 min-h-[70vh]">
      <aside className="col-span-12 md:col-span-3 lg:col-span-2 rounded-xl border border-slate-800 bg-slate-900 p-4 sticky top-20 h-fit">
        <div className="text-sm font-semibold text-slate-200 mb-2">Admin</div>
        <nav className="space-y-2 text-sm">
          <div>
            <div className="text-slate-400 uppercase text-xs mb-1">Dashboard</div>
            <Link href="/admin/dashboard" className="block px-2 py-1 rounded hover:bg-slate-800">Overview</Link>
          </div>
          <div>
            <div className="text-slate-400 uppercase text-xs mt-3 mb-1">Manage Bettors</div>
            <Link href="/admin/bettors/active" className="block px-2 py-1 rounded hover:bg-slate-800">Active Bettors</Link>
            <Link href="/admin/bettors/banned" className="block px-2 py-1 rounded hover:bg-slate-800">Banned Bettors</Link>
            <Link href="/admin/bettors/email-unverified" className="block px-2 py-1 rounded hover:bg-slate-800">Email Unverified</Link>
            <Link href="/admin/bettors/mobile-unverified" className="block px-2 py-1 rounded hover:bg-slate-800">Mobile Unverified</Link>
            <Link href="/admin/bettors/kyc-unverified" className="block px-2 py-1 rounded hover:bg-slate-800">KYC Unverified</Link>
            <Link href="/admin/bettors/kyc-pending" className="block px-2 py-1 rounded hover:bg-slate-800">KYC Pending</Link>
            <Link href="/admin/bettors/with-balance" className="block px-2 py-1 rounded hover:bg-slate-800">With Balance</Link>
            <Link href="/admin/bettors/all" className="block px-2 py-1 rounded hover:bg-slate-800">All Bettors</Link>
            <Link href="/admin/bettors/notify" className="block px-2 py-1 rounded hover:bg-slate-800">Send Notification</Link>
          </div>
          <div>
            <div className="text-slate-400 uppercase text-xs mt-3 mb-1">Betting</div>
            <Link href="/admin/sports/categories" className="block px-2 py-1 rounded hover:bg-slate-800">Categories</Link>
            <Link href="/admin/sports/teams" className="block px-2 py-1 rounded hover:bg-slate-800">Teams</Link>
            <Link href="/admin/sports/leagues" className="block px-2 py-1 rounded hover:bg-slate-800">Leagues</Link>
          </div>
          <div>
            <div className="text-slate-400 uppercase text-xs mt-3 mb-1">Finance</div>
            <Link href="/admin/finance" className="block px-2 py-1 rounded hover:bg-slate-800">Overview</Link>
            <Link href="/admin/finance/deposits" className="block px-2 py-1 rounded hover:bg-slate-800">Deposits</Link>
            <Link href="/admin/finance/withdrawals" className="block px-2 py-1 rounded hover:bg-slate-800">Withdrawals</Link>
          </div>
          <div>
            <div className="text-slate-400 uppercase text-xs mt-3 mb-1">Settings</div>
            <Link href="/admin/settings" className="block px-2 py-1 rounded hover:bg-slate-800">Site Settings</Link>
            <Link href="/admin/settings/api" className="block px-2 py-1 rounded hover:bg-slate-800">API Settings</Link>
          </div>
        </nav>
      </aside>
      <main className="col-span-12 md:col-span-9 lg:col-span-10 space-y-4">
        {children}
      </main>
    </div>
  )
}
