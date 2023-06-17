# 22 Nov 2021. Parse n-ary complexes annotated by iRefIndex and create a list of the protein components per complex rogid.
# Input: the iRefIndex mitab file (modify file name as appropriate).
# Add/modify organism taxonomic identifiers as necessary. Only complexes from the input list of organisms will be stored.
# Mainak Guharoy. VIB Bioinformatics Core.

import csv,sys,pickle

multiproteinComplexes = {} # Store the identifiers and protein component data for iRefIndex complexes.
organisms = ['9606'] # Taxonomic identifiers of organisms to keep.

def getUniProtID(genericProtId,idMappingDict):
	if 'uniprotkb:' in genericProtId:
		return genericProtId.replace('uniprotkb:', ''),0
	elif 'refseq:' in genericProtId:
		refseqProtId = genericProtId.replace('refseq:', '')
		try:
			return idMappingDict[refseqProtId],0
		except KeyError:
			return genericProtId,-1
	elif 'GenBank:' in genericProtId:
		refseqProtId = genericProtId.replace('GenBank:', '')
		try:
			return idMappingDict[refseqProtId],0
		except KeyError:
			return genericProtId,-1
	else:
		return genericProtId,-1

# check the content of generticProtId and see if it is uniprotkb, refseq, GenBank or something else
# if it is uniprotkb, return the id without 'uniprotkb' and add 0? 
# if it is refseq, add the id without 'refseq' to a new variable 'refseqProtId'. Try looking for the refseq id in idMappingDict and if it is there, return the corresponding 
# value of the id with a 0. If it's not in there, retung the original input genericProtId with a -1. 
# if it is GenBank, add the id without 'GenBank' to a new variable 'refseqProtId'. Try looking for the refseq id in idMappingDict and if it is there, return the corresponding 
# value of the id with a 0. If it's not in there, retung the original input genericProtId with a -1. 
# if the id is something else, return the original input with a -1


def handleIsoforms(uniprotID):
	# Dealing with isoforms. For now, treating all isoform specific partners as wt counterparts.
	if '-' in uniprotID:
		return uniprotID.split('-')[0]
	return uniprotID

# check if there is a '-' in the uniprotID and if there is, split it to remove the '-'

if __name__ == "__main__":

	# Open and parse the RefSeq to UniProt id mapping file (pickle object).
	# The "RefSeq2UniProtIDs.pickle" is created in a script that needs to be executed before this one. 
	# The input is loaded into 'RefSeq2UniProtIds'
	with open("RefSeq2UniProtIDs.pickle","rb") as input:
		refseq2UniProtIds = pickle.load(input)

	# Open and parse the IrefIndex Mitab file.
	# Read in the file 
	# Gather the headers in a variable 'header'
	irefIndexFile = "9606.mitab.08-22-2022.txt"
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
			if "complex:" in entryType and expansionModel == 'bipartite' and edgeType == 'C':
				nComplexEntries += 1
				complexId = row[0] 
				proteinSubunit = row[1]

				# Apply a filter for organisms taxonomic id. Optional.
				taxonId_subunit = row[10].split('(')[0].replace('taxid:','') # filter out the taxonID
				if taxonId_subunit not in organisms: # organisms is 9606, human
					continue

				# Try to convert protein id to uniprot id.
				subunitId,idConversion = getUniProtID(proteinSubunit,refseq2UniProtIds)
				if idConversion == 0:
					subunitId = handleIsoforms(subunitId) 

					# Add subunit information to the multiprotein complex data.
					if complexId not in multiproteinComplexes:
						multiproteinComplexes[complexId] = [subunitId]
					else:
						if subunitId not in multiproteinComplexes[complexId]:
							multiproteinComplexes[complexId].append(subunitId)

	print("Number of identified complexes:",len(multiproteinComplexes))
	#print(multiproteinComplexes)
	#print(multiproteinComplexes["complex:K9rb8fer7sOb/6AVPLrfs630kPQ"])
	#print(len(multiproteinComplexes["complex:K9rb8fer7sOb/6AVPLrfs630kPQ"]))
	#print(nComplexEntries)

	# Save the protein complexes dictionary as a pickle file.
	with open("PPIComplexes.pickle","wb") as output:
		pickle.dump(multiproteinComplexes,output,pickle.HIGHEST_PROTOCOL)

complex_set = set(multiproteinComplexes)
print("Number of unique complexes: {}".format(len(complex_set)))