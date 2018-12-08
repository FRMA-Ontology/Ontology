"""
This generates a split list of images for testing our machine learning models


"""

import random, sys



def split_images(all_images, split_ratio, minimum_images_to_keep, one_in_both):
	train_set = []
	test_set = []

	for image in all_images:
		name = image[0]
		num_images = image[1]

		if num_images < minimum_images_to_keep:
			continue # don't include these images in the sets

		image_indexes = [x+1 for x in range(num_images)]
		random.shuffle(image_indexes)

		# if we want to ensure one in both then we randomly sort the image numbers and pick two to split up
		if one_in_both:
			 if num_images < 2:
			 	# then we can't actually split them so just split them randomly and live our lives.
			 	pass
			 else:
			 	# ensure one is in both
			 	# put the first into train and the second into test, we've already randomly shuffled them so it's random
			 	train_set += [(name, image_indexes[0])]
			 	test_set += [(name, image_indexes[1])]
			 	image_indexes = image_indexes[2:]

		# then loop through splitting the rest of the images.
		for index in image_indexes:
			# choose a random set to put it based on the split ratio and a random number
			r = random.random()
			if r < split_ratio:
				train_set += [(name, index)]
			else:
				test_set += [(name, index)]

	return train_set, test_set



# def convert_to_filename(name):
# 	pass

# def convert_to_filenames(images):
# 	filename_version = []
# 	for image in images:
# 		filename_version += [(convert_to_filename(image[0]), image[1])]
# 	return filename_version

if __name__ == "__main__":
	"""this loads the attributes file that has the data for all the photos. Pass in the filename of the tab separated file downloaded
	from http://vis-www.cs.umass.edu/lfw/ with the list of all people names and the number of images associated with them"""

	if len(sys.argv) < 4 or len(sys.argv) > 7:
		print(
			"""Usage: imageSplitter.py file_with_all_image_names.txt output_training_filename output_testing_filename
[rough percentage of images in training set vs test set default = 2/3]
[required number of images per person for inclusion default = 4]
[guarantee at least one image in both sets if there are 2 or more images, default = True]"""
			)
		sys.exit(0) # exit out


	all_names_file = open(sys.argv[1], "r")
	# this then gives us a list of tuples of (name, number_of_images) for all images if you use the file from the website
	all_images = [(image.split("\t")[0], int(image.split("\t")[1])) for image in all_names_file.readlines()]

	# the files to output the data sets to
	output_train_filename = sys.argv[2]
	output_test_filename = sys.argv[3]

	# the approximate ratio of images in training vs. the testing dataset
	split_ratio = float(2)/3
	if len(sys.argv) > 4:
		split_ratio = float(sys.argv[4])

	# require the person have at least this many images if you want to include them in the dataset
	minimum_images_to_keep = 4
	if len(sys.argv) > 5:
		minimum_images_to_keep = int(sys.argv[5])

	# guarantee at least one image in both sets (assuming there's at least two images for the person)
	one_in_both = True
	if len(sys.argv) > 6:
		one_in_both = bool(sys.argv[6])

	train_images, test_images = split_images(all_images, split_ratio, minimum_images_to_keep, one_in_both)

	# train_filenames = convert_to_filenames(train_images)
	# test_filenames = convert_to_filenames(test_images)

	train_images = [image[0] + "\t" + str(image[1]) for image in train_images]
	train_out = open(output_train_filename, "w")
	train_out.write("\n".join(train_images))
	train_out.close()


	test_images = [image[0] + "\t" + str(image[1]) for image in test_images]
	test_out = open(output_test_filename, "w")
	test_out.write("\n".join(test_images))
	test_out.close()