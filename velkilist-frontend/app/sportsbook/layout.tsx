export default function SportsbookLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3 text-sm text-slate-300">
        <a className="hover:text-white" href="/sportsbook">Upcoming</a>
        <a className="hover:text-white" href="/sportsbook?status=live">Live</a>
      </div>
      {children}
    </div>
  )
}
