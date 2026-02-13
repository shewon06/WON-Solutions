"use client";

import React, { useState, useEffect } from "react";
import { getPOSData, processSale } from "../actions";

export default function POSPage() {
    const [products, setProducts] = useState<any[]>([]);
    const [customers, setCustomers] = useState<any[]>([]);
    const [cart, setCart] = useState<any[]>([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [customerId, setCustomerId] = useState("");
    const [paymentType, setPaymentType] = useState("CASH");
    const [loading, setLoading] = useState(true);
    const [processing, setProcessing] = useState(false);

    useEffect(() => {
        const loadData = async () => {
            const result = await getPOSData();
            if (result.success) {
                setProducts(result.products || []);
                setCustomers(result.customers || []);
            }
            setLoading(false);
        };
        loadData();
    }, []);

    const addToCart = (product: any) => {
        const existing = cart.find(item => item.id === product.id);
        if (existing) {
            setCart(cart.map(item =>
                item.id === product.id ? { ...item, qty: item.qty + 1 } : item
            ));
        } else {
            setCart([...cart, { ...product, qty: 1, price: product.selling_price }]);
        }
    };

    const removeFromCart = (id: string) => {
        setCart(cart.filter(item => item.id !== id));
    };

    const updateQty = (id: string, delta: number) => {
        setCart(cart.map(item => {
            if (item.id === id) {
                const newQty = Math.max(1, item.qty + delta);
                return { ...item, qty: newQty };
            }
            return item;
        }));
    };

    const subtotal = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);

    const handleCheckout = async () => {
        if (cart.length === 0) return;
        setProcessing(true);
        const result = await processSale({
            items: cart,
            customerId: customerId || null,
            paymentType
        });

        setProcessing(false);
        if (result.success) {
            alert("Sale completed successfully!");
            setCart([]);
            setCustomerId("");
            // Refresh products to get updated stock
            const posData = await getPOSData();
            if (posData.success) setProducts(posData.products || []);
        } else {
            alert("Error: " + result.error);
        }
    };

    const filteredProducts = products.filter(p =>
        p.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (loading) {
        return <div className="flex h-96 items-center justify-center text-white/40">Loading POS Environment...</div>;
    }

    return (
        <div className="flex gap-8 h-[75vh]">
            {/* Product Selection */}
            <div className="flex-1 flex flex-col min-w-0">
                <div className="mb-6">
                    <div className="relative">
                        <input
                            type="text"
                            placeholder="Search products by name or SKU..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full bg-white/5 border border-white/10 rounded-xl px-12 py-3 text-white outline-none focus:border-blue-500/50 transition-all backdrop-blur-xl"
                        />
                        <svg className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" /></svg>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4 pr-2 custom-scrollbar">
                    {filteredProducts.map((product) => (
                        <button
                            key={product.id}
                            onClick={() => addToCart(product)}
                            className="text-left group rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur-xl transition-all hover:bg-white/[0.08] hover:border-blue-500/30 hover:scale-[1.02]"
                        >
                            <div className="aspect-square rounded-xl bg-white/5 mb-3 flex items-center justify-center text-white/10 group-hover:text-blue-500/20 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m7.5 4.27 9 5.15" /><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z" /><path d="m3.3 7 8.7 5 8.7-5" /><path d="M12 22V12" /></svg>
                            </div>
                            <h3 className="font-bold text-sm text-white/90 truncate">{product.name}</h3>
                            <div className="mt-2 flex items-center justify-between">
                                <span className="text-blue-400 font-bold">LKR {product.selling_price.toLocaleString()}</span>
                                <span className="text-[10px] text-white/30">Stock: {product.stock_qty}</span>
                            </div>
                        </button>
                    ))}
                    {filteredProducts.length === 0 && (
                        <div className="col-span-full py-20 text-center text-white/20 italic">No products matched your search.</div>
                    )}
                </div>
            </div>

            {/* Cart Summary */}
            <div className="w-96 flex flex-col rounded-2xl border border-white/10 bg-black/40 backdrop-blur-2xl shadow-2xl overflow-hidden translate-z-0">
                <div className="p-6 border-b border-white/10 bg-blue-600/10">
                    <div className="flex items-center justify-between">
                        <h2 className="text-xl font-bold flex items-center gap-2">
                            Current Bill
                        </h2>
                        <span className="text-xs bg-white/10 px-2 py-1 rounded text-white/60">{cart.length} Items</span>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
                    {cart.map((item) => (
                        <div key={item.id} className="group flex items-start justify-between gap-4">
                            <div className="flex-1">
                                <h4 className="text-sm font-semibold text-white/90">{item.name}</h4>
                                <div className="flex items-center gap-3 mt-2">
                                    <div className="flex items-center bg-white/5 rounded-lg border border-white/10">
                                        <button onClick={() => updateQty(item.id, -1)} className="p-1 hover:text-blue-400">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14" /></svg>
                                        </button>
                                        <span className="text-xs w-6 text-center">{item.qty}</span>
                                        <button onClick={() => updateQty(item.id, 1)} className="p-1 hover:text-blue-400">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14" /><path d="M12 5v14" /></svg>
                                        </button>
                                    </div>
                                    <span className="text-xs text-white/40">@ {item.price.toLocaleString()}</span>
                                </div>
                            </div>
                            <div className="text-right">
                                <p className="text-sm font-bold text-white">{(item.price * item.qty).toLocaleString()}</p>
                                <button onClick={() => removeFromCart(item.id)} className="text-[10px] text-red-500/70 hover:text-red-500 mt-1 opacity-0 group-hover:opacity-100 transition-opacity">Remove</button>
                            </div>
                        </div>
                    ))}
                    {cart.length === 0 && (
                        <div className="h-full flex flex-col items-center justify-center text-center py-20 opacity-20">
                            <svg className="mb-4" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"><circle cx="8" cy="21" r="1" /><circle cx="19" cy="21" r="1" /><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12" /></svg>
                            <p className="text-sm italic">Cart is empty</p>
                        </div>
                    )}
                </div>

                <div className="p-6 border-t border-white/10 bg-white/5 space-y-4">
                    <div className="space-y-3">
                        <div className="flex items-center justify-between text-sm">
                            <span className="text-white/40">Customer</span>
                            <select
                                value={customerId}
                                onChange={(e) => setCustomerId(e.target.value)}
                                className="bg-transparent text-white outline-none text-right font-medium max-w-[150px] cursor-pointer"
                            >
                                <option value="" className="bg-neutral-900">Walk-in Customer</option>
                                {customers.map(c => (
                                    <option key={c.id} value={c.id} className="bg-neutral-900">{c.name}</option>
                                ))}
                            </select>
                        </div>
                        <div className="flex items-center justify-between text-sm">
                            <span className="text-white/40">Payment Method</span>
                            <select
                                value={paymentType}
                                onChange={(e) => setPaymentType(e.target.value)}
                                className="bg-transparent text-white outline-none text-right font-medium cursor-pointer"
                            >
                                <option value="CASH" className="bg-neutral-900">Cash</option>
                                <option value="CARD" className="bg-neutral-900">Card</option>
                                <option value="CREDIT" className="bg-neutral-900">Credit</option>
                            </select>
                        </div>
                    </div>

                    <div className="pt-4 border-t border-white/10">
                        <div className="flex justify-between items-end">
                            <span className="text-sm font-medium text-white/40">Total Amount</span>
                            <div className="text-right">
                                <span className="text-xs text-blue-400 block mb-1">LKR</span>
                                <span className="text-4xl font-black tracking-tighter text-white">
                                    {subtotal.toLocaleString()}
                                </span>
                            </div>
                        </div>
                    </div>

                    <button
                        onClick={handleCheckout}
                        disabled={cart.length === 0 || processing}
                        className="w-full mt-2 bg-blue-600 py-4 rounded-2xl font-bold hover:bg-blue-500 active:scale-[0.98] transition-all disabled:opacity-20 disabled:scale-100 disabled:bg-white/10 shadow-[0_0_20px_rgba(37,99,235,0.3)]"
                    >
                        {processing ? "Processing..." : "Complete Checkout"}
                    </button>
                </div>
            </div>
        </div>
    );
}
