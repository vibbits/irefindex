# Distinguish the complexes in which at least one component is non-human from all the complexes.
# Now the number 22981 is reduced.to 19139
import csv,sys, pickle

NHComplexes = []
onlyhumancomplexes = {}
allhumancomplexes = {}

if __name__ == "__main__":

	# Read in the file and filter on entryType, expansionModel, edgeType and if necessary on source
	irefIndexFile = "9606.mitab.08-22-2022.txt"
	with open(irefIndexFile, 'r',encoding="utf-8") as ppiFile:
		csvreader = csv.reader(ppiFile, delimiter='\t')
		header = next(csvreader)
		counter = 0

		for row in csvreader:
			counter += 1
			entryType = row[0]
			expansionModel = row[15]
			edgeType = row[52]
			source = row[12]
			interactorId = row[1].split('(')[0].replace('uniprotkb:','')
			taxonId_protB = row[10].split('(')[0].replace('taxid:','')

			# Make a dictionary with all interactor ids for each complex id where the taxonomy of each interactor is not always 9606
			if 'complex:' in entryType and expansionModel == 'bipartite' and edgeType == 'C' and 'bar' in source:
				if entryType not in onlyhumancomplexes:
					allhumancomplexes[entryType] = []
					allhumancomplexes[entryType].append(interactorId)
				else:
					allhumancomplexes[entryType].append(interactorId)

				# Filter out the complexes which have an interactor with taxonomy other than 9606 in a seperate list
				if taxonId_protB != '9606':
					NHComplexes.append(entryType)
				
				# Iterate over the NHComplexes list to only keep complexes of which all interactors have taxonomy 9606
				if entryType not in NHComplexes:
					if entryType not in onlyhumancomplexes:
						onlyhumancomplexes[entryType] = []
						onlyhumancomplexes[entryType].append(interactorId)
						
					else:
						onlyhumancomplexes[entryType].append(interactorId)
			
			# During the execution, check how many lines have been processed
			if counter % 10000 == 0:
				print("Processed {} lines".format(counter))

		# Some informative prints
		print("Number of complexes with non-human interactor:",len(set(NHComplexes)))
		print("Total number of complexes:",len(allhumancomplexes))
		print("Number of only human complexes:",len(onlyhumancomplexes))

		# Write the output to pickle files 
		with open('allHumanComplexes_bar.pickle', 'wb') as output:
			pickle.dump(allhumancomplexes, output, pickle.HIGHEST_PROTOCOL)

		with open('onlyHumanComplexes_bar.pickle', 'wb') as output:
			pickle.dump(onlyhumancomplexes, output, pickle.HIGHEST_PROTOCOL)
