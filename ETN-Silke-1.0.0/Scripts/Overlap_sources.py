import csv,sys
import pandas as pd
import numpy as np

complexes = []
complex_sources = {}

if __name__ == "__main__":
	
	# Read in the file, filter on entryType, expansionModel, edgeType and organism
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
			if 'complex' in entryType and expansionModel == 'bipartite' and edgeType == 'C' and 'Homo sapiens' in taxb and 'imex' not in source:
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
	overlap_counts = {}
	# Iterate over this list of sources and make a list of unique complex ids for these sources
	for i in range(len(source_list)):
		source_i = source_list[i]
		complexes_i = set(complex_sources[source_i])
		# Iterate over the list of sources and make a list of unique complex ids for these sources 
		for j in range(i, len(source_list)):
			source_j = source_list[j]
			complexes_j = set(complex_sources[source_j])
			# Compare the complex ids of two sources and calculate this overlap
			overlap = complexes_i.intersection(complexes_j)
			overlap_count = len(overlap)
			# Make a dictionary for the overlap count between the sources
			key = f"{source_i} - {source_j}"
			overlap_counts[key] = overlap_count
	# Print the results of this comparison between the sources
	for key, count in overlap_counts.items():
		print(f"{key}: {count}")

	# Create a dictionary to store the numbers of complexes that are exclusively present in the sources seperately
	unique_counts_per_source = {}
	exclusive_ids_per_source = {}
	for source in source_list:
		complexes_source = set(complex_sources[source])
		for comparison_source in source_list:
			if comparison_source != source:
				complexes_source -= set(complex_sources[comparison_source])
		unique_counts_per_source[source] = len(complexes_source)
		exclusive_ids_per_source[source] = list(complexes_source)
		
	# Write the exclusive complex_ids for every source to a file
	with open('Exclusive_ids_per_source_Hs-noimex.csv', 'w',newline='') as csv_file:
		csvwriter = csv.writer(csv_file)
		csvwriter.writerow(exclusive_ids_per_source.keys())
		max_ids = max(len(ids) for ids in exclusive_ids_per_source.values())
		for i in range(max_ids):
			row = [exclusive_ids_per_source[source][i] if i < len(exclusive_ids_per_source[source]) else '' for source in source_list]
			csvwriter.writerow(row)
	csv_file.close()
	# Print the results of this comparison between the sources
	for source, count in unique_counts_per_source.items():
		print(f"Number of complexes that are exclusively present in {source}: {count}")

	sys.exit()
	# Transform this data into a matrix 
	matrix = [[overlap_counts.get(f"{source_i} - {source_j}", overlap_counts.get(f"{source_j} - {source_i}",0)) for source_j in source_list] for source_i in source_list]
	# Create a dataframe of the matrix and add the source labels to the matrix
	matrix_labels = pd.DataFrame(matrix,columns=source_list, index=source_list)
	# Only keep the upper part of the triangle in the matrix
	only_upper = np.triu(np.ones(matrix_labels.shape)).astype(bool)
	matrix_labels = matrix_labels.where(only_upper)
	# Replace NaN-values and infinity values with an empty string, convert the data to numeric values
	matrix_labels = matrix_labels.fillna('').replace([np.inf,-np.inf],'').apply(pd.to_numeric, errors='coerce').astype(pd.Int64Dtype()).astype(str)
	# Replace remaining <NA>-values with an empty string
	matrix_labels = matrix_labels.replace("<NA>",'')
	print(matrix_labels)
	# Write the output to a csv file
	matrix_labels.to_csv('Overlap_sources_matrix_Homo-sapiens-noimex.csv',index=True,sep='\t')
	with open('Overlap_sources_matrix_Homo-sapiens-noimex.csv',mode='a') as csv_file:
		csvwriter = csv.writer(csv_file, delimiter='\t')
		csvwriter.writerow(["Exclusive to source"] + [unique_counts_per_source[source] for source in source_list]) # Add an empty column to shift this row to the right
	csv_file.close()
	
