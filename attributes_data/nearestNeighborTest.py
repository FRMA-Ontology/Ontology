"""
This is a test that we're using to gather example data from our two example models.
This is passed a list of image names, image numbers, and the vector representing the face in the photo,
and this script takes that and a split of testing vs training data to determine how accurate the model was by simply
checking which labeled vector (from the train data) the test data is closest to, and returning whether that was right or not.

python nearestNeighborTest.py ../../../../Downloads/facenet_lfw_vector.txt training_split.txt testing_split.txt facenet_results.txt

"""
import sys
import numpy as np


def load_split_file(filename):
	# this loads the split files, reads them, closes them, and returns the data
	f = open(filename, "r")
	data = f.readlines()
	data = [(line.split("\t")[0], int(line.split("\t")[1])) for line in data]
	f.close()
	return data

def nearest_neighbor(vector, neighbors):
	# neighbors is a list of (name, number, vector)s
	# requires at least one neighbor
	# this could be done much, much more efficiently
	closest = neighbors[0]
	closestDistance = np.linalg.norm(vector - neighbors[0][2])
	for neighbor in neighbors:
		distance = np.linalg.norm(vector - neighbor[2])
		if distance < closestDistance:
			closestDistance = distance
			closest = neighbor
	return closest, closestDistance


def main(args):
	results_file = open(args[1], "r") # this contains the vectors describing all of the photos
	output_filename = args[4]

	# then go load all of the files
	all_vector_dict = {}
	all_results = []

	lines = results_file.readlines()
	lines = [line.split(" - ") for line in lines]
	for result in lines:
		words = result[0].split("_")
		words[-1] = words[-1].split(".")[0] # remove the file type from the number
		number = int(words[-1])
		name = "_".join(words[:-1]) # the rest of the underscore separated things before the number
		vector = np.array([float(x) for x in result[1].replace("[", "").replace("]", "").split(", ")])
		r = (name, number, vector)
		all_results += [r]
		all_vector_dict[(name, number)] = r
	results_file.close()

	# now we have the vectors. Now lets load the split

	training_names = load_split_file(args[2])
	testing_names = load_split_file(args[3])

	# now find all of the labeled images so we can loop over them all
	labeled_data = []
	for label in training_names:
		# add the vector to our list of labeled data:
		labeled_data += [all_vector_dict[label]]
	print("amount of labeled data: " + str(len(labeled_data)))

	# then go test it!
	# the output is a list of (name, number, is_result_less_than_.6, nearest_name, nearest_number, is_same_person_bool)
	# which we then output into a text file split by tabs probably.
	output_file = open(output_filename, "w")
	# write everything here!

	# if you uncomment this line then it'll generate the results for ALL images not just the testing data.
	# testing_names += training_names

	# results = []
	# I also save everything to here just in case Matt wants to just edit this code instead of loading the file I guess?
	# there are a couple lines inside the for loop which have to be uncommented to use the results array

	for testing_name in testing_names:
		# this is a name and number tuple
		testing_vector = all_vector_dict[testing_name]
		nearest, nearest_distance = nearest_neighbor(testing_vector[2], labeled_data)
		# nearest is (name, number, vector)
		r = (testing_name[0], testing_name[1], nearest_distance < .6, nearest[0], nearest[1], testing_name[0] == nearest[0])
		# results += [r]
		string_r = [str(x) for x in r]
		o = "\t".join(string_r) + "\n"
		output_file.write(o)
	output_file.close()

	# if you uncomment things you can now do stuff with results, which is a list of (name, number, is_result_less_than_.6, nearest_name, nearest_number, is_same_person_bool)
	# for each result. Currently we only test the testing_files, you can also uncomment the line above the for loop which then means
	# we generate results for ALL images including training data (which should always be correct since its nearest neighbor is itself)
	# but that may be useful for adding more data to the ontology, we'll figure it up later

if __name__ == "__main__":
	"""this loads the attributes file that has the data for all the photos. Pass in the filename of the tab separated file downloaded
	from http://vis-www.cs.umass.edu/lfw/ with the list of all people names and the number of images associated with them"""

	if len(sys.argv) != 5:
		print(
			"""Usage: nearestNeighborTest.py  results_filename  training_filename  testing_filename  output_filename"""
			)
		sys.exit(0) # exit out


	main(sys.argv)