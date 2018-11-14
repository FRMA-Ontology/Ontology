require('dotenv').config()
const fs = require('fs')
const path = require('path')
const request = require('request')
const Promise = require('bluebird')

// // // //

// Pulls Blazegraph host information from environment
const { BLAZEGRAPH_HOST, BLAZEGRAPH_PORT, BLAZEGRAPH_NAMESPACE } = process.env

// Defines which FRMA ontologies to load
const ontologies = ['HO.rdf', 'MLMO.rdf', 'WT.rdf', 'IMG.rdf', 'PFD.rdf', 'FRMA.rdf']

// Loads a single data file into Blazegraph
function loadData(file) {

  // Reads in the data file as UTF-8
  const data = fs.readFileSync(path.join('../../', file), 'utf8')

  // Returns a Promise to handle async behavior
  return new Promise((resolve, reject) => {

    // Assembles request options
    const request_options = {
      url: `http://${BLAZEGRAPH_HOST}:${BLAZEGRAPH_PORT}/blazegraph/namespace/${BLAZEGRAPH_NAMESPACE}/sparql`,
      headers: {
        'Content-type': 'application/rdf+xml'
      },
      body: data
    }

    // Dispatches request to blazegraph, resolves or rejects promise
    request.post(request_options, (err, resp, body) => {
      if (err) { return reject(err) }
      console.log('Loaded ' + file)
      return resolve(body)
    })
  })
}


// Iterates over each ontology and loads the file into Blazegraph
Promise.each(ontologies, o => loadData(o))
.then(() => {
  console.log('Done!')
  process.exit(0)
})
