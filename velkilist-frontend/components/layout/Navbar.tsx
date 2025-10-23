// @ts-nocheck
import Link from 'next/link'

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between py-3">
      <Link href="/" className="text-xl font-semibold text-brand-400">VelkiList</Link>
      <div className="flex items-center gap-4 text-sm text-slate-300">
        <Link href="/sportsbook" className="hover:text-white">Sports</Link>
        <Link href="/casino" className="hover:text-white">Casino</Link>
        <Link href="/wallet" className="hover:text-white">Wallet</Link>
        <Link href="/support" className="hover:text-white">Support</Link>
        <Link href="/admin/dashboard" className="hover:text-white">Admin</Link>
        <Link href="/login" className="hover:text-white">Login</Link>
        <Link href="/register" className="hover:text-white">Register</Link>
      </div>
    </nav>
  )
}
