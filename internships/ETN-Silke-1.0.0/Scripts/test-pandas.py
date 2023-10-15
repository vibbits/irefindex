# This script is not used
import csv, sys
import pandas as pd

complex_ids = []
complexes = []

if __name__ == "__main__":

	# Open and parse the IrefIndex Mitab file.
	# Read in the file 
	irefIndexFile = "9606.mitab.08-22-2022_10000.txt"
	df = pd.read_csv(irefIndexFile, delimiter='\t')
	#print(df.columns)
	#sys.exit()

	#print(entryType[0])
	#sys.exit()
	entryType = df['#uidA']
	expansionModel = df.expansion
	edgeType = df.edgetype 
	#taxonId_protB = df.taxb.apply
	taxonId_protB = df.taxb.split('(')[0].replace('taxid:','')
	
	if taxonId_protB == '9606':
		if 'complex:' in entryType and expansionModel == 'bipartite' and edgeType == 'C':
			
			grouped_complexes = df.groupby(by='#uidA')
			for name,group in grouped_complexes:
				print("Name:",name)
				print("Group:",group.taxb)
	else 	

'''
	for row in df:
		entryType = row[0]
		expansionModel = row[15]
		edgeType = row[52]
		taxonId_protB = row[10].split('(')[0].replace('taxid:','')
		if taxonId_protB == '9606':
			if 'complex:' in entryType and expansionModel == 'bipartite' and edgeType == 'C':
				
				counter = 0
				for group in grouped_complexes:
					counter += 1
					if counter == 10:
						print(group)
						sys.exit()
					
					taxonId_protB = row[10].split('(')[0].replace('taxid:','')
					if taxonId_protB == '9606':


	with open(irefIndexFile, 'r') as ppiFile:
		csvreader = csv.reader(ppiFile, delimiter='\t')
		header = next(csvreader)

		nComplexEntries = 0
		for row in csvreader:
			#print(row)
			#sys.exit()
			entryType = row[0]
			expansionModel = row[15] #'bipartite' for multiprotein complexes in iRefIndex.
			edgeType = row[52]
			taxonId_protA = row[9].split('(')[0].replace('taxid:','')
			taxonId_protB = row[10].split('(')[0].replace('taxid:','')
			if taxonId_protB == '9606':
				if "complex:" in entryType and expansionModel == 'bipartite' and edgeType == 'C':
					nComplexEntries += 1
					complexId = row[0]
					proteinSubunitA = row[1]
					complex_ids.append(entryType)
					complexes.append(row)
					

complex_ids_unique = set(complex_ids)
print(complex_ids_unique)
print("Number of complex ids:",len(complex_ids))
print("Number of unique complex ids:",len(complex_ids_unique))
print(len(complexes))
'''

'''
with open('complexes.csv', mode='w') as complexes_file:
	writer = csv.writer(complexes_file, delimiter='\n')
	writer.writerow(complexes)
complexes_file.close()
'''