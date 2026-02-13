import Head from "next/head";
import Link from "next/link";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <div className={`min-h-screen bg-[#020202] text-white selection:bg-blue-500/30 ${inter.className}`}>
      <Head>
        <title>WON Solutions | Business Management System</title>
        <meta name="description" content="State-of-the-art business management and data visualization" />
      </Head>

      {/* Navigation */}
      <nav className="fixed top-0 z-50 w-full border-b border-white/5 bg-black/50 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 rounded bg-blue-600"></div>
            <span className="text-lg font-bold tracking-tight uppercase">WON Solutions</span>
          </div>
          <div className="flex items-center gap-6 text-sm font-medium text-white/60">
            <Link href="/dashboard" className="transition-colors hover:text-white">Dashboard</Link>
            <Link href="#" className="transition-colors hover:text-white">Enterprise</Link>
            <Link href="/dashboard" className="rounded-full bg-white px-5 py-2 text-black transition-transform hover:scale-105 active:scale-95">
              Launch System
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative flex flex-col items-center justify-center pt-32 pb-20 px-6 overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute top-0 -z-10 h-[600px] w-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-transparent to-transparent opacity-50 blur-3xl"></div>
        <div className="absolute bottom-0 left-1/2 -z-10 h-[400px] w-[800px] -translate-x-1/2 bg-blue-600/10 opacity-30 blur-[120px]"></div>

        <div className="text-center max-w-4xl space-y-8">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/5 px-4 py-1 text-sm font-medium text-blue-400">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
            </span>
            System Restructured & Connected
          </div>

          <h1 className="text-6xl md:text-8xl font-black tracking-tight leading-[1.1]">
            Management <br />
            <span className="bg-gradient-to-b from-white to-white/40 bg-clip-text text-transparent">Reimagined.</span>
          </h1>

          <p className="mx-auto max-w-2xl text-lg md:text-xl text-white/50 leading-relaxed">
            A high-performance business architecture built on Next.js 15+ and MongoDB Atlas.
            Experience zero-latency data visualization and seamless cloud deployment.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link
              href="/dashboard"
              className="w-full sm:w-auto flex items-center justify-center gap-2 rounded-2xl bg-blue-600 px-8 py-4 text-base font-bold shadow-[0_0_20px_rgba(37,99,235,0.4)] transition-all hover:bg-blue-500 hover:shadow-[0_0_30px_rgba(37,99,235,0.6)] active:scale-95"
            >
              Access Dashboard
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14" /><path d="m12 5 7 7-7 7" /></svg>
            </Link>
            <Link
              href="https://wongroup.tech"
              className="w-full sm:w-auto rounded-2xl border border-white/10 bg-white/5 px-8 py-4 text-base font-bold backdrop-blur-xl transition-all hover:bg-white/10 active:scale-95"
            >
              Live Site
            </Link>
          </div>
        </div>

        {/* Floating Mockup (Pure CSS) */}
        <div className="mt-20 w-full max-w-6xl relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl blur opacity-20 group-hover:opacity-30 transition duration-1000"></div>
          <div className="relative rounded-3xl border border-white/10 bg-black/80 p-4 backdrop-blur-2xl">
            <div className="rounded-2xl border border-white/5 bg-[#0a0a0a] aspect-[16/9] overflow-hidden flex items-center justify-center text-white/20">
              {/* Decorative grid */}
              <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
              <p className="text-xl font-mono uppercase tracking-[0.5em]">System Core Active</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/5 bg-black py-12 px-6">
        <div className="mx-auto max-w-7xl flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="text-white/40 text-sm">
            © 2026 WON SOLUTIONS (PVT) LTD. All rights reserved.
          </div>
          <div className="flex gap-8 text-sm font-medium text-white/30">
            <Link href="#" className="hover:text-white transition-colors">Privacy</Link>
            <Link href="#" className="hover:text-white transition-colors">Terms</Link>
            <Link href="#" className="hover:text-white transition-colors">Security</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
