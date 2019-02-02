// read config
const configFile = cat('config.json')
const { dbName, dbCollection }  = JSON.parse(configFile)

// open db connection
const conn = new Mongo();
const db = conn.getDB(dbName);

const collection = db[dbCollection];

// create text index
collection.createIndex({ text: "text" });

// test everything works
// const document = collection.findOne( { $text: { $search: 'host'} } );
// printjson(document);
