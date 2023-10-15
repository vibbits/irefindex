# This is used to look at the number of unique complexes. 
# Seems very high (22981) so find the solution for this (FilterHuman.py)
import csv, sys

complex_ids = []
complexes = []

if __name__ == "__main__":

	# Open and parse the IrefIndex Mitab file.
	# Read in the file 
	# Save the headers in a variable 'header'
	irefIndexFile = "9606.mitab.08-22-2022_10000.txt"
	with open(irefIndexFile, 'r') as ppiFile:
		csvreader = csv.reader(ppiFile, delimiter='\t')
		header = next(csvreader)

		# Read the file row per row, filter on specific columns 
		# Save complex ids and filtered out rows in variables
		nComplexEntries = 0
		for row in csvreader:
			entryType = row[0]
			expansionModel = row[15] #'bipartite' for multiprotein complexes in iRefIndex.
			edgeType = row[52] # 'C' for complexes
			taxonId_protA = row[9].split('(')[0].replace('taxid:','')
			taxonId_protB = row[10].split('(')[0].replace('taxid:','')
			if taxonId_protB == '9606':
				if "complex:" in entryType and expansionModel == 'bipartite' and edgeType == 'C':
					nComplexEntries += 1
					complexId = row[0]
					proteinSubunitA = row[1]
					complex_ids.append(entryType)
					complexes.append(row)
					
# Only keep the unique complex ids and check some counts
complex_ids_unique = set(complex_ids)

print("Number of complex ids:",nComplexEntries)
print("Number of unique complex ids:",len(complex_ids_unique))
#print(len(complexes))

# Write the complexes that were filtered out before to a new file
with open('complexes.csv', mode='w') as complexes_file:
	writer = csv.writer(complexes_file, delimiter='\n')
	writer.writerow(complexes)
complexes_file.close()