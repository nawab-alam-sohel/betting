// @ts-nocheck
import React from 'react'

export default function AuthLayout({ title, children }: { title?: string; children: React.ReactNode }) {
  return (
    <div className="relative min-h-[calc(100vh-4rem)] -mx-4 md:-mx-8 lg:-mx-16">
      {/* Background demo image */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src="/images/auth-demo.svg"
        alt="Auth background"
        className="pointer-events-none select-none absolute inset-0 -z-10 h-full w-full object-cover"
      />
      <div className="absolute inset-0 -z-10 bg-slate-900/50" />

      <div className="container mx-auto px-4 md:px-8 lg:px-16 py-10 flex items-start md:items-center justify-center">
        <div className="w-full max-w-lg rounded-xl bg-white/95 backdrop-blur shadow-2xl">
          <div className="p-6 md:p-8">
            {title && (
              <div>
                <h1 className="text-2xl font-semibold text-slate-900">{title}</h1>
                <div className="h-0.5 w-12 bg-indigo-500 mt-3 mb-4" />
              </div>
            )}
            {children}
            <p className="mt-6 text-[11px] text-slate-500">Background is a demo image. Replace <code className="px-1">/public/images/auth-demo.svg</code> with your real artwork later.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
 
