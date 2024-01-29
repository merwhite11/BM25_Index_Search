/*
# input: path to a built indx

#launch a server with a /search endpoint

# send a POST req to /search ->
  #params: with search phrase & max results

#launch a server that receives post reqs

#create a shell script that will
#run a server
#run a py script that makes a POST to server
#server aka index
#run a script to search index for matches
#returns a response
*/



const express = require('express')
const mongoose = require('mongoose');
const { MongoClient } = require('mongodb');
const app = express()
const port = 3000

// mongoose.connect('mongodb://localhost:27017/bm25', { useNewUrlParser: true, useUnifiedTopology: true });

// const documentSchema = new mongoose.Schema({
//   filename: String,
//   content: String,
//   metadata: {
//     filename: String,
//     size: Number
//   }
// });

// const Document = mongoose.model('Document', documentSchema);
const uri = 'mongodb://localhost:27017/bm25'
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true })

client.connect().then(() => {
  console.log('Connected to MongoDB');
}).catch(err => {
  console.error('Error connecting to MongoDB:', err);
});

// app.get('/', (req, res) => {
//   res.send('Connected to MongoDB and Express')
// })



//write a get req to the db
//calls db model function
//db model function that finds rec in collection and returns

app.get('/search', async (req, res) => {
  try {
    const collection = client.db('bm25').collection('index_0');
    const queryParam = res.req.q
    const documents = await collection.find({filename:'4.txt'}).toArray()

    res.json(documents);

    console.log('result', documents)
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' })
  }

})

app.listen(port, () => console.log(`Server started and listening at ${port}`))