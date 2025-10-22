import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Basic placeholder for role-based guard; currently pass-through
export function middleware(req: NextRequest) {
  return NextResponse.next()
}

export const config = {
  matcher: [
    // protect future admin/agent/wallet routes
    '/admin/:path*',
    '/agents/:path*',
    '/wallet',
  ],
}
