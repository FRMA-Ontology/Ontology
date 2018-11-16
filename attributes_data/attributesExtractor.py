""" Notes that I have to improve:
currently file paths are relative to the top level folder of images, I don't have their entire filepath and it would be different
depending on the computer. We can change it once we get our website portal set up.

Not sure what the deal is with image ID

currently we assume that if they aren't male they're female



"""


import rdflib
from rdflib.namespace import RDF, Namespace, OWL, XSD, RDFS

# these imports are for copying images to a new folder when trying to find images that match criteria
import shutil, os

attributeLabels = """person	imagenum	Male	Asian	White	Black	Baby	Child	Youth	Middle Aged	Senior	Black Hair	Blond Hair	Brown Hair	Bald	No Eyewear	Eyeglasses	Sunglasses	Mustache	Smiling	Frowning	Chubby	Blurry	Harsh Lighting	Flash	Soft Lighting	Outdoor	Curly Hair	Wavy Hair	Straight Hair	Receding Hairline	Bangs	Sideburns	Fully Visible Forehead	Partially Visible Forehead	Obstructed Forehead	Bushy Eyebrows	Arched Eyebrows	Narrow Eyes	Eyes Open	Big Nose	Pointy Nose	Big Lips	Mouth Closed	Mouth Slightly Open	Mouth Wide Open	Teeth Not Visible	No Beard	Goatee	Round Jaw	Double Chin	Wearing Hat	Oval Face	Square Face	Round Face	Color Photo	Posed Photo	Attractive Man	Attractive Woman	Indian	Gray Hair	Bags Under Eyes	Heavy Makeup	Rosy Cheeks	Shiny Skin	Pale Skin	5 o' Clock Shadow	Strong Nose-Mouth Lines	Wearing Lipstick	Flushed Face	High Cheekbones	Brown Eyes	Wearing Earrings	Wearing Necktie	Wearing Necklace"""
attributeList = attributeLabels.strip().split("\t")

individualsNamespaceString = "http://tw.rpi.edu/web/Courses/Ontologies/2017/OE_9_FRMA_Individuals/"

def load_attributes_file(filename = "lfw_attributes.txt"):
	# loads the file and creates a dictionary of names to image numbers to image attributes.
	data = {}
	names = []
	try:
		f = open(filename)
	except Exception as e:
		print("Error opening file:", filename, " : ", e)
	else:
		for line in f.readlines():
			if line.strip()[0] == "#":
				# then skip to the next line because this one is a comment
				continue
			s = line.split("\t")
			name = s[0].lower().strip()
			if name not in names:
				names += [name]
			imagenum = int(s[1]) - 1
			if name not in data:
				data[name] = []
			while len(data[name]) <= imagenum:
				 # this is a hacky way to do this but I wanted to make sure it could handle it if the images are out of order
				data[name] += [{}]
			for i in range(len(s)):
				if i == 0:
					# the person's name
					data[name][imagenum][attributeList[i]] = s[i]
				elif i == 1:
					# the image number
					data[name][imagenum][attributeList[i]] = int(s[i])
				else:
					# the percent chance for all of these
					data[name][imagenum][attributeList[i]] = float(s[i])
		f.close()
	return data, names


def basic_text_query(tags, names):
	name = "asfd"
	while len(name) > 0:
		name = input("Enter image name: ").lower().strip()
		if name in tags:
			numImages = len(tags[name])
			imageNumber = -1
			while imageNumber < 1 or imageNumber > numImages:
				print("There are", numImages, "images for this person.")
				imageNumber = int(input("Enter the image number you want: "))
				# currently can't handle not entering a valid number but this is internal anyways
			imageIndex = imageNumber - 1
			# print(tags[name][imageIndex])
			print() # new line
			for attribute in attributeList[2:]:
				print(attribute, " : ", tags[name][imageIndex][attribute] > 0)
			print()
		elif len(name) > 0:
			print("Name", name, "is not in tags")

def output_labeled_everything(tags, names, output_file):
	f = open(output_file, "w")

	all_text_labeled = ""
	numMissingData = 0
	for name in names:
		# output the data to a text file so it's easier to read:
		images = tags[name]
		for imageNum in range(len(images)):
			image = images[imageNum]
			if (len(image) == 0):
				print("Error on image", imageNum+1, "for person:", name, "- image has no data")
				numMissingData += 1
				continue
			for attribute in attributeList[:2]:
				# the name and image number shouldn't be converted into booleans
				all_text_labeled += attribute + " : " + str(image[attribute]) + "\n"
			for attribute in attributeList[2:]:
				all_text_labeled += attribute + " : " + str(image[attribute] > 0) + "\n"
			all_text_labeled += "\n"
		all_text_labeled += "\n"
	f.write(all_text_labeled)

	f.close()
	print(numMissingData, "Images missing label data")

def generate_rdf_individuals(names, tags, base_filename, output_filename, generateFakeResults, restricted_images = None ):
	# for every name, create the RDF individuals for each of their images.
	g = rdflib.Graph()
	g.parse(base_filename)
	# print(len(g)) # testing out how this library works
	# for subj, pred, obj in g:
	# 	print(type(subj))
	# 	if (subj, pred, obj) not in g:
	# 		raise Exception("It better be!")

	id = 1
	if (restricted_images):
		restricted_images = [(x[0].lower(), x[1]) for x in restricted_images]
	for name in names:
		photos = tags[name]

		for photo_num in range(len(photos)):
			# add the info for this photo:
			if (restricted_images):
				if (name, photo_num+1) not in restricted_images: # added 1 since images have base number 1 not 0
					continue
				if generateFakeResults:
					add_image_to_graph(photos[photo_num], g, id)
					id = id + 1
				else:
					add_image_to_graph(photos[photo_num], g, 0)
	# here add another triple to test this
	# instantiatedNamespace = Namespace(individualsNamespaceString)
	# g.add((instantiatedNamespace.ThisIsATest, RDF.type, OWL.NamedIndividual))
	# g.add((instantiatedNamespace.ThisIsATest, rdflib.term.URIRef('https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/hasDemographic'), OWL.NamedIndividual))
	# print("PRedicats", list(g.predicates()))

	o = clean_up_xml_string(g.serialize(format='pretty-xml').decode("utf-8"))
	output_file = open(output_filename, "w")
	output_file.write(o)
	output_file.close()

