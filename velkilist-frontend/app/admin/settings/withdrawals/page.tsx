// @ts-nocheck
export default function WithdrawalsSettingsPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Withdrawals Methods</h1>
      <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
        <div className="text-sm text-slate-400">Configuration placeholder</div>
        <p className="text-slate-300 text-sm mt-2">For now, manage withdrawal methods and flow from Django Admin (Payments/WithdrawalRequest) or extend the API to expose provider/method configs. I can add a simple model and UI if you want to manage them here.</p>
      </div>
    </div>
  )
}
