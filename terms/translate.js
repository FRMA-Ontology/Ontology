const fs = require('fs')
const path = require('path')
const Promise = require('bluebird')
const rdfTranslator = require('rdf-translator')

// // // //

// Constants
const SRC_ROOT = '../'
const DEST_ROOT = './json-ld'
const FORMAT_XML = 'xml'
const FORMAT_N3 = 'n3'
const FORMAT_JSONLD = 'json-ld'

// Converts a file (src) in one format (srcFormat) another file (des) in another format (destFormat)
function convertFile({ src, dest }) {
  return new Promise((resolve, reject) => {

    // Reads in RDF/XML
    const input = fs.readFileSync(path.resolve(SRC_ROOT, src))

    // Sends to RDF translator
    rdfTranslator(input, FORMAT_XML, FORMAT_JSONLD)
    .then(data => {
      fs.writeFileSync(path.resolve(DEST_ROOT, dest), data)
      console.log('Translated ' + dest)
      return resolve(data)
    }).catch(err => {
      console.error(err);
    });
  })

}

// // // //

const ONTOLOGY_HO = 'OE_X_HairOntology.rdf'
const ONTOLOGY_FRMA = 'OE_X_FRMA.rdf'
const ONTOLOGY_IMAGE = 'OE_X_ImageOntology.rdf'
const ONTOLOGY_MLMO = 'OE_X_MachineLearningModelOntology.rdf'
const ONTOLOGY_PFD = 'OE_X_PersonFaceAndDemographicOntology.rdf'
const ONTOLOGY_WTO = 'OE_X_WearableThingsOntology.rdf'

console.log('Translating ontologies...')
Promise.all([
  convertFile({ src: ONTOLOGY_HO, dest: 'ho.json' }),
  convertFile({ src: ONTOLOGY_FRMA, dest: 'frma.json' }),
  convertFile({ src: ONTOLOGY_IMAGE, dest: 'image.json' }),
  convertFile({ src: ONTOLOGY_MLMO, dest: 'mlmo.json' }),
  convertFile({ src: ONTOLOGY_PFD, dest: 'pfd.json' }),
  convertFile({ src: ONTOLOGY_WTO, dest: 'wto.json'  })
]).then(() => {
  console.log('DONEZO')
})