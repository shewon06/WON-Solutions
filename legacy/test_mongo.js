const { MongoClient } = require('mongodb');

const uri = "mongodb+srv://Vercel-Admin-atlas-amber-gardenc:XGrObDyQBHhk9TN5@atlas-amber-gardenc.ff23ewx.mongodb.net/?retryWrites=true&w=majority";

async function run() {
    const client = new MongoClient(uri, { serverSelectionTimeoutMS: 10000 });
    try {
        console.log("Connecting to MongoDB...");
        await client.connect();
        await client.db("admin").command({ ping: 1 });
        print("Pinged your deployment. You successfully connected to MongoDB!");
    } catch (e) {
        console.error("Connection failed:", e);
    } finally {
        await client.close();
    }
}
run();
