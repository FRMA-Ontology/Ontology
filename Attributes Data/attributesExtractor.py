attributeLabels = """person	imagenum	Male	Asian	White	Black	Baby	Child	Youth	Middle Aged	Senior	Black Hair	Blond Hair	Brown Hair	Bald	No Eyewear	Eyeglasses	Sunglasses	Mustache	Smiling	Frowning	Chubby	Blurry	Harsh Lighting	Flash	Soft Lighting	Outdoor	Curly Hair	Wavy Hair	Straight Hair	Receding Hairline	Bangs	Sideburns	Fully Visible Forehead	Partially Visible Forehead	Obstructed Forehead	Bushy Eyebrows	Arched Eyebrows	Narrow Eyes	Eyes Open	Big Nose	Pointy Nose	Big Lips	Mouth Closed	Mouth Slightly Open	Mouth Wide Open	Teeth Not Visible	No Beard	Goatee	Round Jaw	Double Chin	Wearing Hat	Oval Face	Square Face	Round Face	Color Photo	Posed Photo	Attractive Man	Attractive Woman	Indian	Gray Hair	Bags Under Eyes	Heavy Makeup	Rosy Cheeks	Shiny Skin	Pale Skin	5 o' Clock Shadow	Strong Nose-Mouth Lines	Wearing Lipstick	Flushed Face	High Cheekbones	Brown Eyes	Wearing Earrings	Wearing Necktie	Wearing Necklace"""
attributeList = attributeLabels.strip().split("\t")


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


if __name__ == "__main__":
	tags, names = load_attributes_file()
	print("\n",names,"\n")
	basic_text_query(tags, names)
	# print(tags[names[0]][0])

	# run this if you want to output a text file to "labeled_attributes.txt" that has all of the labels nicely formatted for all the photos
	# that have them
	# output_labeled_everything(tags, names, "labeled_attributes.txt")




# mugshot image: felipe perez roque, image 4
# non-mugshot image: gary doer, image 1



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