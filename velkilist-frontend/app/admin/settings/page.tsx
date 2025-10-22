// @ts-nocheck
"use client"

import Link from 'next/link'

const cards = [
  { href: '/admin/settings/general', title: 'General Setting', desc: 'Configure fundamental information of the site.' },
  { href: '/admin/settings/system', title: 'System Configuration', desc: 'Control basic modules of the system.' },
  { href: '/admin/settings/api', title: 'API Setting', desc: 'Configure odds API providers and tokens.' },
  { href: '/admin/settings/logo', title: 'Logo and Favicon', desc: 'Upload your logo and favicon.' },
  { href: '/admin/settings/referral', title: 'Referral Setting', desc: 'Configure referral settings.' },
  { href: '/admin/settings/notification', title: 'Notification Setting', desc: 'Control in-app and email notifications.' },
  { href: '/admin/settings/payments', title: 'Payment Gateways', desc: 'Automatic or manual payment gateways.' },
  { href: '/admin/settings/withdrawals', title: 'Withdrawals Methods', desc: 'Setup withdrawal methods and rules.' },
  { href: '/admin/settings/kyc', title: 'KYC Setting', desc: 'Dynamic input fields for client KYC.' },
  { href: '/admin/settings/frontend', title: 'Manage Frontend', desc: 'Control frontend contents and SEO.' },
  { href: '/admin/settings/seo', title: 'SEO Configuration', desc: 'Meta title, description, keywords.' },
  { href: '/admin/settings/social-login', title: 'Social Login Setting', desc: 'Configure social login providers.' },
]

export default function SettingsHome() {
  return (
    <div>
      <h1 className="text-xl font-semibold mb-3">Site Settings</h1>
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {cards.map((c) => (
          <Link key={c.href} href={c.href} className="rounded-xl border border-slate-800 bg-slate-900 p-4 hover:border-slate-700">
            <div className="text-lg font-semibold">{c.title}</div>
            <div className="text-sm text-slate-400 mt-1">{c.desc}</div>
          </Link>
        ))}
      </div>
    </div>
  )
}
