# SPARQL Queries


#### Accuracy Query
This query calculates the accuracy of images across a result set. It can be modified with image/person restrictions to calculate accuracy across images with a specific conditions (Long Hair, mug shots, etc.). Note for our current data, we have generate classification results artificially - FaceNet and DLib will have a 50% accuracy such that when one misclassified an image the other will identify it correctly.


#### Mugshot
The query below returns the image IRI and the depicted persons name for every image that is inferred by the ontology to be a mugshot photo. Because this query relies on the inferencing in our ontology it can only run in the Snap SPARQL Query, which when a reasoner is run generates the extra inferred triple: image rdf:type MugShotPhoto. In the future we plan to run an inference engine to generate these triples and include them in our triple store.


#### Occlusion Accuracy
This is the query for the competency question, “Q: What part of the face does my facial recognition model depend on the most?” What the query actually grabs is the accuracy rate for all sources of occlusion in the individuals that are used, along with the type of the occlusion source object. From here, we can use a seperate description logic inferencing software to connect the type of the occlusion source to the body region being occluded and so answer the question.


#### Johnny Depp


#### Misclassified Attributes
