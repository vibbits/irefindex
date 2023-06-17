# Extract all the interactors of 6 different complexes which have 1 common interactor
import csv, sys

complex_ids1 = []

if __name__ == "__main__":
	# Read in the file and filter on certain complex ids to get its interactors
	irefIndexFile = "9606.mitab.08-22-2022.txt"
	with open(irefIndexFile, 'r') as ppiFile:
		csvreader = csv.reader(ppiFile, delimiter='\t')
		header = next(csvreader)

		nComplexEntries = 0
		for row in csvreader:
			entryType = row[0]
			expansionModel = row[15] #'bipartite' for multiprotein complexes in iRefIndex.
			edgeType = row[52]
			taxonId_protB = row[10].split('(')[0].replace('taxid:','')
			if taxonId_protB == '9606':
				if "complex:RHZO87ChDcZQNLG/C2LHGaeXLHw" in entryType and expansionModel == 'bipartite' and edgeType == 'C':
					nComplexEntries += 1
					complexId = row[0]
					proteinSubunitA = row[1]
					complex_ids1.append(row)
				elif "complex:CKQk4qHFCUSaZQzdLogIi8W1m3o" in entryType and expansionModel == 'bipartite' and edgeType == 'C':
					nComplexEntries += 1 
					complexId = row[0]
					proteinSubunitA = row[1]
					complex_ids1.append(row)
				elif "complex:cxG5/M5+0DeQwOjYeAEPXk2NluQ" in entryType and expansionModel == 'bipartite' and edgeType == 'C':
					nComplexEntries += 1 
					complexId = row[0]
					proteinSubunitA = row[1]
					complex_ids1.append(row)
				elif "complex:+2iu3CFO3h5y5P0HReAVd+f3+6I" in entryType and expansionModel == 'bipartite' and edgeType == 'C':
					nComplexEntries += 1 
					complexId = row[0]
					proteinSubunitA = row[1]
					complex_ids1.append(row)
				elif "complex:YBLG0W43Zi4brSjnEY0WixObGJ0" in entryType and expansionModel == 'bipartite' and edgeType == 'C':
					nComplexEntries += 1 
					complexId = row[0]
					proteinSubunitA = row[1]
					complex_ids1.append(row)
				elif "complex:wJS3Cx3PC+ZhdSGn57ebLK9loiA" in entryType and expansionModel == 'bipartite' and edgeType == 'C':
					nComplexEntries += 1 
					complexId = row[0]
					proteinSubunitA = row[1]
					complex_ids1.append(row)

# Write the output to a csv file to analyse
with open('complex_ids1.csv', mode='w') as complex_ids_file:
	writer = csv.writer(complex_ids_file, delimiter='\n')
	writer.writerow(complex_ids1)
complex_ids_file.close()
