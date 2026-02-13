import Link from "next/link";
import React from "react";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-screen bg-[#0a0a0a] text-white">
            {/* Sidebar */}
            <aside className="w-64 border-r border-white/10 bg-black/50 p-6 backdrop-blur-xl">
                <div className="mb-10 flex items-center gap-2">
                    <div className="h-8 w-8 rounded-lg bg-blue-600 shadow-[0_0_15px_rgba(37,99,235,0.5)]"></div>
                    <span className="text-xl font-bold tracking-tight">WON SOLUTIONS</span>
                </div>

                <nav className="space-y-2">
                    <Link href="/dashboard" className="flex items-center gap-3 rounded-lg px-4 py-2 transition-colors hover:bg-white/5 text-white/70 hover:text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="7" height="9" x="3" y="3" rx="1" /><rect width="7" height="5" x="14" y="3" rx="1" /><rect width="7" height="5" x="3" y="16" rx="1" /><rect width="7" height="9" x="14" y="12" rx="1" /></svg>
                        Dashboard
                    </Link>
                    <Link href="/dashboard/pos" className="flex items-center gap-3 rounded-lg bg-blue-600/10 px-4 py-2 text-blue-400 border border-blue-600/20">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><path d="M12 8v8" /><path d="M8 12h8" /></svg>
                        POS System
                    </Link>
                    <div className="pt-4 text-xs font-semibold text-white/40 uppercase tracking-wider px-4">Management</div>
                    <Link href="/dashboard/products" className="flex items-center gap-3 rounded-lg px-4 py-2 transition-colors hover:bg-white/5 text-white/70 hover:text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m7.5 4.27 9 5.15" /><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z" /><path d="m3.3 7 8.7 5 8.7-5" /><path d="M12 22V12" /></svg>
                        Products
                    </Link>
                    <Link href="/dashboard/sales" className="flex items-center gap-3 rounded-lg px-4 py-2 transition-colors hover:bg-white/5 text-white/70 hover:text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z" /><path d="M3 6h18" /><path d="M16 10a4 4 0 0 1-8 0" /></svg>
                        Sales
                    </Link>
                    <Link href="/dashboard/customers" className="flex items-center gap-3 rounded-lg px-4 py-2 transition-colors hover:bg-white/5 text-white/70 hover:text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg>
                        Customers
                    </Link>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 p-10 overflow-auto bg-gradient-to-br from-[#0a0a0a] to-[#121212]">
                <header className="mb-10 flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold">System Overview</h1>
                        <p className="text-white/40">Welcome back to WON Solutions dashboard.</p>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="h-10 w-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" /></svg>
                        </div>
                        <div className="h-10 px-4 rounded-lg bg-white/5 border border-white/10 flex items-center gap-2">
                            <span className="text-sm font-medium">Administrator</span>
                        </div>
                    </div>
                </header>

                {children}
            </main>
        </div>
    );
}
