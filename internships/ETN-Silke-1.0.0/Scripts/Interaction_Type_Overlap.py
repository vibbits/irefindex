import csv, sys
import matplotlib.pyplot as plt
from collections import Counter

complexes = []
complex_sources = {}
overlap_complexes = []
complex_type = {}
interaction_types_list = []
type_counts = {}
type_counts_str = {}

if __name__ == "__main__":
	
	# Read in the file, filter on entrytype, expansionmodel, edgetype, organism 
	# Store the filtered data in a new variable 'complexes'
	irefIndexFile = "All.mitab.08-22-2022.txt"
	with open(irefIndexFile, 'r',encoding="utf-8") as ppiFile:
		csvreader = csv.reader(ppiFile, delimiter='\t')
		header = next(csvreader)
		counter = 0
		
		for row in csvreader:
			counter += 1
			entryType = row[0]
			taxb = row[10]
			source = row[12]
			expansionModel = row[15]
			edgeType = row[52]
			if 'complex' in entryType and expansionModel == 'bipartite' and edgeType == 'C' and 'Homo sapiens' in taxb:
				complexes.append(row)

			if counter % 100000 == 0:
				print("Processed {} lines".format(counter))
		
	# Iterate over the complexes and make a dictionary with the complex ids for every source
	for complex_row in complexes:
		complex_id = complex_row[0]
		source = complex_row[12].split('(')[1].rstrip(')')

		if source not in complex_sources:
			complex_sources[source] = []
			complex_sources[source].append(complex_id)
		else:
			complex_sources[source].append(complex_id)
	
	# Make a list with all available sources
	source_list = list(complex_sources.keys())
	print(source_list)

	# Get the overlapping complex ids between intact and corum
	complexes_intact = set(complex_sources['intact'])
	complexes_corum = set(complex_sources['corum'])
	overlap = complexes_intact.intersection(complexes_corum)
	overlap_count = len(overlap)
	print("Overlap: {}".format(overlap_count))
	print(len(set(overlap)))
	
	print('complex_ids')
	
	# Get the data for the exclusive complexes only
	row_dict = {row[0]:row for row in complexes}
	for id in overlap:
		if id in row_dict:
			overlap_complexes.append(row_dict[id])
	print('data for exclusive complexes')

	# For each complex_id, get the unique types
	for row in overlap_complexes:
		complex_id = row[0]
		interaction_type = row[11]
		if complex_id not in complex_type:
			complex_type[complex_id] = set()
			complex_type[complex_id].add(interaction_type)
		else:
			complex_type[complex_id].add(interaction_type)
	print('unique types')
	
	# For each type, count the number of occurences
	for complex_id,type in complex_type.items():
		interaction_types_list.append(type) 
	interaction_types_list = [tuple(type) for type in interaction_types_list] # Convert the sets of types to tuples
	type_counts = dict(Counter(interaction_types_list))
	print('occurences types')
	
	# Convert the type tuple into a string to get rid of the extra parentheses
	for type_tuple,count in type_counts.items():
		type_str = type_tuple[0]
		type_counts_str[type_str] = count

	# Sort the counts of unique types in descending order
	type_counts_sorted = sorted(type_counts_str.items(), key=lambda x: x[1], reverse=True)
	print('sort')

	# Store the type data in variables to plot them
	type = []
	frequencies = []
	for key,value in type_counts_sorted:
		type_terms = key.split('(')
		if len(type_terms) > 1:
			type_term = type_terms[1].rstrip(')')
			type.append(type_term)
			frequencies.append(value)

	# Function to add the labels to the bars 
	def addlabels(x,y):
		for i in range(len(x)):
			plt.text(i,y[i]+5,y[i],ha='center')

	# Plot this type data
	fig,ax = plt.subplots()
	ax.bar(type[0:10], frequencies[0:10])
	ax.set(ylim=(0,200),xlabel="Interaction type",ylabel="Number of occurences",
	title="Number of occurences of each \ninteraction type - intact & corum")
	addlabels(type[0:10],frequencies[0:10])
	plt.xticks(rotation=45, ha='right')
	plt.subplots_adjust(bottom=0.35)
	plt.show()