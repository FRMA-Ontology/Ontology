# Ontology Conceptual Map

We now generate our conceptual map diagrams with the Protege [OntoGraf](https://protegewiki.stanford.edu/wiki/OntoGraf) plugin.

The OntoGraf plugin will show all classes by default - because we only want to show the classes we've created, we can configure OntoGraph's search feature to only show the results we want.


Paste the following regular expression into the OntoGraf search to display the desired classes:

```regex
^(face|image|skin|hair|ornament|image fidelity|demographic|occlusion|makeup|\'hair texture\'|\'occluding wearable object\'|\'skin tone\'|\'balding\'|\'facial hair\'|\'weight range\'|\'age range\'|\'gender expression\'|\'optimal condition photo\'|\'pictorial element\'|\'image fidelity\'|jewelry|headwear|mouth|nose|cheek|eyewear|\'black and white image\'|\'mouth open state\'|bald|\'color image\'|shiny|\'facial expression\'|smiling|frowning)

```

Please update this regular expression as needed!