def add_image_to_graph(image_data, graph, generateFakeResultId):
	# this adds image stuff
	"""
	Things we need to do:
	Create the image, create the person, create the image, create the result set, add the image to the result set
	"""

	if len(image_data) == 0:
		print("Tried to add image to graph that had no data")
		return

	base_iri = "https://tw.rpi.edu//web/Courses/Ontologies/2017/OE_9_FRMA_Individuals/"
	# image_iri = "https://tw.rpi.edu//web/Courses/Ontologies/2017/OE_8_FRMA_Individuals/Image/PERSON_NAME/IMAGENUM"

	person_name = image_data["person"]
	person_id = person_name.replace(" ", "")
	# print(person_id)
	image_IRI = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]))



	if generateFakeResultId > 0:
		hasFeature = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/hasFeature")
		hasConstituent = rdflib.term.URIRef("http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/hasConstituent")
		hasTag = rdflib.term.URIRef("http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/hasTag")

		resultset_facenet_IRI = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2017/OE_9_FRMA_Individuals/FaceNetTest01ResultSet")
		result_facenet_IRI = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2017/OE_9_FRMA_Individuals/FaceNetTest01ResultSet/Result" + str(generateFakeResultId))

		resultset_dlib_IRI = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2017/OE_9_FRMA_Individuals/dlibTest01ResultSet")
		result_dlib_IRI = rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2017/OE_9_FRMA_Individuals/dlibTest01ResultSet/Result" + str(generateFakeResultId))

		graph.add((resultset_facenet_IRI, hasConstituent, result_facenet_IRI))
		graph.add((resultset_facenet_IRI, RDFS.label, rdflib.term.Literal("FaceNet", datatype=XSD.string)))

		graph.add((resultset_dlib_IRI, hasConstituent, result_dlib_IRI))
		graph.add((resultset_dlib_IRI, RDFS.label, rdflib.term.Literal("DLib", datatype=XSD.string)))

		if (generateFakeResultId % 2) == 1: # every other answer
			graph.add((result_facenet_IRI, hasTag, rdflib.term.Literal(person_name, datatype=XSD.string)))
			graph.add((result_dlib_IRI, hasTag, rdflib.term.Literal("Steve Erwin", datatype=XSD.string)))
		else:
			graph.add((result_facenet_IRI, hasTag, rdflib.term.Literal("Steve Erwin", datatype=XSD.string)))
			graph.add((result_dlib_IRI, hasTag, rdflib.term.Literal(person_name, datatype=XSD.string)))
		graph.add((result_dlib_IRI, hasFeature, image_IRI))
		graph.add((result_facenet_IRI, hasFeature, image_IRI))


	# create the base image class
	graph.add((image_IRI, RDF.type, OWL.NamedIndividual))
	# graph.add((image_IRI, RDF.type, rdflib.term.URIRef("http://purl.org/net/lio#Image")))

	if (image_data["Posed Photo"] > 0):

		graph.add((image_IRI, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/ImageOntology/PosedImage")))
	else:
		graph.add((image_IRI, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/ImageOntology/CandidImage")))

	if (image_data["Color Photo"] > 0):
		graph.add((image_IRI, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/ImageOntology/ColorImage")))
	else:
		graph.add((image_IRI, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/ImageOntology/BlackAndWhiteImage")))


	image_filepath = person_name.replace(" ", "_") + "/" + person_name.replace(" ", "_") + "_" + "%04d" % (image_data["imagenum"],) + ".jpg"
	graph.add((image_IRI, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/ImageOntology/hasFilePath"), rdflib.term.Literal(image_filepath, datatype=XSD.anyURI)))
	graph.add((image_IRI, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/ImageOntology/hasFileExtension"), rdflib.term.Literal(".jpg", datatype=XSD.string)))


	# create the lighting information
	# "https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/ImageOntology/Lighting_Variation"
	# graph.add((image_IRI, RDF.type, OWL.NamedIndividual))

	pfd_iri = "https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology"
	hasPart = rdflib.term.URIRef("http://purl.obolibrary.org/obo/BFO_0000051")

	# create the person
	person_iri = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person")
	graph.add((person_iri, RDF.type, OWL.NamedIndividual))
	graph.add((person_iri, RDF.type, rdflib.term.URIRef("https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person")))
	graph.add((person_iri, rdflib.term.URIRef("http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/hasName"), rdflib.term.Literal(person_name, datatype=XSD.string)))
	# create the face
	face_iri = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Face")
	graph.add((face_iri, RDF.type, OWL.NamedIndividual))
	graph.add((face_iri, RDF.type, rdflib.term.URIRef("http://purl.obolibrary.org/obo/UBERON_0001456")))
	graph.add((person_iri, hasPart, face_iri))

	graph.add((image_IRI, rdflib.term.URIRef("http://purl.org/net/lio#depicts"), person_iri))

	# demographic:
	if (image_data["Asian"] > 0):
		graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/hasDemographic"), rdflib.term.URIRef(pfd_iri + "/Asian")))
	if (image_data["White"] > 0):
		graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/hasDemographic"), rdflib.term.URIRef(pfd_iri + "/White")))
	if (image_data["Black"] > 0):
		graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/hasDemographic"), rdflib.term.URIRef(pfd_iri + "/Black")))
	if (image_data["Indian"] > 0):
		graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/hasDemographic"), rdflib.term.URIRef(pfd_iri + "/Indian")))

	if (image_data["Strong Nose-Mouth Lines"] > 0):
		graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/hasStrongNoseMouthLines"), rdflib.term.Literal(True, datatype=XSD.boolean)))
	else:
		graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/hasStrongNoseMouthLines"), rdflib.term.Literal(False, datatype=XSD.boolean)))

	if (image_data["Attractive Man"] > 0 or image_data["Attractive Woman"] > 0):
		graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/isAttractive"), rdflib.term.Literal(True, datatype=XSD.boolean)))
	else:
		graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/isAttractive"), rdflib.term.Literal(False, datatype=XSD.boolean)))


	gender_iri = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/Gender")
	graph.add((gender_iri, RDF.type, OWL.NamedIndividual))
	graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/hasDemographic"), gender_iri))
	if (image_data["Male"] > 0):
		graph.add((gender_iri, RDF.type, rdflib.term.URIRef(pfd_iri + "/Masculine")))
	else:
		# currently we assume that if they aren't male they're female
		graph.add((gender_iri, RDF.type, rdflib.term.URIRef(pfd_iri + "/Feminine")))


	age_range_iri = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/AgeRange")
	graph.add((age_range_iri, RDF.type, OWL.NamedIndividual))
	graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/hasDemographic"), age_range_iri))

	# these need to be disjoint
	if (image_data["Baby"] > 0):
		graph.add((age_range_iri, RDF.type, rdflib.term.URIRef(pfd_iri + "/Baby")))
	else:
		if (image_data["Child"] > 0):
			graph.add((age_range_iri, RDF.type, rdflib.term.URIRef(pfd_iri + "/Child")))
		else:
			if (image_data["Youth"] > 0):
				graph.add((age_range_iri, RDF.type, rdflib.term.URIRef(pfd_iri + "/Youth")))
			else:
				if (image_data["Middle Aged"] > 0):
					graph.add((age_range_iri, RDF.type, rdflib.term.URIRef(pfd_iri + "/Middle_Aged")))
				else:
					if (image_data["Senior"] > 0):
						graph.add((age_range_iri, RDF.type, rdflib.term.URIRef(pfd_iri + "/Senior")))

	weight_iri = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/AgeRange")
	graph.add((weight_iri, RDF.type, OWL.NamedIndividual))
	graph.add((person_iri, rdflib.term.URIRef(pfd_iri + "/hasDemographic"), weight_iri))
	if (image_data["Chubby"] > 0):
		graph.add((weight_iri, RDF.type, rdflib.term.URIRef(pfd_iri + "/Chubby")))
	else:
		graph.add((weight_iri, RDF.type, rdflib.term.URIRef(pfd_iri + "/Skinny")))


	# wearables:
	wt_iri = "https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/WearableThingsOntology"
	eyewear_iri = base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/Eyewear"
	if (image_data["Eyeglasses"] > 0):
		# make an eyeglasses individual
		wearing_item_class = "Eyeglasses"
		wearable_individual = rdflib.term.URIRef(eyewear_iri + "/" + wearing_item_class)
		graph.add((wearable_individual, RDF.type, OWL.NamedIndividual))
		graph.add((wearable_individual, RDF.type, rdflib.term.URIRef(wt_iri + "/" + wearing_item_class)))
		# make the person wear them:
		graph.add((person_iri, rdflib.term.URIRef(wt_iri + "/isWearing"), wearable_individual))\

	if (image_data["Sunglasses"] > 0):
		# make an sunglasses individual
		wearing_item_class = "Sunglasses"
		wearable_individual = rdflib.term.URIRef(eyewear_iri + "/" + wearing_item_class)
		graph.add((wearable_individual, RDF.type, OWL.NamedIndividual))
		graph.add((wearable_individual, RDF.type, rdflib.term.URIRef(wt_iri + "/" + wearing_item_class)))
		# make the person wear them:
		graph.add((person_iri, rdflib.term.URIRef(wt_iri + "/isWearing"), wearable_individual))

	wearable_generic_things = [("Wearing Hat", "Hat"), ("Wearing Earrings", "Earrings"), ("Wearing Necktie", "Necktie"),
					("Wearing Necklace", "Necklace"), ("Wearing Lipstick", "Lipstick")]
	for t in wearable_generic_things:
		if (image_data[t[0]] > 0):
			# make an individual
			wearing_item_class = t[1]
			wearable_individual = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + wearing_item_class)
			graph.add((wearable_individual, RDF.type, OWL.NamedIndividual))
			graph.add((wearable_individual, RDF.type, rdflib.term.URIRef(wt_iri + "/" + wearing_item_class)))
			# make the person wear them:
			graph.add((person_iri, rdflib.term.URIRef(wt_iri + "/isWearing"), wearable_individual))

	if (image_data["Wearing Lipstick"] > 0 or image_data["Heavy Makeup"] > 0):
			# make a makeup individual
			wearing_item_class = "Makeup"
			wearable_individual = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + wearing_item_class)
			graph.add((wearable_individual, RDF.type, OWL.NamedIndividual))
			graph.add((wearable_individual, RDF.type, rdflib.term.URIRef(wt_iri + "/" + wearing_item_class)))
			# make the person wear them:
			graph.add((person_iri, rdflib.term.URIRef(wt_iri + "/isWearing"), wearable_individual))

			# mark whether or not it's heavy makeup
			graph.add((wearable_individual, rdflib.term.URIRef(pfd_iri + "/isHeavyMakeup"), rdflib.term.Literal(image_data["Heavy Makeup"] > 0, datatype=XSD.boolean)))

	# Hair:
	hair_iri_string = "https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/HairOntology"

	# create the head hair individual
	hair_name = "HeadHair"
	hair_individual = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + hair_name)
	graph.add((hair_individual, RDF.type, OWL.NamedIndividual))
	graph.add((hair_individual, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + hair_name)))
	graph.add((person_iri, hasPart, hair_individual))

	hair_texture = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + hair_name + "/HairTexture")
	graph.add((hair_individual, RDF.type, OWL.NamedIndividual))
	graph.add((hair_individual, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "HairTexture")))
	graph.add((hair_individual, rdflib.term.URIRef(hair_iri_string + "/" + "hasTexture"), hair_texture))

	# these need to be disjoint
	if (image_data["Curly Hair"] > 0):
		graph.add((hair_texture, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "CurlyHair")))
	else:
		if (image_data["Wavy Hair"] > 0):
			graph.add((hair_texture, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "WavyHair")))
		else:
			if (image_data["Straight Hair"] > 0):
				graph.add((hair_texture, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "StraightHair")))

	if (image_data["Bangs"] > 0):
		graph.add((hair_individual, rdflib.term.URIRef(hair_iri_string + "/" + "hasHaircut"), rdflib.term.URIRef(hair_iri_string + "/" + "Bangs")))
	else:
		hair_cut = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + hair_name + "/Haircut")
		graph.add((hair_cut, RDF.type, OWL.NamedIndividual))
		graph.add((hair_cut, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "Haircut")))
		graph.add((hair_individual, rdflib.term.URIRef(hair_iri_string + "/" + "hasHaircut"), hair_cut))

		# these need to be disjoint
		if (image_data["Receding Hairline"] > 0):
			graph.add((hair_cut, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "RecedingHairline")))
		else:
			if (image_data["Bald"] > 0):
				graph.add((hair_cut, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "Bald")))


	newColor = True
	if (image_data["Black Hair"] > 0):
		newColor = False
		graph.add((hair_individual, rdflib.term.URIRef(hair_iri_string + "/" + "hasHairColor"), rdflib.term.URIRef(hair_iri_string + "/" + "BlackHair")))

	if (image_data["Black Hair"] > 0):
		newColor = False
		graph.add((hair_individual, rdflib.term.URIRef(hair_iri_string + "/" + "hasHairColor"), rdflib.term.URIRef(hair_iri_string + "/" + "BlackHair")))

	if (image_data["Brown Hair"] > 0):
		newColor = False
		graph.add((hair_individual, rdflib.term.URIRef(hair_iri_string + "/" + "hasHairColor"), rdflib.term.URIRef(hair_iri_string + "/" + "BrownHair")))

	if (image_data["Gray Hair"] > 0):
		newColor = False
		graph.add((hair_individual, rdflib.term.URIRef(hair_iri_string + "/" + "hasHairColor"), rdflib.term.URIRef(hair_iri_string + "/" + "GrayHair")))

	if newColor:
		hair_color = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Hair/HairColor")
		graph.add((hair_color, RDF.type, OWL.NamedIndividual))
		graph.add((hair_color, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "HairColor")))
		graph.add((hair_individual, rdflib.term.URIRef(hair_iri_string + "/" + "hasHairColor"), hair_color))

	if (image_data["5 o' Clock Shadow"] > 0):
		graph.add((person_iri, hasPart, rdflib.term.URIRef(hair_iri_string + "/" + "FiveOClockShadow")))

	if (image_data["Bushy Eyebrows"] > 0):
		graph.add((person_iri, hasPart, rdflib.term.URIRef(hair_iri_string + "/" + "BushyEyebrows")))
	else:
		graph.add((person_iri, hasPart, rdflib.term.URIRef(hair_iri_string + "/" + "ThinEyebrows")))

	if (image_data["Goatee"] > 0):
		graph.add((person_iri, hasPart, rdflib.term.URIRef(hair_iri_string + "/" + "Goatee")))

	if (image_data["Sideburns"] > 0):
		facialHair = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "FacialHair0")
		graph.add((facialHair, RDF.type, OWL.NamedIndividual))
		graph.add((facialHair, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "Sideburn")))
		graph.add((person_iri, hasPart, facialHair))

	if (image_data["Mustache"] > 0):
		facialHair = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "FacialHair1")
		graph.add((facialHair, RDF.type, OWL.NamedIndividual))
		graph.add((facialHair, RDF.type, rdflib.term.URIRef(hair_iri_string + "/" + "Mustache")))
		graph.add((person_iri, hasPart, facialHair))


	hasVisualFeature = rdflib.term.URIRef(pfd_iri + "/" + "hasVisualFeature")

    # Face Stuff
	expressionIri = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Expression")
	graph.add((expressionIri, RDF.type, OWL.NamedIndividual))
	graph.add((face_iri, hasVisualFeature, expressionIri))
	graph.add((expressionIri, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "FacialExpression")))

	# these need to be disjoint
	if (image_data["Smiling"] > 0):
		graph.add((expressionIri, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "Smiling")))
	else:
		if (image_data["Frowning"] > 0):
			graph.add((expressionIri, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "Frowning")))

	if (image_data["Arched Eyebrows"] > 0):
		graph.add((expressionIri, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "ArchedEyebrow")))

	if (image_data["Narrow Eyes"] > 0):
		graph.add((expressionIri, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "NarrowEyes")))


	if (image_data["Round Jaw"] > 0):
		graph.add((face_iri, hasPart, rdflib.term.URIRef(pfd_iri + "/" + "RoundJaw")))

	if (image_data["Double Chin"] > 0):
		graph.add((face_iri, hasPart, rdflib.term.URIRef(pfd_iri + "/" + "DoubleChin")))


	hasShape = rdflib.term.URIRef(pfd_iri + "/" + "hasShape")
	if (image_data["Oval Face"] > 0):
		graph.add((face_iri, hasShape, rdflib.term.URIRef(pfd_iri + "/" + "OvalFace")))

	if (image_data["Square Face"] > 0):
		graph.add((face_iri, hasShape, rdflib.term.URIRef(pfd_iri + "/" + "SquareFace")))

	if (image_data["Round Face"] > 0):
		graph.add((face_iri, hasShape, rdflib.term.URIRef(pfd_iri + "/" + "RoundFace")))

	cheekIRI = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Cheek")
	graph.add((cheekIRI, RDF.type, OWL.NamedIndividual))
	graph.add((face_iri, hasPart, cheekIRI))
	graph.add((cheekIRI, RDF.type, rdflib.term.URIRef("http://purl.obolibrary.org/obo/UBERON_0001567")))

	if (image_data["Rosy Cheeks"] > 0):
		graph.add((cheekIRI, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "RosyCheek")))

	if (image_data["High Cheekbones"] > 0):
		graph.add((cheekIRI, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "HighCheekbone")))

	noseIRI = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Nose")
	graph.add((noseIRI, RDF.type, OWL.NamedIndividual))
	graph.add((face_iri, hasPart, noseIRI))
	graph.add((noseIRI, RDF.type, rdflib.term.URIRef("http://purl.obolibrary.org/obo/UBERON_0000004")))

	if (image_data["Big Nose"] > 0):
		graph.add((noseIRI, rdflib.term.URIRef(pfd_iri + "/" + "hasSize"), rdflib.term.URIRef(pfd_iri + "/" + "Large")))
	else:
		graph.add((noseIRI, rdflib.term.URIRef(pfd_iri + "/" + "hasSize"), rdflib.term.URIRef(pfd_iri + "/" + "Medium")))

	if (image_data["Pointy Nose"] > 0):
		graph.add((noseIRI, rdflib.term.URIRef(pfd_iri + "/" + "hasShape"), rdflib.term.URIRef(pfd_iri + "/" + "PointyNoise")))
	else:
		noseShape = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "NoseShape")
		graph.add((noseShape, RDF.type, OWL.NamedIndividual))
		graph.add((noseShape, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "NoseShape")))
		graph.add((noseIRI, rdflib.term.URIRef(pfd_iri + "/" + "hasShape"), noseShape))


	mouthIRI = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Mouth")
	graph.add((mouthIRI, RDF.type, OWL.NamedIndividual))
	graph.add((face_iri, hasPart, mouthIRI))
	graph.add((mouthIRI, RDF.type, rdflib.term.URIRef("http://purl.obolibrary.org/obo/UBERON_0000165")))

	if (image_data["Big Lips"] > 0):
		graph.add((mouthIRI, rdflib.term.URIRef(pfd_iri + "/" + "hasSize"), rdflib.term.URIRef(pfd_iri + "/" + "Large")))
	else:
		graph.add((mouthIRI, rdflib.term.URIRef(pfd_iri + "/" + "hasSize"), rdflib.term.URIRef(pfd_iri + "/" + "Medium")))

	graph.add((mouthIRI, rdflib.term.URIRef(pfd_iri + "/" + "teethVisable"), rdflib.term.Literal(not (image_data["Teeth Not Visible"] > 0), datatype=XSD.boolean)))

	if (image_data["Mouth Wide Open"] > 0):
		graph.add((mouthIRI, hasVisualFeature, rdflib.term.URIRef(pfd_iri + "/" + "MouthWideOpen")))
	else:
		if(image_data["Mouth Slightly Open"] > 0):
			graph.add((mouthIRI, hasVisualFeature, rdflib.term.URIRef(pfd_iri + "/" + "MouthSlightlyOpen")))
		else:
			graph.add((mouthIRI, hasVisualFeature, rdflib.term.URIRef(pfd_iri + "/" + "MouthClosed")))



	eyeIRI = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Eye")
	graph.add((eyeIRI, RDF.type, OWL.NamedIndividual))
	graph.add((face_iri, hasPart, eyeIRI))
	graph.add((eyeIRI, RDF.type, rdflib.term.URIRef("http://purl.obolibrary.org/obo/UBERON_0000970")))

	graph.add((eyeIRI, rdflib.term.URIRef(pfd_iri + "/" + "isOpen"), rdflib.term.Literal(not (image_data["Eyes Open"] > 0), datatype=XSD.boolean)))
	graph.add((eyeIRI, rdflib.term.URIRef(pfd_iri + "/" + "isBaggy"), rdflib.term.Literal(not (image_data["Bags Under Eyes"] > 0), datatype=XSD.boolean)))

	if (image_data["Brown Eyes"] > 0):
		graph.add((eyeIRI, rdflib.term.URIRef(pfd_iri + "/" + "hasColor"), rdflib.term.URIRef(pfd_iri + "/" + "Brown")))
	else:
		eyeColorIri = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Eye/Color")
		graph.add((eyeColorIri, RDF.type, OWL.NamedIndividual))
		graph.add((eyeColorIri, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "EyeColor")))
		graph.add((eyeIRI, rdflib.term.URIRef(pfd_iri + "/" + "hasColor"), eyeColorIri))


	skinIRI = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Skin")
	graph.add((skinIRI, RDF.type, OWL.NamedIndividual))
	graph.add((face_iri, hasPart, skinIRI))
	graph.add((skinIRI, RDF.type, rdflib.term.URIRef("http://purl.obolibrary.org/obo/UBERON_1000021")))


	if (image_data["Shiny Skin"] > 0):
		graph.add((skinIRI, hasVisualFeature, rdflib.term.URIRef(pfd_iri + "/" + "Shiny")))
	else:
		skinFinish = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Skin/Finish")
		graph.add((skinFinish, RDF.type, OWL.NamedIndividual))
		graph.add((skinFinish, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "Finish")))
		graph.add((skinIRI, hasVisualFeature, skinFinish))


	if (image_data["Pale Skin"] > 0):
		graph.add((skinIRI, hasVisualFeature, rdflib.term.URIRef(pfd_iri + "/" + "Pale")))
	else:
		if (image_data["Flushed Face"] > 0):
			graph.add((skinIRI, hasVisualFeature, rdflib.term.URIRef(pfd_iri + "/" + "Flushed")))
		else:
			skinTone = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Skin/Tone")
			graph.add((skinTone, RDF.type, OWL.NamedIndividual))
			graph.add((skinTone, RDF.type, rdflib.term.URIRef(pfd_iri + "/" + "Tone")))
			graph.add((skinIRI, hasVisualFeature, skinTone))

	frma_iri = "https://tw.rpi.edu/web/Courses/Ontologies/2018/FRMA/FRMA"
	if ((image_data["Fully Visible Forehead"] > 0) or (image_data["Partially Visible Forehead"] > 0)):
		occlusionIRI = rdflib.term.URIRef(base_iri + "Image/" + person_id + "/"+str(image_data["imagenum"]) + "/Person/" + "Occlusion")
		graph.add((occlusionIRI, RDF.type, OWL.NamedIndividual))
		graph.add((occlusionIRI, RDF.type, rdflib.term.URIRef(frma_iri + "/" + "FrontalOcclusion")))
		graph.add((person_iri, rdflib.term.URIRef(frma_iri + "/" + "hasOcculsion"), occlusionIRI))

