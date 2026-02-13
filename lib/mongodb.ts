import { MongoClient } from "mongodb";

/**
 * MONGODB CONNECTION UTILITY
 * 
 * NOTE: Environment-Specific Workaround
 * Due to persistent DNS/Topology negotiation issues in Node.js v24 on this Windows 
 * environment, we use a single-host direct connection to Atlas shard-00-00.
 * This bypasses SRV lookups and replica set discovery which were causing timeouts.
 */
const uri = "mongodb://Vercel-Admin-atlas-amber-gardenc:XGrObDyQBHhk9TN5@ac-8tkitlg-shard-00-00.ff23ewx.mongodb.net:27017/?authSource=admin&ssl=true&directConnection=true";

const client = new MongoClient(uri, {
  serverSelectionTimeoutMS: 15000,
  connectTimeoutMS: 15000,
});

export default client;
