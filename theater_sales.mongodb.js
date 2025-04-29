const fs = require("fs");
use("demo");
const docs = EJSON.parse(fs.readFileSync("./theater_sales.json"))

const collectionName = "theater_sales";
const collection = db.getCollection(collectionName);

collection.deleteMany({});

collection.insertMany(docs);

collection.createIndex({ day: 1, theater: 1 });
collection.createIndex({ theater: 1 });
collection.createIndex({ day: 1, "sales.movie": 1, theater: 1 });
