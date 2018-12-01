# FRMA Conceptual Map


### FRMA Ontology

(1) an overview of the problem you have been working on and of the ontology itself
(2) a paragraph description of your ontology overview diagram
(3) at least 3 other diagrams that, together with your text descriptions, document the ontology


### Hair Ontology

(1) an overview of the problem you have been working on and of the ontology itself
(2) a paragraph description of your ontology overview diagram
(3) at least 3 other diagrams that, together with your text descriptions, document the ontology


### Image Ontology

The Image Ontology encapsulates the metadata required to describe images in the context of the FRMA project. Specifically, it defines an Image class and numerous subclasses that can describe the fidelity, color, lighting conditions, and pose of a particular image.

The attached diagrams show

(1) an overview of the problem you have been working on and of the ontology itself
(2) a paragraph description of your ontology overview diagram
(3) at least 3 other diagrams that, together with your text descriptions, document the ontology


### Machine Learning Model Ontology

(1) an overview of the problem you have been working on and of the ontology itself
(2) a paragraph description of your ontology overview diagram
(3) at least 3 other diagrams that, together with your text descriptions, document the ontology


### Person, Face, and Demographic Ontology

(1) an overview of the problem you have been working on and of the ontology itself
(2) a paragraph description of your ontology overview diagram
(3) at least 3 other diagrams that, together with your text descriptions, document the ontology


### Wearable Things Ontology

When dealing with facial recognition of images, it is fairly normal for the people in the images to be wearing some type of clothing or accessory. It is also reasonable for those pieces of clothing to effectively block a part of the image of someone’s face, to occlude the face in other words. The WearableThingsOntology was created to be a simple to use method of keeping track of the various clothing and accessories that could potentially mess with a facial recognition algorithm. This ontology exists to be used by the higher up FRMA ontology that imports it. From there, it acts as a place to hold potential sources of occlusion that also happen to be wearable things/accessories.

When viewed in a vacuum, the ontologies simplicity is one of it’s best points. It holds a simple tree like structure of is-a relationships between the different concepts that we currently have in our dataset, all of which span from the root concept of being some “wearable thing.” When view in conjunction with the rest of the project, the different concepts within WearableThingsOntology are connected to the FRMA concept of occlusions through the idea that the objects within WTO will typically be a source of a specific type of occlusion. Expressed concisely, (Forall WTO:SomeObject (Exist FRMA:Occlusion [WTO:SomeObject   FRMA:isOcclusionSourceOf   FRMA:Occlusion])).