def clean_up_xml_string(xml):
	classes = xml.split("\n  <owl")
	return "\n\n\n  <owl".join(classes)

def find_mugshot_photos(check_for, names, tags):
	# these two variables let us find what requirement is the limiting factor so we can remove it
	num_errors_to_include = 1 # if there are this many errors keep track of the errors so we can use that info to remove the
	# limiting requirement and get more photos
	most_frequent_errors = {} # so that we can find the best requirement to remove to find more photos

	found_images = []
	num_unlabeled = 0
	for name in names:
		images = tags[name]
		for image in images:
			if len(image) == 0:
				continue # some of the images don't have any labels.
			valid = True
			invalid_characteristics = []
			for a in check_for.split("\t"):
				a = a.strip()
				# this was to prevent key errors but really we're fine with them since we'll have to correct them anyways:
				# if (a not in image) and (a[1:] not in image):
				# 	print(a, "not in image for person", name, image)
				# 	break # check the next word

				if a[0] == "!":
					# if it's a yes (i.e. the confidence > 0) then continue
					if image[a[1:]] > 0: # exclude the !
						invalid_characteristics += [a] # you don't want it to be true
				elif image[a] <= 0:
					# otherwise you want it to be true
					# if the confidence is <= 0 then it's false, so then it's incorrect
					invalid_characteristics += [a]
			if len(invalid_characteristics) == 0:
				# it made it through the gauntlet so it's a valid image that fits the criteria
				# add it to our list of images
				image_name = image["person"]
				image_num = image["imagenum"]
				found_images += [(image_name, image_num)]
			if len(invalid_characteristics) <= num_errors_to_include:
				for a in invalid_characteristics:
					if a not in most_frequent_errors:
						most_frequent_errors[a] = 1
					else:
						most_frequent_errors[a] += 1
	# clean up the most frequent errors now:
	errors = [(most_frequent_errors[a], a) for a in most_frequent_errors]
	errors.sort()
	errors.reverse()
	return found_images, errors

