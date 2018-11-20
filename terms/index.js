const Promise = require('bluebird')
const csv = require('csvtojson')
const fs = require('fs')

const ho = require('./ho.json')
const pfd = require('./pfd.json')
const image = require('./image.json')
const frma = require('./frma.json')
const wto = require('./wto.json')
const mlmo = require('./mlmo.json')

const ontologies = [
  ho,
  pfd,
  image,
  frma,
  wto,
  mlmo
]

// // // //

// Defines the path to the CSV file
// NOTE - this filepath is relative to the
// parent directory where this script is run
const CSV_FILEPATH = './terms.csv'
const LABEL = 'rdfs:label'
const VALUE = '@value'

let termCount = 0;
let noTermCount = 0;
let noTerms = []

// Opens CSV file
csv().fromFile(CSV_FILEPATH)
.then((collection)=>{

  console.log('CSV Rows: ' + collection.length);

  // Iterates over each ontology
  ontologies.forEach((ontology) => {
    ontology['@graph'] = ontology['@graph'].map((node) => {
      if (!node[LABEL]) {
        return node
      } else {

        let nodeLabel
        if (typeof node[LABEL] === 'string') {
          nodeLabel = node[LABEL]
        } else {
          if (Array.isArray(node[LABEL])) {
            let shifted = node[LABEL].shift()
            nodeLabel = shifted[VALUE]
          } else {
            nodeLabel = node[LABEL][VALUE]
          }
        }

        // Finds associated term
        const term = collection.find(c => c.label.toLowerCase() === nodeLabel.toLowerCase() || c.label.toLowerCase().includes(nodeLabel.toLowerCase()) || nodeLabel.toLowerCase().includes(c.label.toLowerCase()))
        if (term) {
          // console.log('TERM!')
          // console.log(term)
          // console.log("\n")

          // node['skos:definition'] = {
          //   "@language": "en",
          //   "@value": term['field4']
          // }

          if (term.citation) {
            node['dct:bibliographicCitation'] = term.citation
          }

          termCount++
        } else {
          noTermCount++
          noTerms.push(nodeLabel)
        }
      }

      // Returns node from map function
      return node

    })

    fs.writeFileSync('out.ld.json', JSON.stringify(ontology, null, 2))
  })


  console.log('TermsFound: ' + termCount)
  console.log('NoTermsFound: ' + noTermCount)
  console.log(noTerms)

})

