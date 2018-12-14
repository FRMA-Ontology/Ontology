import rdflib
from rdflib.namespace import RDF, Namespace, OWL, XSD, RDFS


filepath = 'dlib_results.txt'
algorithm = 'DLib'# 'FaceNet'

graph = rdflib.Graph()


# Create resultset
resultset_IRI = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/OE_9_FRMA_Individuals/" + algorithm + "Test01ResultSet")
graph.add((resultset_IRI, RDF.type, OWL.NamedIndividual))
graph.add((resultset_IRI, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/ResultSet")))
graph.add((resultset_IRI, RDFS.label, rdflib.term.Literal(algorithm, datatype=XSD.string)))

with open(filepath) as fp:
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
        result_IRI = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/OE_9_FRMA_Individuals/" + algorithm + "Test01ResultSetResult" + str(cnt))
        graph.add((result_IRI, RDF.type, OWL.NamedIndividual))
        graph.add((result_IRI, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/Result")))
        graph.add((result_IRI, hasTag, rdflib.term.Literal(lsplit[3].replace("_", " "), datatype=XSD.string)))
        graph.add((result_IRI, hasFeature, image_IRI))
        graph.add((resultset_IRI, hasConstituent, result_IRI))
        # break

graph.serialize(destination=filepath+".ttl", format='turtle')