def copy_image_files(images, new_path):
	# this is for finding specific photos like the mugshot photos
	for image in images:
		underscore_name = image[0].replace(" ", "_")
		image_file = underscore_name + "/" + underscore_name + "_" + "%04d" % (image[1],) + ".jpg"
		new_folder_path = os.path.dirname(new_path)
		if not os.path.exists(new_folder_path):
			os.mkdir(new_folder_path)
		shutil.copy("lfw_images/" + image_file, new_folder_path)


if __name__ == "__main__":
	"""this loads the attributes file that has the data for all the photos"""
	tags, names = 1, 2 #load_attributes_file()
	tags, names = load_attributes_file()

	"""this prints out the names of all the people in the ontology and allows you to query the names and images to get the data"""
	# print("\n",names,"\n")
	# basic_text_query(tags, names)
	# print(tags[names[0]][0])


	"""This chunk of code finds images that satisfy these requirements. If there's an ! in front of the name then it has to be
	false, otherwise it has to be true. If it's not listed then it doesn't care what it is. It copys those images into another
	folder called "found folder", and prints them out, along with the attributes that most often caused the image to fail if it was
	close to succeeding"""
	# requirements = """No Eyewear	!Eyeglasses	!Sunglasses	!Blurry	!Soft Lighting	!Outdoor
	# Eyes Open	Posed Photo	!Heavy Makeup	!Wearing Lipstick
	# !Wearing Earrings	!Wearing Necklace"""
	# found_images, most_frequent_errors = find_mugshot_photos(requirements, names, tags)
	# copy_image_files(found_images, "found_images/")
	# print(found_images)
	# print(most_frequent_errors)


	"""Run this to generate the individuals.rdf file for our ontology"""
	restricted_images_all = [('Aaron Pena', 1), ('Abdel Nasser Assidi', 1), ('Abdullah Ahmad Badawi', 1), ('Abdullah Gul', 12), ('Abdullah Gul', 13), ('Adam Rich', 1), ('Adolfo Rodriguez Saa', 1), ('Adrien Brody', 4), ('Agnelo Queiroz', 1), ('Akbar Hashemi Rafsanjani', 1), ('Alan Zemaitis', 1), ('Aleksander Kwasniewski', 4), ('Alexander Rumyantsev', 2), ('Al Gore', 3), ('Ali Abbas', 2), ('Alimzhan Tokhtakhounov', 2), ('Andre Agassi', 35), ('Andrew Bernard', 1), ('Andy Graves', 1), ('Anjum Hussain', 1), ('Antonio Trillanes', 1), ('Ariel Sharon', 1), ('Ariel Sharon', 25), ('Ariel Sharon', 74), ('Arminio Fraga', 4), ('Arminio Fraga', 6), ('Arnaud Lagardere', 1), ('Arnold Schwarzenegger', 14), ('Arnold Schwarzenegger', 33), ('Art Hoffmann', 2), ('Asa Hutchinson', 2), ('Ashraf Alasmar', 1), ('Augustin Calleri', 1), ('Barry Williams', 1), ('Barzan al-Tikriti', 1), ('Benazir Bhutto', 2), ('Ben Howland', 1), ('Benjamin McKenzie', 1), ('Bill Belichick', 2), ('Bill Clinton', 8), ('Bill Clinton', 13), ('Bill Clinton', 19), ('Bill McBride', 3), ('Bill Paxton', 4), ('Bill Pryor', 1), ('Bill Sizemore', 1), ('Billy Beane', 1), ('Billy Crystal', 5), ('Billy Sollie', 1), ('Bob Dole', 2), ('Bob Goldman', 1), ('Bob Hope', 7), ('Bob Hope', 8), ('Bob Petrino', 1), ('Brandon Webb', 1), ('Brian Campbell', 1), ('Brian De Palma', 1), ('Brian Griese', 1), ('Brian Kerr', 1), ('Brock Berlin', 1), ('Carlo Azeglio Ciampi', 1), ('Carlos Ghosn', 1), ('Carson Daly', 1), ('Carson Daly', 2), ('Carson Palmer', 1), ('Celso Amorim', 1), ('Chang Dae-whan', 1), ('Charles Rogers', 1), ('Charles Taylor', 1), ('Charles Taylor', 3), ('Charlotte Rampling', 1), ('Chawki Armali', 1), ('Chhouk Rin', 1), ('Chris Cornell', 1), ('Chris Matthews', 1), ('Chris Noth', 1), ('Christian Longo', 2), ('Christian Wulff', 1), ('Christopher Whittle', 1), ('Chung Mong-joon', 1), ('Chyung Dai-chul', 1), ('Clay Aiken', 5), ('Colin Farrell', 3), ('Colin Farrell', 5), ('Craig Morgan', 1), ('Crispin Glover', 1), ('Dalia Rabin-Pelosoff', 1), ('Damon Dash', 1), ('Daniel Barenboim', 1), ('Daniel Ortega', 1), ('Dariusz Michalczewski', 1), ('David Ballantyne', 1), ('David Beckham', 6), ('David Caruso', 1), ('David Heymann', 1), ('David Heymann', 3), ('David Hilt', 1), ('David Hyde Pierce', 4), ('David Scott Morris', 1), ('David Siegel', 1), ('Demetrin Veal', 1), ('Dennis Erickson', 2), ('Dennis Kozlowski', 2), ('Dennis Kucinich', 3), ('Dennis Kucinich', 7), ('Dennis Miller', 1), ('Derek Abney', 1), ('Derek Jeter', 4), ('Derrick Battie', 1), ('Dominique de Villepin', 2), ('Dominique de Villepin', 10), ('Douglas Gansler', 1), ('Doug Melvin', 1), ('Dwayne Williams', 1), ('E Clay Shaw', 1), ('Eduard Shevardnadze', 4), ('Eduard Shevardnadze', 5), ('Ekke Hard Forberg', 1), ('Elgin Baylor', 1), ('Elvis Presley', 1), ('Emmit Smith', 1), ('Eric Robert Rudolph', 3), ('Eric Shinseki', 1), ('Erin Runnion', 2), ('Erin Runnion', 3), ('Ethan Hawke', 4), ('Felix Doh', 1), ('Felix Sanchez', 1), ('Fernando Henrique Cardoso', 4), ('Franco Dragone', 2), ('Frank Hilldrup', 1), ('Frank Lautenberg', 1), ('Frank Stallone', 1), ('Fred Thompson', 2), ('Gary Gitnick', 1), ('Gary Winnick', 1), ('Geoffrey Rush', 1), ('George Lucas', 1), ('George Papandreou', 3), ('George Papandreou', 4), ('George P Bush', 2), ('George Robertson', 5), ('George Robertson', 11), ('George W Bush', 7), ('George W Bush', 12), ('George W Bush', 128), ('George W Bush', 141), ('George W Bush', 180), ('George W Bush', 198), ('George W Bush', 278), ('George W Bush', 314), ('George W Bush', 344), ('George W Bush', 362), ('George W Bush', 455), ('George W Bush', 471), ('George W Bush', 495), ('Gerard Kleisterlee', 1), ('Gerhard Schroeder', 72), ('Gerhard Schroeder', 81), ('Gerhard Schroeder', 84), ('Gerhard Schroeder', 102), ('Gloria Macapagal Arroyo', 3), ('Gloria Macapagal Arroyo', 18), ('Gloria Macapagal Arroyo', 34), ('Gordon Lightfoot', 1), ('Graciano Rocchigiani', 1), ('Gray Davis', 8), ('Gray Davis', 16), ('Gray Davis', 24), ('Greg Frers', 1), ('Greg Hennigar', 1), ('Gregorio Rosal', 1), ('Gus Van Sant', 1), ('Gwyneth Paltrow', 1), ('Hamid Karzai', 12), ('Hamid Karzai', 15), ('Hamid Karzai', 16), ('Hank McKinnell', 1), ('Harrison Ford', 10), ('Harry Belafonte', 2), ('Heather Chinnock', 1), ('Heath Ledger', 1), ('Hector Mitelman', 1), ('Heinz Feldmann', 3), ('Heizo Takenaka', 4), ('Heizo Takenaka', 5), ('Henri Proglio', 1), ('Hermando Harton', 1), ('Hilmi Ozkok', 2), ('Hisham Halawi', 1), ('Horace Newcomb', 1), ('Howard Dean', 1), ('Howard Dean', 10), ('Hrithik Roshan', 1), ('Hugh Grant', 2), ('Hugh Grant', 3), ('Hugo Chavez', 25), ('Hugo Chavez', 57), ('Hugo Chavez', 59), ('Hu Jintao', 6), ('Hu Jintao', 12), ('Iain Richmond', 1), ('Ian Thorpe', 7), ('Ibrahim Al-Marashi', 1), ('Igor Ivanov', 20), ('Islam Karimov', 1), ('Jackie Chan', 4), ('Jackie Chan', 6), ('Jackie Sherrill', 1), ('Jacques Chirac', 9), ('Jacques Chirac', 44), ('Jacques Rogge', 4), ('Jake Gyllenhaal', 1), ('James Baker', 1), ('James Brazelton', 1), ('James Cameron', 3), ('James Cunningham', 1), ('James Franco', 1), ('James Hughes', 1), ('James Kelly', 11), ('James McGreevey', 3), ('Jamie Villafane', 1), ('Jan Ullrich', 1), ('Jaromir Jagr', 1), ('Jason Bentley', 1), ('Jason Kidd', 4), ('Jason Priestley', 1), ('Javier Bardem', 1), ('Javier Solana', 8), ('Jean Charest', 3), ('Jean Chretien', 39), ('Jean-David Levitte', 7), ('Jean-Marc Olive', 1), ('Jeff Dederian', 1), ('Jeremy Fogel', 1), ('Jeremy Greenstock', 3), ('Jeremy Greenstock', 6), ('Jeremy Greenstock', 7), ('Jerry Seinfeld', 1), ('Jesse Jackson', 9), ('Jesse Ventura', 1), ('Jim Doyle', 1), ('Jim Hahn', 2), ('Jim Hahn', 3), ('Joanne Duquette', 1), ('Job Cohen', 1), ('Joe Calzaghe', 1), ('Joe Darrell', 1), ('Joe Lieberman', 9), ('Joerg Haider', 2), ('John Ashcroft', 4), ('John Ashcroft', 49), ('John Ashcroft', 51), ('John Burnett', 1), ('John Edwards', 4), ('John Edwards', 5), ('John Kerry', 2), ('John Leguizamo', 1), ('John Malkovich', 2), ('John Mayer', 1), ('John Mayer', 2), ('John McCain', 2), ('John Negroponte', 7), ('John Negroponte', 10), ('John Negroponte', 12), ('John Negroponte', 14), ('John Negroponte', 16), ('Johnny Tapia', 2), ('John Philip Elkann', 1), ('John Reilly', 2), ('John Rosa', 2), ('John Snow', 3), ('John Snow', 11), ('John Snow', 15), ('John Stockton', 4), ('Jon Gruden', 5), ('Jon Gruden', 7), ('Jon Stewart', 1), ('Jon Voight', 2), ('Jorge Valdano', 1), ('Joschka Fischer', 1), ('Joschka Fischer', 2), ('Jose Genoino', 1), ('Jose Maria Aznar', 1), ('Joseph Estrada', 2), ('Joseph Ralston', 1), ('Josh Evans', 1), ('Juan Antonio Samaranch', 1), ('Juan Carlos Ortega', 1), ('Juan Jose Lucas', 1), ('Judd Davies', 1), ('Juergen Trittin', 1), ('Julian Battle', 1), ('Junichiro Koizumi', 1), ('Junichiro Koizumi', 3), ('Junichiro Koizumi', 8), ('Junichiro Koizumi', 35), ('Junichiro Koizumi', 50), ('Kamal Kharrazi', 1), ('Katie Smith', 1), ('Keith Fotta', 1), ('Keith Snyder', 1), ('Kelsey Grammer', 1), ('Ken Balk', 1), ('Kevin Costner', 8), ('Kevin James', 1), ('Kevin Nealon', 1), ('Kevin Spacey', 2), ('Kevin Spacey', 3), ('Kevin Spacey', 4), ('Kevin Spacey', 5), ('Kim Ryong-sung', 5), ('Kim Ryong-sung', 8), ('King Abdullah II', 3), ('Kirk Douglas', 1), ('Kobe Bryant', 3), ('Kofi Annan', 4), ('Kofi Annan', 20), ('Lance Armstrong', 4), ('Lance Armstrong', 7), ('Lance Armstrong', 18), ('Lance Bass', 5), ('Lane Odom', 1), ('Lars Von Trier', 1), ('Lawrence Di Rita', 1), ('Lennox Lewis', 2), ('Lenny Wilkens', 3), ('Leonardo DiCaprio', 1), ('Leonardo DiCaprio', 6), ('Leonardo DiCaprio', 8), ('Leonardo DiCaprio', 9), ('Lewis Booth', 1), ('Lincoln Chafee', 1), ('Luis Ernesto Derbez Bautista', 2), ('Luis Guzman', 1), ('Luiz Inacio Lula da Silva', 5), ('Luiz Inacio Lula da Silva', 8), ('Luiz Inacio Lula da Silva', 11), ('Luiz Inacio Lula da Silva', 23), ('Luiz Inacio Lula da Silva', 29), ('Lyle Lovett', 1), ('Mack Brown', 1), ('Marc-Andre Fleury', 1), ('Marco Archer Cardoso Moreira', 1), ('Marco Irizarry', 1), ('Mario Jardel', 1), ('Mark Broxmeyer', 1), ('Mark Gottfried', 1), ('Mark Hogan', 1), ('Mark Kelly', 1), ('Mark Komara', 1), ('Mark Schweiker', 2), ('Marquier Montano Contreras', 1), ('Martin Bandier', 1), ('Martin Brodeur', 1), ('Massoud Barzani', 1), ('Matt Damon', 1), ('Matt Damon', 4), ('Matthew Broderick', 4), ('Matthew Perry', 1), ('Matthew Perry', 4), ('Matt Walters', 1), ('Mekhi Phifer', 1), ('Mel Brooks', 1), ('Michael Bloomberg', 7), ('Michael Bloomberg', 17), ('Michael Capellas', 1), ('Michael Douglas', 4), ('Michael Fitzgerald', 1), ('Michael Guiler', 1), ('Michael Jordan', 3), ('Michael Kirby', 1), ('Michael Kostelnik', 1), ('Michael Leavitt', 2), ('Michael Milton', 1), ('Michael Powell', 4), ('Michael Schumacher', 12), ('Michael Weiss', 1), ('Michael Winterbottom', 2), ('Michel Charles Chretien', 1), ('Mika Hakkinen', 1), ('Mike Eskew', 1), ('Mike Helton', 1), ('Mike Matheny', 1), ('Mike Myers', 3), ('Mike Myers', 5), ('Milt Palacio', 1), ('Mireille Jospin-Dandieu', 1), ('Mitar Rasevic', 1), ('Mitt Romney', 1), ('Mohamed ElBaradei', 3), ('Mohammad Aktar', 1), ('Momir Nikolic', 1), ('Nanni Moretti', 2), ('Nate Hybl', 1), ('Nathan Smith', 1), ('Nestor Kirchner', 26), ('Nick Nolte', 5), ('Nicolas Cage', 1), ('Nicolas Cage', 4), ('Nicolas Eyzaguirre', 1), ('Noor Mohammed', 1), ('OJ Simpson', 1), ('Omar Khan Sharif', 1), ('Oscar De La Hoya', 6), ('Oscar DLeon', 1), ('Owen Nolan', 1), ('Patrice Chereau', 2), ('Patrick Bourrat', 1), ('Paul Bremer', 8), ('Paul Burrell', 11), ('Paul Crake', 1), ('Paul Martin', 3), ('Paul McCartney', 2), ('Paul William Hurley', 2), ('Pedro Almodovar', 1), ('Pedro Solbes', 3), ('Pedro Solbes', 4), ('Peter Costello', 1), ('Peter Fitzgerald', 1), ('Peter Fonda', 1), ('Peter Gilmour', 1), ('Peter Greenaway', 2), ('Peter Holmberg', 1), ('Pete Sampras', 18), ('Philip Cummings', 1), ('Pierce Brosnan', 1), ('Pierce Brosnan', 4), ('Pierce Brosnan', 7), ('Pierre Van Hooijdonk', 1), ('Pio Laghi', 1), ('Placido Domingo', 2), ('Platon Lebedev', 1), ('Pupi Avati', 2), ('Qian Qichen', 1), ('Qusai Hussein', 1), ('Rachel Corrie', 1), ('Rafael Ramirez', 1), ('Ralph Firman', 2), ('Randy Travis', 1), ('Raul Cubas', 1), ('Ray Allen', 3), ('Ray Lucas', 1), ('Ray Nagin', 2), ('Ray Romano', 5), ('Ray Sherman', 1), ('Raza Rabbani', 1), ('Recep Tayyip Erdogan', 2), ('Recep Tayyip Erdogan', 24), ('Rhett Warrener', 1), ('Ricardo Lagos', 12), ('Ricardo Sanchez', 6), ('Richard Armitage', 9), ('Richard Gere', 8), ('Richard Hellfant', 1), ('Richard Myers', 4), ('Richard Myers', 9), ('Richard Myers', 12), ('Richard Myers', 17), ('Richard Myers', 18), ('Rich Brooks', 1), ('Rick Santorum', 1), ('Rick Santorum', 2), ('Ricky Martin', 2), ('Robbie Coltrane', 1), ('Robbie Williams', 3), ('Robert Bonner', 2), ('Robert Bonner', 3), ('Robert Duvall', 4), ('Roberto Cavalli', 1), ('Robert Torricelli', 2), ('Robin Cook', 2), ('Rob Marshall', 3), ('Rob Niedermayer', 1), ('Rod Blagojevich', 2), ('Roh Moo-hyun', 8), ('Roh Moo-hyun', 23), ('Rolandas Paksas', 1), ('Ronaldo Luis Nazario de Lima', 4), ('Roy Moore', 1), ('Rubens Barrichello', 10), ('Rudolf Schuster', 1), ('Rudolph Giuliani', 26), ('Rupert Grint', 1), ('Rupert Grint', 2), ('Saburo Kawabuchi', 2), ('Saddam Hussein', 6), ('Saied Hadi al Mudarissi', 1), ('Scott Blum', 1), ('Sean Combs', 1), ('Sean Hayes', 1), ('Sedigh Barmak', 1), ('Sepp Blatter', 4), ('Serena Williams', 36), ('Sergei Yastrzhembsky', 1), ('Sergey Lavrov', 9), ('Sergio Castellitto', 1), ('Sergio Vieira De Mello', 10), ('Shaul Mofaz', 3), ('Sherry Irving', 1), ('Shi Guangsheng', 1), ('Silvio Berlusconi', 11), ('Silvio Berlusconi', 23), ('Simon Cowell', 2), ('Solomon Passy', 1), ('Spencer Abraham', 1), ('Spencer Abraham', 4), ('Spike Jonze', 1), ('Stefaan Declerk', 1), ('Stephen Cooper', 1), ('Steve Avery', 1), ('Steve Blake', 1), ('Steve Case', 1), ('Steve Lavin', 2), ('Steve Lavin', 3), ('Steve Lavin', 4), ('Steve Valentine', 1), ('Sue Johnston', 1), ('Susilo Bambang Yudhoyono', 3), ('Syed Ibrahim', 1), ('Sylvester Stallone', 9), ('Taha Yassin Ramadan', 7), ('Taha Yassin Ramadan', 9), ('Tavis Smiley', 1), ('Ted Nolan', 1), ('Terence Newman', 1), ('Thaksin Shinawatra', 5), ('Thomas Fargo', 3), ('Thomas Franklin', 1), ('Thomas Malchow', 2), ('Thomas OBrien', 1), ('Thomas OBrien', 3), ('Thomas Rupprath', 2), ('Thomas Wyman', 1), ('Tiger Woods', 13), ('Timothy McVeigh', 1), ('Tim Pawlenty', 1), ('Todd Haynes', 3), ('Tom Cruise', 1), ('Tom Cruise', 7), ('Tom Daschle', 3), ('Tom Daschle', 7), ('Tom Daschle', 8), ('Tom Daschle', 10), ('Tom Hanks', 5), ('Tom Hanks', 9), ('Tommy Franks', 3), ('Tommy Franks', 5), ('Tommy Franks', 8), ('Tom OBrien', 1), ('Tom Osborne', 1), ('Tom Ridge', 2), ('Tom Ridge', 4), ('Tom Ridge', 8), ('Tom Ridge', 11), ('Tom Ridge', 23), ('Tonino Guerra', 1), ('Tony Blair', 31), ('Tony Blair', 32), ('Tony Blair', 33), ('Tony Blair', 34), ('Tony Blair', 41), ('Tony Blair', 43), ('Tony Blair', 45), ('Tony Blair', 61), ('Tony Blair', 85), ('Tony Blair', 115), ('Tony Blair', 122), ('Tony Blair', 129), ('Tony Blair', 131), ('Tony LaRussa', 1), ('Tony Shalhoub', 4), ('Tony Stewart', 1), ('Tony Stewart', 2), ('Toshihiko Fukui', 2), ('Tung Chee-hwa', 5), ('Tyler Hamilton', 2), ('Vaclav Havel', 2), ('Valdas Adamkus', 1), ('Valentino Rossi', 3), ('Valery Giscard dEstaing', 5), ('Vicente Fox', 1), ('Vicente Fox', 23), ('Victor Garber', 1), ('Vladimir Golovlyov', 1), ('Vladimir Putin', 36), ('Warren Beatty', 2), ('Wayne Brady', 1), ('William Bratton', 1), ('William Delahunt', 1), ('William Murabito', 1), ('William Rehnquist', 2), ('Wolfgang Clement', 1), ('Yang Jianli', 1), ('Yann Martel', 2), ('Yoelbi Quesada', 1), ('Yoshiyuki Kamei', 1), ('Yves Brodeur', 1), ('Zafarullah Khan Jamali', 2), ('Zhang Ziyi', 1), ('Zico', 2), ('Zurab Tsereteli', 1)]
	restricted_images = []
	for i in range(len(restricted_images_all)):
		if i % int(len(restricted_images_all)/4) == 0:
			restricted_images.append(restricted_images_all[i])
	print(len(restricted_images))
	# generate_rdf_individuals(names, tags, "../Individuals.rdf", "individuals.rdf", restricted_images)

	# restricted_single = [('Patrick Bourrat', 1)]
	restricted_single = [('Bill Clinton', 19), ('Billy Crystal', 5), ('Colin Farrell', 3), ('Derek Jeter', 4), ('Harry Belafonte', 2), ('Arnold Schwarzenegger', 1), ('Benjamin Franklin', 1), ('Bill Gates', 3), ('Bill OReilly', 1), ('Bill Paxton', 3), ('Al Gore', 8), ('Alexis Bledel', 1), ('Angelina Jolie', 1), ('Antonio Banderas', 2), ('Johnny Depp', 1), ('Johnny Depp', 2), ('Aaron Eckhart', 1), ('Adam Sandler', 1), ('Alanis Morissette', 1), ('Alec Baldwin', 1)]
	generate_rdf_individuals(names, tags, "../FaceNet_Individual.rdf", "individuals.rdf", True, restricted_single)




	# run this if you want to output a text file to "labeled_attributes.txt" that has all of the labels nicely formatted for all the photos
	# that have them
	# output_labeled_everything(tags, names, "labeled_attributes.txt")




