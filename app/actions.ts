"use server";

import client from "@/lib/mongodb";

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
