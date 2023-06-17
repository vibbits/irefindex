# Import the necessary libraries
import csv, pickle, sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

complexes = []
tax_complex = {}

if __name__ == "__main__":
	
	# Read in the file, filter on edgeType
	irefIndexFile = "All.mitab.08-22-2022.txt"
	with open(irefIndexFile, 'r',encoding="utf-8") as ppiFile:
		csvreader = csv.reader(ppiFile, delimiter='\t')
		header = next(csvreader)
		counter = 0

		nComplexEntries = 0
		for row in csvreader:
			counter += 1 
			interactor_id = row[0]
			edgeType = row[52]
			if edgeType == 'Y':
				nComplexEntries += 1 
				interactor_id = row[0]
				complexes.append(row)
		
			# During the execution of the script, check how the process is going
			if counter % 100000 == 0:
				print("Processed {} lines".format(counter))
		print("Number of complexes",len(complexes)) # 19.908

	# Iterate over complexes dataframe to make a dictionary with key,value pairs for each organism
	# The keys are the unique species, the values are the interactor ids
	complexes_df = pd.DataFrame(data=complexes,columns=header)
	for index, row in complexes_df.iterrows():
		taxonomy = row['taxa'].split('(')[1].rstrip(')')
		interactor_id = row['#uidA']
		if taxonomy not in tax_complex:
			tax_complex[taxonomy] = []
			tax_complex[taxonomy].append(interactor_id)
		else: 
			tax_complex[taxonomy].append(interactor_id)
	print("Taxonomy")
	
	# For each organism, count the number of unique complexes
	tax_complex_counts = {}
	for tax,complexes in tax_complex.items():
		nr_complexes = len(set(complexes))
		tax_complex_counts[tax] = nr_complexes
	print("Count")
	print("Number of unique complexes:",sum(tax_complex_counts.values()))

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
	data = {'taxa':taxon, 'frequencies':frequencies}
	with open('all_organisms_plot_data_Y.pickle','wb') as output:
		pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
	print("Save")
# Read in the data to plot
	data = pickle.load(open("all_organisms_plot_data_Y.pickle",'rb'))
	taxon = data['taxa']
	frequencies = data['frequencies']

# Function to add the labels (number of unique complexes) to the bars 
	def addlabels(x,y):
		for i in range(len(x)):
			plt.text(i,y[i]+5,y[i],ha='center')

# Plot this data
	fig,ax = plt.subplots()
	ax.bar(taxon[0:10], frequencies[0:10])
	ax.set(ylim=(0,1100), ylabel="Number of unique complexes",
	title="Number of unique complexes per organism")
	addlabels(taxon[0:10],frequencies[0:10])
	plt.xticks(rotation=45, ha='right')
	plt.subplots_adjust(bottom=0.35)
	plt.show()
	
# Heatmap 
# Count occurrences per source for each taxonomy in complexes_df
	tax_source_counts = {}
	for tax, tax_data in complexes_df.groupby('taxa'):
		source_counts = tax_data['sourcedb'].value_counts().to_dict()
		tax = tax.split('(')[1].rstrip(')')
		source_counts = {source.split('(')[1].rstrip(')'): count for source, count in source_counts.items()}
		tax_source_counts[tax] = source_counts

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
	plt.title("Number of complexes per source per organism - edgetype Y")
	plt.ylabel("Source")
	plt.xticks(rotation=45, ha='right')
	plt.tight_layout()
	plt.show()

# Some informational prints
	print("Number of complex ids:",nComplexEntries)
	print("Total nr of unique complexes:",sum(tax_complex_counts.values()))