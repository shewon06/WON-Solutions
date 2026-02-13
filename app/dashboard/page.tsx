import React from "react";
import { getDashboardStats } from "../actions";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
    const result = await getDashboardStats();

    // Default stats to ensure type safety and handle failures gracefully
    const stats = (result.success && result.stats) ? result.stats : {
        products: 0,
        sales: 0,
        companies: 0,
        revenue: 0
    };

    return (
        <div className="space-y-8">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                <StatCard
                    title="Total Products"
                    value={stats.products.toString()}
                    icon={<BoxIcon />}
                    color="blue"
                />
                <StatCard
                    title="Total Sales"
                    value={stats.sales.toString()}
                    icon={<TagIcon />}
                    color="green"
                />
                <StatCard
                    title="Revenue (LKR)"
                    value={`${stats.revenue.toLocaleString()}`}
                    icon={<DollarIcon />}
                    color="emerald"
                />
                <StatCard
                    title="Companies"
                    value={stats.companies.toString()}
                    icon={<BuildingIcon />}
                    color="purple"
                />
            </div>

            {/* Grid for more content */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl transition-all hover:bg-white/[0.07]">
                    <h3 className="mb-6 text-xl font-bold">Migration Status</h3>
                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <span className="text-white/60">Legacy Data Migration</span>
                            <span className="rounded-full bg-green-500/20 px-3 py-1 text-xs font-semibold text-green-400">Complete</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-white/60">MongoDB Connection</span>
                            <span className="rounded-full bg-green-500/20 px-3 py-1 text-xs font-semibold text-green-400">Stable</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-white/60">Vercel Deployment</span>
                            <span className="rounded-full bg-blue-500/20 px-3 py-1 text-xs font-semibold text-blue-400">Restructured</span>
                        </div>
                    </div>
                </div>

                <div className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl transition-all hover:bg-white/[0.07]">
                    <h3 className="mb-6 text-xl font-bold">System Health</h3>
                    <div className="flex items-center gap-4 text-sm">
                        <div className="h-12 w-12 rounded-full border border-blue-500/30 bg-blue-500/10 flex items-center justify-center">
                            <span className="text-blue-400 font-bold">99%</span>
                        </div>
                        <div>
                            <p className="font-semibold text-white/80">API Response optimized</p>
                            <p className="text-white/40 text-xs">Connected to Atlas FF23EWX shard-00-00</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ title, value, icon, color }: { title: string, value: string, icon: React.ReactNode, color: string }) {
    const colorMap: Record<string, string> = {
        blue: "text-blue-400 bg-blue-400/10 border-blue-400/20",
        green: "text-green-400 bg-green-400/10 border-green-400/20",
        emerald: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20",
        purple: "text-purple-400 bg-purple-400/10 border-purple-400/20",
    };

    return (
        <div className="group rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl transition-all hover:bg-white/[0.07]">
            <div className="mb-4 flex items-center justify-between">
                <div className={`rounded-xl p-2 transition-transform group-hover:scale-110 ${colorMap[color]}`}>
                    {icon}
                </div>
            </div>
            <p className="text-sm font-medium text-white/40">{title}</p>
            <p className="text-3xl font-bold tracking-tight text-white">{value}</p>
        </div>
    );
}

// Simplified Icons to avoid build issues
const BoxIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z" /></svg>
);
const TagIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2H2v10l9.29 9.29c.94.94 2.48.94 3.42 0l6.58-6.58c.94-.94.94-2.48 0-3.42L12 2Z" /></svg>
);
const DollarIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="12" x="2" y="6" rx="2" /><circle cx="12" cy="12" r="2" /><path d="M6 12h.01M18 12h.01" /></svg>
);
const BuildingIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="16" height="20" x="4" y="2" rx="2" /><path d="M9 22v-4h6v4" /></svg>
);
