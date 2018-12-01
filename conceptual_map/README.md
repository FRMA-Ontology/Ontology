# FRMA Conceptual Map


### FRMA Ontology

Machine learning allows us to learn a model for a given task such as facial recognition with a high degree of accuracy. However, after these models are generated they are often treated as black boxes and the limitations of a model are often unknown to the end user. Facial Recognition Model Analyzer (FRMA) provides an intuitive interface to explore the limits of a facial recognition model by integrating “smart” images that semantically describe their subject and Kumar [2] features, with classification results aimed at uncovering common causes for misclassifications (including occlusions and wearable objects).

FRMA specifically outlines the concepts of “occlusions” and “wearable objects.” Wearable objects are items recognized by facial recognition algorithms (e.g., eyeglasses, earrings, hats). FRMA breaks these items into two categories; headwear (e.g., eyeglasses, hats) and ornaments (e.g., jewelry, neckwear, and makeup). Occlusions model the concept of something that blocks the view of the subject within an image. FRMA breaks occlusions into two further categories; cervical occlusions (anything obstructing the subject’s neck), and facial occlusions (modeling the upper and lower portions of the subject’s face separately).

(3) at least 3 other diagrams that, together with your text descriptions, document the ontology



### Hair Ontology

The Hair Ontology aims to more precisely describe the hair on the subject’s head and/or face. Because human hair is incredibly varied, the hair ontology focuses on multiple traits to more completely describe a person’s head and/or facial hair.

The Hair Ontology includes subclasses for hair location, color, texture, and haircut. Location is broken into further subclasses like facial hair and balding. This allows for more detailed description of facial hair and other traits that are usually a binary option in traditional models. This gives our queries the requisite vocabulary to answer competency questions like, ““Which of these two models is better at classifying people with long hair?"

(3) at least 3 other diagrams that, together with your text descriptions, document the ontology


### Image Ontology

Image Ontology enables the FRMA system to classify the properties of different image files.

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
