"use server";

import client from "@/lib/mongodb";
import { ObjectId } from "mongodb";

export async function testDatabaseConnection() {
  let isConnected = false;
  try {
    const mongoClient = await client.connect();
    await mongoClient.db("admin").command({ ping: 1 });
    return true;
  } catch (e) {
    console.error(e);
    return false;
  }
}

export async function getDashboardStats() {
  try {
    const mongoClient = await client.connect();
    const db = mongoClient.db();

    const [productCount, saleCount, companyCount, totalRevenue] = await Promise.all([
      db.collection("products").countDocuments(),
      db.collection("sales").countDocuments(),
      db.collection("company_master").countDocuments(),
      db.collection("sales").aggregate([
        { $group: { _id: null, total: { $sum: "$total_amount" } } }
      ]).toArray()
    ]);

    const revenue = totalRevenue.length > 0 ? totalRevenue[0].total : 0;

    return {
      success: true,
      stats: {
        products: productCount,
        sales: saleCount,
        companies: companyCount,
        revenue: Math.round(revenue * 100) / 100
      }
    };
  } catch (e) {
    console.error("Error fetching dashboard stats:", e);
    return {
      success: false,
      error: "Failed to fetch dashboard statistics"
    };
  }
}

export async function getPOSData() {
  try {
    const mongoClient = await client.connect();
    const db = mongoClient.db();

    const [products, customers] = await Promise.all([
      db.collection("products").find({ is_active: true }).toArray(),
      db.collection("customers").find().toArray()
    ]);

    return {
      success: true,
      products: products.map(p => ({
        id: p._id.toString(),
        name: p.name,
        selling_price: p.selling_price,
        cost_price: p.cost_price,
        stock_qty: p.stock_qty || 0,
        category: p.category?.toString() || ""
      })),
      customers: customers.map(c => ({
        id: c._id.toString(),
        name: c.name,
        phone: c.phone
      }))
    };
  } catch (e) {
    console.error("Error fetching POS data:", e);
    return { success: false, error: "Failed to fetch POS data" };
  }
}

export async function processSale(saleData: any) {
  try {
    const mongoClient = await client.connect();
    const db = mongoClient.db();

    // 1. Calculate VAT and Totals (18% if applicable)
    // For now assuming VAT logic from legacy
    const totalAmount = saleData.items.reduce((acc: number, item: any) => acc + (item.price * item.qty), 0);
    const vatAmount = totalAmount - (totalAmount / 1.18);
    const subtotal = totalAmount - vatAmount;

    // 2. Create Sale Record
    const saleResult = await db.collection("sales").insertOne({
      total_amount: totalAmount,
      subtotal: subtotal,
      vat_amount: vatAmount,
      is_vat_inclusive: true,
      payment_type: saleData.paymentType,
      customer_id: saleData.customerId,
      created_at: new Date(),
      sold_by: "Admin" // Placeholder until auth is integrated
    });

    const saleId = saleResult.insertedId;

    // 3. Create Sale Items and Update Stock
    for (const item of saleData.items) {
      const productId = new ObjectId(item.id);

      await db.collection("sale_items").insertOne({
        sale_id: saleId,
        product_id: productId,
        quantity: item.qty,
        price: item.price,
        cost_price: item.cost_price || 0
      });

      await db.collection("products").updateOne(
        { _id: productId },
        { $inc: { stock_qty: -item.qty } }
      );
    }

    return { success: true, saleId: saleId.toString() };
  } catch (e) {
    console.error("Error processing sale:", e);
    return { success: false, error: "Failed to complete transaction" };
  }
}
