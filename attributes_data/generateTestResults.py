import rdflib
from rdflib.namespace import RDF, Namespace, OWL, XSD, RDFS
import sys

# python generateTestResults.py ALGORITHM_NAME PATH_TO_RESULTS_FILE PATH_TO_OUTPUT_RDF_FILE.ttl




def generate_results(results_filepath, algorithm_name, output_filepath):
    graph = rdflib.Graph()

    # Create resultset
    resultset_IRI = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/OE_9_FRMA_Individuals/" + algorithm_name + "Test01ResultSet")
    graph.add((resultset_IRI, RDF.type, OWL.NamedIndividual))
    graph.add((resultset_IRI, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/ResultSet")))
    graph.add((resultset_IRI, RDFS.label, rdflib.term.Literal(algorithm_name, datatype=XSD.string)))

    with open(results_filepath) as fp:
        for cnt, line in enumerate(fp):
            lsplit = line.split("\t")

            testimage = lsplit[0]+lsplit[1]
            tag = lsplit[3]
            print("testimage: " + testimage + ", " + "guess: " + tag)


            base_iri = "https://tw.rpi.edu/web/Courses/Ontologies/2018/OE_9_FRMA_Individuals/Image/" + lsplit[0].replace("_", "") + "/"+lsplit[1]
            image_IRI = rdflib.term.URIRef(base_iri + "/Image")

            hasFeature = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/hasFeature")
            hasConstituent = rdflib.term.URIRef("http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/hasConstituent")
            hasTag = rdflib.term.URIRef("http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/hasTag")


            # Create the result
            result_IRI = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/OE_9_FRMA_Individuals/" + algorithm_name + "Test01ResultSetResult" + str(cnt))
            graph.add((result_IRI, RDF.type, OWL.NamedIndividual))
            graph.add((result_IRI, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/Result")))
            graph.add((result_IRI, hasTag, rdflib.term.Literal(lsplit[3].replace("_", " "), datatype=XSD.string)))
            graph.add((result_IRI, hasFeature, image_IRI))
            graph.add((resultset_IRI, hasConstituent, result_IRI))
            # break

    graph.serialize(destination=output_filepath+".ttl", format='turtle')



if __name__ == "__main__":
    # python generateTestResults.py ALGORITHM_NAME PATH_TO_RESULTS_FILE PATH_TO_OUTPUT_RDF_FILE.ttl
    if len(sys.argv) != 4:
        print("Run as 'python generateTestResults.py ALGORITHM_NAME PATH_TO_RESULTS_FILE PATH_TO_OUTPUT_RDF_FILE.ttl'")
        sys.exit(0)
    else:
        # run the program:
        generate_results(sys.argv[2], sys.argv[1], sys.argv[3])