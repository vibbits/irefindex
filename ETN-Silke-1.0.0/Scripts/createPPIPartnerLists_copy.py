# 12 Nov 2021. Parse the IrefIndex MITAB file and create a dictionary of PPI partners per UniProt ID.
# The ID mapping (RefSeq: NP_*) to UniProt ID is carried out offline after downloading the ID mapping file from UniProt.
# 23 Nov 2021. Optional: Added parsing data for multiprotein complexes, also obtained from IRefIndex.
# Mainak Guharoy. VIB Bioinformatics Core.

import csv,sys,pickle

organisms = ['9606'] # Taxonomic identifiers of organisms to keep.
proteinsOfInterest = ['Q96EY8','Q9Y4U1','P11310','P49748','Q9H845','P03886','P03923','P28331','O75306','Q8IUX1']
parseComplexes = False #True
ppisDict = {}

def addInteraction(protein, partner):
	if protein not in ppisDict.keys():
		ppisDict[protein] = [partner]
	else:
		if partner not in ppisDict[protein]:
			ppisDict[protein].append(partner)

def getUniProtID(genericProtId,idMappingDict): # this is the same as in the parseIRefIndexComplexes.py script
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

def handleIsoforms(uniprotID):
	# Dealing with isoforms. For now, treating all isoform specific partners as wt counterparts.
	if '-' in uniprotID:
		#if uniprotID.split('-')[1] == '1':
		return uniprotID.split('-')[0]
	return uniprotID

if __name__ == "__main__":

	# Open and parse the RefSeq to UniProt id mapping file (pickle object).
	with open("RefSeq2UniProtIDs.pickle","rb") as input:
		refseq2UniProtIds = pickle.load(input)

	# Open and parse the multiprotein complexes dataset pre-parsed from iRefIndex (pickle object).
	# This PPIComplexes.pickle file is created by executing the previous script (parseIRefIndexComplexes.py)
	with open("PPIComplexes.pickle","rb") as input:
		complexes = pickle.load(input)

	# Open and parse the IrefIndex Mitab file.
	irefIndexFile = "All.mitab.06-11-2021.txt"
	with open(irefIndexFile, 'r') as ppiFile:
		csvreader = csv.reader(ppiFile, delimiter='\t')
		header = next(csvreader)

		for row in csvreader:
			numParticipants = int(row[-1]) #the last row
			ppiType = row[-2] #the second last row

			if ppiType in ['X'] and numParticipants == 2: #X=binary interaction

				# Check for taxonomic identifier and filter interaction by organism.
				taxonId_protA = row[9].split('(')[0].replace('taxid:','')
				taxonId_protB = row[10].split('(')[0].replace('taxid:','')

				if taxonId_protA in organisms and taxonId_protB in organisms and taxonId_protA == taxonId_protB:

					# Protein IDs from columns labelled '#uidA', 'uidB'.
					uniprotId_A,IdConvertFlag_A = getUniProtID(row[0],refseq2UniProtIds)
					uniprotId_B,IdConvertFlag_B = getUniProtID(row[1],refseq2UniProtIds)

					if IdConvertFlag_A == 0 and IdConvertFlag_B == 0:
						uniprotId_A = handleIsoforms(uniprotId_A)
						uniprotId_B = handleIsoforms(uniprotId_B)

						# Add the binary PPI data.
						if uniprotId_A in proteinsOfInterest:
							addInteraction(uniprotId_A, uniprotId_B)
						if uniprotId_B in proteinsOfInterest:
							addInteraction(uniprotId_B, uniprotId_A)

					# Protein IDs (alternate ids, often contains updated Swiss-Prot ids) from 'FinalReferenceA', 'FinalReferenceB'.
					uniprotId_A,IdConvertFlag_A = getUniProtID(row[38],refseq2UniProtIds)
					uniprotId_B,IdConvertFlag_B = getUniProtID(row[39],refseq2UniProtIds)

					if IdConvertFlag_A == 0 and IdConvertFlag_B == 0:
						uniprotId_A = handleIsoforms(uniprotId_A)
						uniprotId_B = handleIsoforms(uniprotId_B)

						# Add the binary PPI data.
						if uniprotId_A in proteinsOfInterest:
							addInteraction(uniprotId_A, uniprotId_B)
						if uniprotId_B in proteinsOfInterest:
							addInteraction(uniprotId_B, uniprotId_A)

			elif ppiType in ['C'] and numParticipants >= 2: #C=complex

				if not parseComplexes:
					continue

				complexRogId = row[0]
				taxonId_subunit = row[10].split('(')[0].replace('taxid:','')
				if taxonId_subunit in organisms:
					# Protein subunit ID from columns labelled 'uidB'.
					uniprotId_subunit,IdConvertFlag = getUniProtID(row[1],refseq2UniProtIds)
					if IdConvertFlag == 0:
						uniprotId_subunit = handleIsoforms(uniprotId_subunit)

						if uniprotId_subunit in proteinsOfInterest:
							complexPartners = complexes[complexRogId]
							for partner in complexPartners:
								addInteraction(uniprotId_subunit,partner)

					# Protein subunit ID from columns labelled 'FinalReferenceB'.
					uniprotId_subunit,IdConvertFlag = getUniProtID(row[39],refseq2UniProtIds)
					if IdConvertFlag == 0:
						uniprotId_subunit = handleIsoforms(uniprotId_subunit)

						if uniprotId_subunit in proteinsOfInterest:
							complexPartners = complexes[complexRogId]
							for partner in complexPartners:
								addInteraction(uniprotId_subunit,partner)

	print(len(ppisDict))

	# Save the partners dictionary as a pickle file.
	if parseComplexes:
		with open("PPIPartnersPerUniProtID_BinaryAndComplexes.pickle","wb") as output:
			pickle.dump(ppisDict,output,pickle.HIGHEST_PROTOCOL)
	else:
		with open("PPIPartnersPerUniProtID_Binary.pickle","wb") as output:
			pickle.dump(ppisDict,output,pickle.HIGHEST_PROTOCOL)
