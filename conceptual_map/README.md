# FRMA Conceptual Map Documentation

This documentation details an overview of the FRMA project and its associated ontologies.

<a href="https://frma-ontology.github.io/diagrams/#/map" target="_blank" style="font-size: 1.5rem;">Interactive FRMA Conceptual Diagrams Available Here</a>

### FRMA Ontology
**Overview**

Machine learning allows us to learn a model for a given task such as facial recognition with a high degree of accuracy. However, after these models are generated they are often treated as black boxes and the limitations of a model are often unknown to the end user. Facial Recognition Model Analyzer (FRMA) provides an intuitive interface to explore the limits of a facial recognition model by integrating “smart” images that semantically describe their subject and Kumar [2] features, with classification results aimed at uncovering common causes for misclassifications (including occlusions and wearable objects).

<img style="width: 100%;" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/frma.jpg" />

FRMA specifically outlines the concepts of “occlusions” and “wearable objects.” Wearable objects are items recognized by facial recognition algorithms (e.g., eyeglasses, earrings, hats). FRMA breaks these items into two categories; headwear (e.g., eyeglasses, hats) and ornaments (e.g., jewelry, neckwear, and makeup). Occlusions model the concept of something that blocks the view of the subject within an image. FRMA breaks occlusions into two further categories; cervical occlusions (anything obstructing the subject’s neck), and facial occlusions (modeling the upper and lower portions of the subject’s face separately).



### Hair Ontology
**Overview**

The Hair Ontology aims to more precisely describe the hair on the subject’s head and/or face. Because human hair is incredibly varied, the hair ontology focuses on multiple traits to more completely describe a person’s head and/or facial hair.

<img style="width: 100%;" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/hair.jpg" />

**Detail**

The Hair Ontology includes subclasses for hair location, color, texture, and haircut. Location is broken into further subclasses like facial hair and balding. This allows for more detailed description of facial hair and other traits that are usually a binary option in traditional models.

<img style="width: 100%" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/detail/OE_X_HairOntology-detail-02.svg.jpg" />

This gives our queries the requisite vocabulary to answer competency questions like, ““Which of these two models is better at classifying people with long hair?"



### Image Ontology
**Overview**

Image Ontology enables the FRMA system to classify the properties of individual image files. This metadata includes semantic descriptors of the visual image and its subject rather than native image metadata describing camera settings and file information. FRMA is interested in semantically defining the dearth of content within the image rather than merely interpreting the image itself as a flat photograph.

<img style="width: 100%;" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/img.jpg" />

**Detail**

The Image Ontology encapsulates the metadata required to describe images in the context of the FRMA project.

<img style="width: 100%" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/detail/OE_X_ImageOntology-detail-02.svg.jpg" />

Specifically, the Image Ontology defines an Image class and numerous subclasses that describe descriptors like fidelity, color, lighting conditions, and pose.



### Machine Learning Model Ontology
**Overview**

The Machine Learning Model Ontology allows users to describe the learning process, the structure of the learned model, and the evaluation of the model from a data-centric perspective.

<img style="width: 100%;" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/mlmo.jpg" />

**Detail**

This ontology defines the provenance used throughout the testing data. It is also used to model the concepts of testing and training ML models, each of which is a subclass of an activity. Many machine learning ontologies describe models using simple text fields or overly simplified Latex equations. However, the Machine Learning Model Ontology allows users to describe their model in RDF allowing developers to describe their model layer by layer. This allows future users to more easily understand the model's architecture and more confidently reuse their systems.

<img style="width: 100%" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/detail/OE_X_MachineLearningModelOntology-detail-02.svg.jpg" />




### Person, Face, and Demographic Ontology
**Overview**

This sub-ontology focuses specifically on a person’s demographic and facial features that appear in their images, including facial expression, age range, and nose shape.

<img style="width: 100%;" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/pfd.jpg" />

**Detail**

A “person” is the subject or face that is analyzed by FRMA.

<img style="width: 100%" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/detail/OE_X_PersonFaceAndDemographicOntology-detail-01.svg.jpg" />

A “face” is defined by visual descriptors including face shape, facial expression, nose size, face size, and skin tone.

<img style="width: 100%" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/detail/OE_X_PersonFaceAndDemographicOntology-detail-02.svg.jpg" />

“Demographic” is used to define things like age range, ethnicity, gender expression, and weight range.




### Wearable Things Ontology
**Overview**

When dealing with facial recognition, people in the images may be wearing some type of clothing or accessory. Those pieces of clothing may effectively block a part of or occlude someone’s face. The Wearable Things Ontology was created to keep track of various clothing and accessories that could disrupt a facial recognition algorithm. This ontology acts as a place to hold potential sources of occlusion that also happen to be wearable things.

<img style="width: 100%;" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/wto.jpg" />


**Detail**

It holds a simple tree like structure of is-a relationships between the different concepts that we currently have in our dataset, all of which span from the root concept of being some “wearable thing.”

<img style="width: 100%" src="https://raw.githubusercontent.com/FRMA-Ontology/diagrams/master/concept-maps/oe_12/jpg/detail/OE_X_WearableThingsOntology-detail-01.svg.jpg" />

When viewed in conjunction with the rest of the project, the different concepts within Wearable Things Ontology (WTO) are connected to the FRMA concept of occlusions through the idea that the objects within WTO will typically be occlusive. Expressed concisely, (Forall WTO:SomeObject (Exist FRMA:Occlusion [WTO:SomeObject   FRMA:isOcclusionSourceOf   FRMA:Occlusion])).