"""
Filipe Perez Roque image 4:

Male  :  True
Asian  :  False
White  :  True
Black  :  False
Baby  :  False
Child  :  False
Youth  :  False
Middle Aged  :  False
Senior  :  False
Black Hair  :  False
Blond Hair  :  False
Brown Hair  :  True
Bald  :  False
No Eyewear  :  True
Eyeglasses  :  False
Sunglasses  :  False
Mustache  :  False
Smiling  :  False
Frowning  :  True
Chubby  :  False
Blurry  :  False
Harsh Lighting  :  False
Flash  :  False
Soft Lighting  :  False
Outdoor  :  True
Curly Hair  :  True
Wavy Hair  :  False
Straight Hair  :  False
Receding Hairline  :  False
Bangs  :  False
Sideburns  :  True
Fully Visible Forehead  :  True
Partially Visible Forehead  :  False
Obstructed Forehead  :  False
Bushy Eyebrows  :  True
Arched Eyebrows  :  False
Narrow Eyes  :  True
Eyes Open  :  True
Big Nose  :  True
Pointy Nose  :  True
Big Lips  :  True
Mouth Closed  :  False
Mouth Slightly Open  :  True
Mouth Wide Open  :  False
Teeth Not Visible  :  True
No Beard  :  True
Goatee  :  False
Round Jaw  :  True
Double Chin  :  False
Wearing Hat  :  False
Oval Face  :  False
Square Face  :  False
Round Face  :  False
Color Photo  :  True
Posed Photo  :  True
Attractive Man  :  False
Attractive Woman  :  False
Indian  :  False
Gray Hair  :  False
Bags Under Eyes  :  False
Heavy Makeup  :  False
Rosy Cheeks  :  False
Shiny Skin  :  False
Pale Skin  :  False
5 o' Clock Shadow  :  True
Strong Nose-Mouth Lines  :  False
Wearing Lipstick  :  False
Flushed Face  :  False
High Cheekbones  :  False
Brown Eyes  :  True
Wearing Earrings  :  False
Wearing Necktie  :  True
Wearing Necklace  :  False


Gary Doer image 1:

Male  :  True
Asian  :  False
White  :  True
Black  :  False
Baby  :  False
Child  :  False
Youth  :  False
Middle Aged  :  False
Senior  :  False
Black Hair  :  False
Blond Hair  :  False
Brown Hair  :  True
Bald  :  True
No Eyewear  :  False
Eyeglasses  :  False
Sunglasses  :  False
Mustache  :  False
Smiling  :  True
Frowning  :  False
Chubby  :  False
Blurry  :  True
Harsh Lighting  :  False
Flash  :  False
Soft Lighting  :  True
Outdoor  :  True
Curly Hair  :  True
Wavy Hair  :  True
Straight Hair  :  False
Receding Hairline  :  True
Bangs  :  False
Sideburns  :  True
Fully Visible Forehead  :  True
Partially Visible Forehead  :  True
Obstructed Forehead  :  False
Bushy Eyebrows  :  True
Arched Eyebrows  :  False
Narrow Eyes  :  False
Eyes Open  :  False
Big Nose  :  False
Pointy Nose  :  True
Big Lips  :  True
Mouth Closed  :  True
Mouth Slightly Open  :  False
Mouth Wide Open  :  False
Teeth Not Visible  :  True
No Beard  :  True
Goatee  :  False
Round Jaw  :  True
Double Chin  :  False
Wearing Hat  :  False
Oval Face  :  True
Square Face  :  False
Round Face  :  False
Color Photo  :  True
Posed Photo  :  False
Attractive Man  :  False
Attractive Woman  :  False
Indian  :  False
Gray Hair  :  False
Bags Under Eyes  :  True
Heavy Makeup  :  False
Rosy Cheeks  :  True
Shiny Skin  :  False
Pale Skin  :  False
5 o' Clock Shadow  :  False
Strong Nose-Mouth Lines  :  False
Wearing Lipstick  :  False
Flushed Face  :  False
High Cheekbones  :  False
Brown Eyes  :  False
Wearing Earrings  :  False
Wearing Necktie  :  False
Wearing Necklace  :  False
"""
