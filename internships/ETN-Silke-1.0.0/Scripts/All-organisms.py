# Import the necessary libraries
import csv, pickle, sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

complex_ids = []
complexes = []
taxonomies = []
tax_complex = {}

if __name__ == "__main__":
	
	# Read in the file, filter on entryType, expansionModel and edgeType
	irefIndexFile = "All.mitab.08-22-2022_1Mlines.txt"
	with open(irefIndexFile, 'r',encoding="utf-8") as ppiFile:
		csvreader = csv.reader(ppiFile, delimiter='\t')
		header = next(csvreader)
		counter = 0

		nComplexEntries = 0
		for row in csvreader:
			counter += 1 
			entryType = row[0]
			taxonomy = row[10].split('(')[1].rstrip(')')
			expansionModel = row[15]
			edgeType = row[52]
			if 'complex' in entryType and expansionModel == 'bipartite' and edgeType == 'C':
				nComplexEntries += 1 
				complexId = row[0]
				complex_ids.append(entryType)
				complexes.append(row)
				taxonomies.append(taxonomy)

			# During the execution of the script, check how the process is going
			if counter % 100000 == 0:
				print("Processed {} lines".format(counter))

	# Group the complexes based on taxids of interactors
	# One group with mixed species in the same complex and one group with the same species over all interactors of that complex
	print("After processed lines")
	complexes_df = pd.DataFrame(data=complexes,columns=header)
	same_species_complexes_data = []
	different_species_complexes_data = []
	data_grouped = complexes_df.groupby(by='#uidA')

	total_groups = len(data_grouped)
	group_counter = 0
	print("After grouping")
	for complex_id,complex_data in data_grouped:
		group_counter += 1
		if group_counter % 1000 == 0:
			print("Processed {} groups of {}".format(group_counter, total_groups))
		unique_taxids = complex_data['taxb'].unique()
		if len(unique_taxids) == 1:
			same_species_complexes_data.append(complex_data)
			
		else: 
			different_species_complexes_data.append(complex_data)
	
	same_species_complexes = pd.concat(same_species_complexes_data)
	different_species_complexes = pd.concat(different_species_complexes_data)

	print("Number of complexes with the same species",len(same_species_complexes))
	print("Before different species")
	print("Number of complexes with mixed species",len(different_species_complexes))
	print("Total number of complexes",len(same_species_complexes)+len(different_species_complexes))

	# Iterate over same_species_complexes to make a dictionary with key,value pairs for each organism
	# The keys are the unique species, the values are the complex ids
	for index, row in same_species_complexes.iterrows():
		taxonomy = row['taxb'].split('(')[1].rstrip(')')
		complex_id = row['#uidA']
		if taxonomy not in tax_complex:
			tax_complex[taxonomy] = []
			tax_complex[taxonomy].append(complex_id)
		else: 
			tax_complex[taxonomy].append(complex_id)
	print("Taxonomy")

	# Add different_species_complexes as seperate organism in tax_complex_counts and iterate over it to make the dictionary
	different_species_tax = "Mixed organisms"
	if different_species_tax not in tax_complex:
		tax_complex[different_species_tax] = []
	for index, row in different_species_complexes.iterrows():
		complex_id = row['#uidA']
		tax_complex[different_species_tax].append(complex_id)
	else: 
		tax_complex[different_species_tax].append(complex_id)
	print("Mixed complexes")

	# For each organism, count the number of unique complexes
	tax_complex_counts = {}
	for tax,complexes in tax_complex.items():
		nr_complexes = len(set(complexes))
		tax_complex_counts[tax] = nr_complexes
	print("Count")

# Sort the counts of unique complexes in descending order
	tax_complex_counts_sorted = sorted(tax_complex_counts.items(), key=lambda x: x[1], reverse=True)	
	
# Store the data in variables to plot them
	taxon = []
	frequencies = []
	for key,value in tax_complex_counts_sorted:
		taxon.append(key)
		frequencies.append(value)
	print("Store")

# Save this data to a pickle file
	data = {'taxb':taxon, 'frequencies':frequencies}
	print(data)
	with open('all_organisms_plot_data_full.pickle','wb') as output:
		pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
	print("Save")

# Read in the data to plot
	data = pickle.load(open("all_organisms_plot_data_full.pickle",'rb'))
	taxon = data['taxb']
	frequencies = data['frequencies']

# Function to add the labels (number of unique complexes) to the bars 
	def addlabels(x,y):
		for i in range(len(x)):
			plt.text(i,y[i]+5,y[i],ha='center')

# Plot this data
	fig,ax = plt.subplots()
	ax.bar(taxon[0:10], frequencies[0:10])
	ax.set(ylim=(0,2000), ylabel="Number of unique complexes",
	title="Number of unique complexes per organism")
	addlabels(taxon[0:10],frequencies[0:10])
	plt.xticks(rotation=45, ha='right')
	plt.subplots_adjust(bottom=0.35)
	plt.show()

# Heatmap 
# Count occurrences per source for each taxonomy in same_species_complexes
	tax_source_counts = {}
	for tax, tax_data in same_species_complexes.groupby('taxb'):
		source_counts = tax_data['sourcedb'].value_counts().to_dict()
		tax = tax.split('(')[1].rstrip(')')
		source_counts = {source.split('(')[1].rstrip(')'): count for source, count in source_counts.items()}
		tax_source_counts[tax] = source_counts

# Count occurrences per source for mixed species complexes
	mixed_species_counts = different_species_complexes['sourcedb'].value_counts().to_dict()
	mixed_species_counts = {source.split('(')[1].rstrip(')'):count for source, count in mixed_species_counts.items()}
	tax_source_counts['Mixed organisms'] = mixed_species_counts
# Sort the counts for each taxonomy in descending order
	tax_source_counts_sorted = sorted(tax_source_counts.items(), key=lambda x: sum(x[1].values()), reverse=True)
# Only select the top 10 taxonomies, based on counts
	top10_taxonomies = [tax for tax, count in tax_source_counts_sorted[0:10]]
# Filter out the data only from the top 10 taxonomies
	top10_tax_source_counts = {tax:counts for tax, counts in tax_source_counts_sorted if tax in top10_taxonomies}

# Convert the tax_source_counts dictionary to a DataFrame for plotting
	heatmap_data = pd.DataFrame(top10_tax_source_counts).fillna(0).astype(int)
	
# Plot the heatmap
	plt.figure(figsize=(10, 8))
	sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt="d", cbar=True)
	plt.title("Number of complexes per source per organism")
	plt.ylabel("Source")
	plt.xticks(rotation=45, ha='right')
	plt.tight_layout()
	plt.show()

# Some informational prints
	print("Number of complex ids:",nComplexEntries)
	print("Number of unique complex ids:",len(set(complex_ids)))
	print("Taxonomies in data:",len(set(taxonomies)))
	print("total nr of complexes:",sum(tax_complex_counts.values()))